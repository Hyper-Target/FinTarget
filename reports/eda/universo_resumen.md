# EDA — universo FinTarget y cobertura de etiquetas

- Universo cotizado (EE. UU.): **6,314** emisores
- Con CIK (mapeables a SEC EDGAR / XBRL / 10-K): **5,899** (93%)
- En el S&P 500: **494**
- Tramo por capitalización — large/mid (r1000): **1,000** · small (r2000): **2,000** · micro: **876**

## Capitalización por tramo

| Tramo | Nº emisores | Cap. agregada (US$ B) | Cap. mediana (US$ MM) |
|---|--:|--:|--:|
| Large/Mid (≈ Russell 1000) | 1,000 | 76,440 | 16,780 |
| Small (≈ Russell 2000) | 2,000 | 3,271 | 1,091 |
| Micro | 876 | 46 | 41 |

> Los tramos son una **aproximación pública y reproducible** a los índices Russell, no la composición oficial (iShares exige aceptar un descargo para descargar las tenencias del ETF). La capitalización es la reportada por el *screener* de Nasdaq; puede incluir algún ADR o ticker preliminar. Para el panel de entrenamiento se filtra a emisores con CIK y 10-K en SEC EDGAR.

## Distribución sectorial del universo

| Sector | Emisores | % |
|---|--:|--:|
| Finance | 1,338 | 21.2% |
| Consumer Discretionary | 1,055 | 16.7% |
| Health Care | 1,025 | 16.2% |
| Technology | 721 | 11.4% |
| Industrials | 594 | 9.4% |
| (sin dato) | 579 | 9.2% |
| Real Estate | 229 | 3.6% |
| Energy | 187 | 3.0% |
| Utilities | 154 | 2.4% |
| Basic Materials | 145 | 2.3% |
| Consumer Staples | 144 | 2.3% |
| Telecommunications | 81 | 1.3% |
| Miscellaneous | 62 | 1.0% |

## Dataset de rating crediticio — cobertura

- Observaciones (empresa-año): **5,403**
- Emisores únicos (CIK): **686**
- De esos, todavía cotizan y están en el universo actual: **553** (81%)
- Ventana temporal: **2010–2016**
- Grado de inversión / *high yield*: **62% / 38%**
- Escalones representados: **22** (de AAA a C)
