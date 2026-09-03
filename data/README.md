# Datos de FinTarget

Cinco capas. Solo se versionan en el repo los datasets externos pequeños y de licencia abierta
(`data/external/`). `data/raw/` y `data/processed/` se generan localmente y están en `.gitignore`.

| Capa | Fuente | Acceso | Estado |
|---|---|---|---|
| Contable | SEC EDGAR — API `companyfacts` (XBRL) | Público. `User-Agent` con contacto obligatorio | Verificado (VISA CIK 0001403161) |
| Narrativa 10-K (1993–2020) | `eloukas/edgar-corpus` (HuggingFace) | Público, **no gated**, JSONL por año | Verificado |
| Narrativa 10-K (2021–2025) | Índice EDGAR + parser propio (`ingest/tenk.py`) | Público | Por construir |
| Noticias (ventana 7 días) | Procedimiento del reporte semanal del autor | Uso académico; solo features derivados | Experimental |
| Etiquetas de rating | Ver abajo | Mirrors en GitHub | Verificado |

## `data/external/`

### `ccrd_financial_raw.csv` — 5.403 × 25
*Corporate Credit Rating with Financial Ratios* (Kaggle: `kirtandelwadia/...`), vía el mirror
[`Mengmeara/CCRD-Dataset`](https://github.com/Mengmeara/CCRD-Dataset).
678 empresas, 686 CIK, 2010–2016. 16 ratios (0 % faltantes), **CIK** y **SIC Code** incluidos → llave de
unión con SEC EDGAR y EDGAR-CORPUS. Etiqueta: 22 escalones + binaria grado de inversión / *high yield*
(3.368 / 2.035). Agencias: S&P (2.179), Moody's (1.417), Egan-Jones (1.334), Fitch (427), otras (46).
Licencia de origen: CC BY 4.0.

### `corporate_rating.csv` — 2.029 × 31
*Corporate Credit Rating* (Kaggle: `agewerc/corporate-credit-rating`), vía
[`Agewerc/ML-Finance`](https://github.com/Agewerc/ML-Finance).
593 empresas, 2014–2016. 25 ratios. 10 clases (AAA…D). Sin CIK. Se usa para robustez.

## Pendiente de traer
- *US Company Bankruptcy Prediction* (Kaggle: `utkarshx27/...`, CC0) — ~78k empresa-año, 1999–2018.
