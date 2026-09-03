---
name: MarketRatios
description: Construye un tablero de ratios de mercado (múltiplos de precio y de firm value, rendimientos y métricas por acción) para una empresa cotizada, dentro de un archivo Excel. Ancla todo al año fiscal real de la empresa, reconcilia los datos sensibles (número de acciones, precio, deuda, caja) entre varias fuentes (SEC EDGAR, Yahoo Finance, Investing.com, stockanalysis.com, macrotrends) y genera una pestaña "Fuentes" con el link exacto de cada dato tomado de la web, celda a celda, para poder auditarlo al instante. Úsalo cuando el usuario pida "ratios de mercado", "múltiplos", "P/E, EV/EBITDA, P/B", "valoración por múltiplos", "dividend yield / FCF yield", o invoque explícitamente FinTech:MarketRatios.
---

# MarketRatios (FinTech)

Skill hermana de [VerticalAnalysis](../VerticalAnalysis/SKILL.md), [RatioAnalysis](../RatioAnalysis/SKILL.md), [WaccModel](../WaccModel/SKILL.md) e [IncAnalyze](../IncAnalyze/SKILL.md).

- `RatioAnalysis` calcula ratios **contables** (salen solo de los estados financieros).
- **`MarketRatios` calcula ratios de MERCADO**: los que mezclan una cifra contable con el **precio de la acción** (P/E, EV/EBITDA, P/B, dividend yield, FCF yield, PEG…). Requiere datos de la web, y por eso el foco de la skill es **de dónde salió cada número y cómo se reconcilió**.

El entregable es el propio Excel, con una pestaña **Fuentes** que da el link preciso de cada dato tomado de internet.

Nació de la sesión del 29-ago-2026 (Tecnoglass / TGLS, FY dic-2025, datos de SEC EDGAR 10-K + Damodaran + stockanalysis + US Treasury).

## Cuándo usarla

- El usuario tiene (o quiere) los múltiplos de mercado de una empresa cotizada: "dame el P/E histórico", "múltiplos de valoración", "EV/EBITDA por año", "a cuánto cotiza vs sus fundamentales".
- El usuario quiere un tablero auditable donde cada dato de mercado tenga su fuente.
- El usuario invoca `FinTech:MarketRatios`.

Si el usuario quiere el **costo de capital**, usa [WaccModel](../WaccModel/SKILL.md) (que reutiliza la capitalización de mercado y el beta que produce esta skill).

## Perfil del usuario (asumir siempre)

Científico de Datos en Finanzas — Maestría en Finanzas, Uninorte. Quiere el tablero **dentro del Excel**, con fórmulas recalculables, y **exige poder verificar cada dato web con un clic** (pestaña Fuentes con URL exacta por celda).

## Principio rector: año fiscal + reconciliación + trazabilidad

### 1. Ancla todo al año fiscal REAL de la empresa

