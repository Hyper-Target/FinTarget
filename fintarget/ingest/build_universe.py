"""
build_universe.py — construye el universo de empresas cotizadas de EE. UU. para FinTarget.

Fusiona tres fuentes públicas:
  1. Nasdaq stock screener   -> capitalización bursátil, sector, industria, año de salida a bolsa
  2. SEC company_tickers_exchange.json -> CIK y bolsa (llave para SEC EDGAR / XBRL / 10-K)
  3. Lista de constituyentes del S&P 500 (datasets/s-and-p-500-companies) -> bandera large cap

Genera data/processed/universe.csv con un tramo de tamaño estilo Russell:
    - r1000  : las ~1.000 mayores por capitalización  (aprox. Russell 1000, large/mid cap)
    - r2000  : las ~2.000 siguientes                   (aprox. Russell 2000, small cap)
    - micro  : el resto por debajo                     (micro cap, fuera de índice)

No se descargan las tenencias oficiales del ETF IWM porque iShares exige aceptar un
descargo de responsabilidad; el tramo por capitalización es una aproximación pública y
reproducible del mismo universo.
"""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

RAW = Path(__file__).resolve().parents[2] / "data" / "raw"
OUT = Path(__file__).resolve().parents[2] / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def load_screener() -> pd.DataFrame:
    rows = json.loads((RAW / "nasdaq_screener_all.json").read_text())["data"]["rows"]
    df = pd.DataFrame(rows)
    df["marketCap"] = pd.to_numeric(df["marketCap"], errors="coerce")
    df["ipoyear"] = pd.to_numeric(df["ipoyear"], errors="coerce")
    df = df.rename(columns={"symbol": "ticker"})
    return df[["ticker", "name", "marketCap", "sector", "industry", "ipoyear", "country"]]


def load_sec() -> pd.DataFrame:
    d = json.loads((RAW / "sec_company_tickers_exchange.json").read_text())
    df = pd.DataFrame(d["data"], columns=d["fields"])
    df["cik"] = df["cik"].astype(int)
    return df[["cik", "ticker", "exchange"]]


def load_sp500() -> set[str]:
    df = pd.read_csv(RAW / "sp500_constituents.csv")
    return set(df["Symbol"].str.upper())


def main() -> None:
    scr = load_screener()
    sec = load_sec()
    sp = load_sp500()

    u = scr.merge(sec, on="ticker", how="left")
    u["in_sp500"] = u["ticker"].str.upper().isin(sp)

    # Dedupe de clases de acción / duplicados por emisor: si hay CIK, un CIK = un emisor
    # (colapsa GOOG/GOOGL, BRK/A-BRK/B, etc.), quedándonos con la línea de mayor capitalización.
    with_cik = u[u["cik"].notna()].sort_values("marketCap", ascending=False)
    with_cik = with_cik.drop_duplicates("cik", keep="first")
    no_cik = u[u["cik"].isna()]
    u = pd.concat([with_cik, no_cik], ignore_index=True)

    # Universo primario = emisores con CIK (reportan a la SEC) e incorporados en EE. UU.
    u["universo_primario"] = u["cik"].notna() & (u["country"] == "United States")

    rated = u[u["universo_primario"] & u["marketCap"].notna() & (u["marketCap"] > 0)].copy()
    rated = rated.sort_values("marketCap", ascending=False).reset_index(drop=True)
    rated["cap_rank"] = rated.index + 1
    rated["size_bucket"] = pd.cut(
        rated["cap_rank"],
        bins=[0, 1000, 3000, 10**9],
        labels=["r1000", "r2000", "micro"],
    )

    u = u.merge(rated[["ticker", "cap_rank", "size_bucket"]], on="ticker", how="left")
    u.to_csv(OUT / "universe.csv", index=False)

    print(f"universo total (tras dedupe por CIK): {len(u):,} tickers")
    print(f"con CIK (mapeable a SEC EDGAR): {u['cik'].notna().sum():,}")
    print(f"universo primario (CIK + EE. UU.): {u['universo_primario'].sum():,}")
    print(u["size_bucket"].value_counts(dropna=False).to_dict())
    print(f"S&P 500 encontrados: {u['in_sp500'].sum()}")
    agg = rated.groupby("size_bucket", observed=True)["marketCap"].sum() / 1e12
    print("cap agregada por tramo (US$ B):", (agg * 1000).round(0).to_dict())


if __name__ == "__main__":
    main()
