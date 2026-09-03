"""
00_eda.py — exploración inicial (EDA) del universo FinTarget y de los datasets de etiquetas.

Produce:
  reports/eda/universo_resumen.md
  reports/eda/fig_capitalizacion.png
  reports/eda/fig_sectores.png
  reports/eda/fig_rating_cobertura.png

Ejecutar desde la raíz del repo:  python notebooks/00_eda.py
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
EXT = ROOT / "data" / "external"
OUT = ROOT / "reports" / "eda"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"figure.dpi": 120, "font.size": 9, "axes.grid": True, "grid.alpha": 0.3})


def main() -> None:
    u = pd.read_csv(PROC / "universe.csv")
    r = pd.read_csv(EXT / "ccrd_financial_raw.csv")

    lines: list[str] = []
    add = lines.append
    add("# EDA — universo FinTarget y cobertura de etiquetas\n")
    add(f"- Universo cotizado (EE. UU.): **{len(u):,}** emisores")
    add(f"- Con CIK (mapeables a SEC EDGAR / XBRL / 10-K): **{u['cik'].notna().sum():,}** "
        f"({u['cik'].notna().mean():.0%})")
    add(f"- En el S&P 500: **{int(u['in_sp500'].sum())}**")
    b = u["size_bucket"].value_counts()
    add(f"- Tramo por capitalización — large/mid (r1000): **{b.get('r1000',0):,}** · "
        f"small (r2000): **{b.get('r2000',0):,}** · micro: **{b.get('micro',0):,}**\n")

    # capitalización agregada por tramo
    cap = (u.dropna(subset=["size_bucket"])
             .groupby("size_bucket", observed=True)["marketCap"]
             .agg(["count", "sum", "median"]))
    cap["sum"] /= 1e12
    cap["median"] /= 1e9
    add("## Capitalización por tramo\n")
    add("| Tramo | Nº emisores | Cap. agregada (US$ B) | Cap. mediana (US$ MM) |")
    add("|---|--:|--:|--:|")
    names = {"r1000": "Large/Mid (≈ Russell 1000)", "r2000": "Small (≈ Russell 2000)", "micro": "Micro"}
    for k in ["r1000", "r2000", "micro"]:
        if k in cap.index:
            row = cap.loc[k]
            add(f"| {names[k]} | {int(row['count']):,} | {row['sum']*1000:,.0f} | {row['median']*1000:,.0f} |")
    add("\n> Los tramos son una **aproximación pública y reproducible** a los índices Russell, no la "
        "composición oficial (iShares exige aceptar un descargo para descargar las tenencias del ETF). "
        "La capitalización es la reportada por el *screener* de Nasdaq; puede incluir algún ADR o "
        "ticker preliminar. Para el panel de entrenamiento se filtra a emisores con CIK y 10-K en SEC EDGAR.\n")

    # sectores
    add("## Distribución sectorial del universo\n")
    sec = u["sector"].fillna("(sin dato)").value_counts()
    add("| Sector | Emisores | % |")
    add("|---|--:|--:|")
    for s, n in sec.items():
        add(f"| {s} | {n:,} | {n/len(u):.1%} |")
    add("")

    # cobertura del dataset de rating
    r_ciks = set(pd.to_numeric(r["CIK"], errors="coerce").dropna().astype(int))
    u_ciks = set(u["cik"].dropna().astype(int))
    inter = r_ciks & u_ciks
    add("## Dataset de rating crediticio — cobertura\n")
    add(f"- Observaciones (empresa-año): **{len(r):,}**")
    add(f"- Emisores únicos (CIK): **{len(r_ciks):,}**")
    add(f"- De esos, todavía cotizan y están en el universo actual: **{len(inter):,}** "
        f"({len(inter)/len(r_ciks):.0%})")
    add(f"- Ventana temporal: **{int(r['Rating Date'].min())}–{int(r['Rating Date'].max())}**")
    ig = (r["Binary Rating"] == 1).mean()
    add(f"- Grado de inversión / *high yield*: **{ig:.0%} / {1-ig:.0%}**")
    add(f"- Escalones representados: **{r['Rating'].nunique()}** (de AAA a C)\n")

    # figuras
    fig, ax = plt.subplots(figsize=(6, 3.2))
    d = u.dropna(subset=["marketCap"])
    ax.hist(d["marketCap"].clip(upper=5e11) / 1e9, bins=60, color="#2b6cb0")
    ax.set_xlabel("Capitalización bursátil (US$ B, recortada a 500)")
    ax.set_ylabel("Nº de emisores")
    ax.set_title("Distribución de la capitalización — universo FinTarget")
    fig.tight_layout(); fig.savefig(OUT / "fig_capitalizacion.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 3.6))
    sec.sort_values().plot.barh(ax=ax, color="#2f855a")
    ax.set_xlabel("Nº de emisores"); ax.set_title("Emisores por sector")
    fig.tight_layout(); fig.savefig(OUT / "fig_sectores.png"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 3.2))
    order = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "CC", "C"]
    g = (r["Rating"].str.replace(r"[+-]", "", regex=True).value_counts()
         .reindex(order).fillna(0))
    g.plot.bar(ax=ax, color=["#2f855a"]*4 + ["#c05621"]*5)
    ax.set_ylabel("Observaciones"); ax.set_title("Dataset de rating — distribución por grado")
    fig.tight_layout(); fig.savefig(OUT / "fig_rating_cobertura.png"); plt.close(fig)

    (OUT / "universo_resumen.md").write_text("\n".join(lines), encoding="utf-8")
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("\n".join(lines))
    print(f"\n-> {OUT/'universo_resumen.md'} + 3 figuras")


if __name__ == "__main__":
    main()