- Determina el cierre fiscal (mes/día) desde el 10-K / 20-F (portada "fiscal year ended ...") o el 6-K. Tecnoglass cierra el **31 de diciembre**; otras cierran en junio, septiembre, enero…
- Un múltiplo "a FY2024" usa: **numerador de mercado a la fecha de cierre fiscal** (precio y # de acciones al 31-dic-2024, deuda y caja del balance de cierre) y **denominador = cifra del año fiscal 2024**. No mezcles precio de hoy con utilidad de hace dos años.
- El múltiplo **"actual / TTM"** usa precio y acciones de hoy contra la cifra de los últimos 12 meses reportados (suma de trimestres).
- Ojo con reorganizaciones (holding, spin-off, cambio de ticker), splits y cambios de cierre fiscal: anótalos.

### 2. Reconcilia los datos sensibles entre fuentes

Para **# de acciones, precio, deuda total, caja, EBITDA, FCF, dividendo** toma el dato de **al menos dos** fuentes de esta jerarquía y deja constancia:

| Prioridad | Fuente | Para qué | Nota |
|---|---|---|---|
| 1 (primaria) | **SEC EDGAR** 10-K/10-Q/8-K (o 20-F/6-K para emisores extranjeros) — portada y notas | # acciones en circulación (portada), deuda y su tasa efectiva (nota de deuda), impuesto efectivo, EBITDA-building blocks | `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K` · descargar el `.htm` con `curl -A "nombre correo"` (SEC bloquea user-agents genéricos) |
| 2 | **Yahoo Finance** `/quote/{T}/key-statistics` | precio, market cap, shares outstanding, beta 5Y, EV, múltiplos TTM | a veces devuelve 503/SPA; reintentar o usar stockanalysis |
| 2 | **stockanalysis.com** `/stocks/{t}/statistics/` y `/financials/ratios/` | múltiplos por año fiscal, EV, FCF, tabla histórica limpia | muy consistente para series por FY |
| 3 | **Investing.com** | contraste de EPS, dividendo, acciones | agregador; discrepancias frecuentes en años lejanos |
| 3 | **macrotrends.net** `/stocks/charts/{T}/{name}/pe-ratio` | precio y P/E por año (para reconstruir múltiplos históricos) | a veces 403 |

Cuando dos fuentes discrepen **materialmente** (p. ej. # de acciones 44,7 M vs 46,6 M porque una usa el conteo de portada y otra el promedio ponderado diluido): **muestra ambos valores, elige uno con criterio explícito y anótalo**. Regla por defecto:
- **# de acciones para capitalización de mercado** → acciones **en circulación** de la portada del último 10-K/10-Q (no el promedio ponderado, no las emitidas con tesorería).
- **# de acciones para EPS** → promedio ponderado **diluido** del período (viene del propio estado de resultados).
- **Deuda** → deuda financiera bruta de la nota de deuda del 10-K (obligaciones bajo acuerdos de financiación), no "total liabilities".
- **Precio** → cierre más reciente; anota la fecha exacta.

### 3. Trazabilidad celda a celda — la pestaña `Fuentes`

Es **obligatoria y es el corazón de esta skill**. Una fila por cada dato que se tomó de la web (no por cada celda calculada). Columnas:

| Columna | Contenido |
|---|---|
| `ID` | Etiqueta corta (`PRICE`, `SHARES_OUT`, `DEBT_2025`, `SOFR`, `BETA_5Y`, `ERP_US`…) |
| `Dato` | Descripción en palabras |
| `Valor usado` | El número que entró al modelo |
| `Unidad` | USD, USD mm, %, x, # acciones… |
| `Fuente` | Nombre (SEC EDGAR 10-K FY2025 · Yahoo Finance · Damodaran · stockanalysis.com) |
| `URL exacta` | El link **directo a la página del dato** (no la home del sitio). Hipervínculo real de Excel. |
| `Fecha de acceso` | AAAA-MM-DD en que se consultó |
| `Valor alterno (otra fuente)` | El número de la 2ª fuente, si difiere |
| `Criterio / nota` | Por qué se eligió ese valor; discrepancias; ajustes |

Las hojas de cálculo del modelo **referencian la hoja `Fuentes`** (p. ej. `='Fuentes'!C5`) para los datos web, de modo que cambiar el dato y su link en un solo lugar actualiza todo. Los hipervínculos se ponen con `cell.hyperlink = url` + `cell.style = "Hyperlink"`.

## Contenido del tablero de ratios

Serie por año fiscal (los últimos 4-5) **más** una columna "Actual / TTM".

| Grupo | Ratios |
|---|---|
| **Por acción** | UPA (EPS) básica y diluida · Valor en libros por acción (BVPS) · Ventas por acción (SPS) · FCF por acción (FCFPS) · Dividendo por acción (DPS) |
| **Múltiplos de precio (equity)** | P/E *trailing* · P/E *forward* (si hay estimado) · P/VL (P/B) · P/Ventas (P/S) · P/FCF · PEG (P/E ÷ crecimiento esperado de UPA) |
| **Múltiplos de firm value (EV)** | EV/EBITDA · EV/EBIT · EV/Ventas · EV/FCF · EV/(EBITDA−Capex) |
| **Rendimientos (yields)** | Earnings yield (1/PE) · FCF yield · Dividend yield · Buyback yield · **Shareholder yield** (div + recompras netas) / capitalización |
| **Política de capital** | Payout (dividendo/UPA) · Cobertura del dividendo con FCF |
| **Construcción de EV** | Capitalización = precio × acciones en circulación · EV = Capitalización + Deuda financiera − Caja e inversiones CP + Interés minoritario + Acciones preferentes |

### Cross-checks obligatorios (fila de verificación, debe dar ~0)

- Capitalización = precio × # acciones.
- EV reconstruido = EV reportado por la fuente de contraste (tolerancia por diferencia de fecha).
- Earnings yield = 1 / (P/E).
- P/E = P/VL ÷ ROE (identidad de DuPont del múltiplo).

## Semáforos y contexto

- Los múltiplos **no tienen umbral absoluto**: usa **mapa de calor de la serie** (cada múltiplo vs su propia historia) y, si el usuario lo pide, una columna con la mediana de un set de comparables.
- Marca con nota el múltiplo cuando el denominador sea negativo o cercano a cero (P/E n/s si UPA < 0; EV/FCF n/s si FCF < 0).
- Añade una fila de **descuento/premio vs. su promedio de 5 años** para cada múltiplo (mapa de calor rojo = caro / verde = barato).

## Paso a paso

1. **Identifica CIK y cierre fiscal** (SEC EDGAR full-text search o `company_tickers.json`). Descarga el último 10-K/10-Q con `curl -A "MiNombre micorreo@dominio"`.
2. **Extrae de la primaria**: acciones en circulación (portada), acciones diluidas promedio (estado de resultados), deuda financiera y su tasa efectiva (nota), caja, dividendos pagados, recompras (estado de flujos / patrimonio), impuesto efectivo.
3. **Trae de las secundarias**: precio y fecha, market cap, EV, beta, y la **serie histórica de múltiplos por FY** (stockanalysis `/financials/ratios/`), para contrastar.
4. **Llena la hoja `Fuentes`** con una fila por dato, URL exacta e hipervínculo.
5. **Construye `Datos de Mercado`**: bloque de reconciliación (valor fuente 1 / valor fuente 2 / valor elegido / criterio) para acciones, precio, deuda, caja, EBITDA, FCF, dividendo.
6. **Construye `Ratios de Mercado`**: fórmulas que referencian `Datos de Mercado` y las hojas de estados financieros (si están en el mismo libro) o `Fuentes`. Serie por FY + TTM. Mapa de calor por fila. Filas de cross-check.
7. **Recalcula** con `scripts/recalc_excel_windows.py` (Excel COM) y confirma cero celdas `#`. Revisa 2-3 rangos con `scripts/export_preview_excel.py`.
8. **Metodología / Notas**: fuente primaria vs secundaria, fecha de los precios, reorganizaciones/splits, y aviso de que es material informativo, no asesoría.

## Scripts

`scripts/build_market_ratios.py` — genera `Fuentes`, `Datos de Mercado` y `Ratios de Mercado`. Parametrizado por un dict `FUENTES` (id → dato, valor, unidad, fuente, url, fecha, alterno, nota) y un dict `FY` con las cifras contables por año. **No es un motor genérico**: en cada sesión se rellena con los datos reales de la empresa. `recalc_excel_windows.py` y `export_preview_excel.py` como en las otras skills.

## Notas y advertencias

- **La fuente primaria es SEC EDGAR** (o 20-F/6-K). Los agregadores se usan para contrastar y para la serie histórica de precios, no como verdad única.
- **Nunca inventes un precio, un # de acciones o un dividendo.** Si no lo encuentras, deja la celda vacía y anótalo en `Fuentes`.
- Registra **la fecha de acceso** de cada dato web: los precios cambian a diario y el modelo debe decir "a qué día" está.
- Emisor extranjero (ADR): revisa si reporta en US GAAP o IFRS y si el # de acciones del ADR ≠ acciones ordinarias (ratio de ADR).
- Cierra con la aclaración de material informativo/educativo, no asesoría de inversión.
