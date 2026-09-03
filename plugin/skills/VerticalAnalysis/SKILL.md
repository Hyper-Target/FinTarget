---
name: VerticalAnalysis
description: Aplica un análisis financiero profesional (vertical, horizontal, indicadores y DuPont) directamente sobre un archivo Excel con los estados financieros de una empresa, siguiendo el estándar de tres niveles NIIF/IFRS + CFA Institute + reporte anual auditado. Distingue el tratamiento de una empresa no financiera (industrial/comercial) del de un banco (métricas Basilea III). Úsalo cuando el usuario pida "análisis vertical", "análisis horizontal", "aplícale indicadores a este Excel", "análisis DuPont" sobre un archivo de Excel existente, o invoque explícitamente FinTech:VerticalAnalysis.
---

# VerticalAnalysis (FinTech)

Skill hermana de [DailyReport](../DailyReport/SKILL.md) e [IncAnalyze](../IncAnalyze/SKILL.md). Mientras `IncAnalyze` investiga una empresa desde cero (SEC EDGAR, Yahoo Finance, etc.) y entrega un informe en Markdown, `VerticalAnalysis` toma un **archivo Excel que el usuario ya tiene** con los estados financieros de una empresa (balance + resultados, varios años) y le **aplica el análisis directamente dentro del mismo libro**: análisis vertical, análisis horizontal, indicadores (liquidez, endeudamiento, solvencia, eficiencia, rentabilidad, DuPont, calidad del balance) — con formulas de Excel reales (no valores pegados) y semáforos de color.

Nació de una sesión real (22-ago-2026) en la que se aplicó este análisis a `Ecopetrol.xlsx` (balance y resultados 2021-2025, en COP millones, cargados desde Investing.com Pro).

## Cuándo usarla

- El usuario tiene un Excel con estados financieros de una empresa y pide "aplícale un análisis vertical", "análisis horizontal", "ponle indicadores", "hazle un DuPont" a ese archivo.
- El usuario pide explícitamente el estándar descrito abajo (NIIF + CFA) sobre un archivo propio.
- El usuario invoca `FinTech:VerticalAnalysis`.

Si en cambio el usuario NO tiene datos todavía y pide "investiga/analiza la empresa X" desde cero, usa [IncAnalyze](../IncAnalyze/SKILL.md) primero para recolectar los datos, y esta skill después si además quiere el análisis vertical/horizontal/indicadores dentro de un Excel.

## Perfil del usuario (asumir siempre)

Científico de Datos en Finanzas — Maestría en Finanzas, Uninorte. Quiere el análisis **dentro del mismo archivo Excel** (no un Markdown aparte), con fórmulas reales (recalculables) y colores que comuniquen qué es lo más importante — no solo una tabla plana de números.

## Estándar técnico (3 niveles) — aplícalo siempre, en este orden

| Nivel | Recurso | Para qué sirve en esta skill |
|---|---|---|
| 1 | IFRS Foundation — **IAS 1** (Presentación de Estados Financieros) | Confirma que el balance y el estado de resultados del Excel del usuario están completos y bien estructurados antes de analizarlos. No inventes subtotales que el archivo no tiene. |
| 2 | IFRS Foundation — **IAS 7** (Estado de Flujo de Efectivo) | Si el Excel NO trae flujo de caja (caso frecuente con exports de terceros), dilo explícitamente en la hoja de metodología y marca como "No disponible" los indicadores de caja (FCO/Utilidad, conversión de EBITDA en efectivo) — nunca los estimes sin decirlo. |
| 3 | CFA Institute — **Analyzing Balance Sheets** | Guía el análisis vertical/horizontal del balance y la sección "Calidad del Balance" (goodwill, intangibles, provisiones, pasivos contingentes). |
| 4 | CFA Institute — **Financial Analysis Techniques** | Guía la hoja de Indicadores: liquidez, endeudamiento, solvencia, eficiencia (actividad), rentabilidad, y la descomposición DuPont del ROE. |
| 5 | CFA Institute — **Financial Reporting Quality** | Guía la lectura crítica: si el archivo no trae notas a los EEFF, dilo — no se puede evaluar calidad de utilidades a fondo sin ellas. |

Un caso bancario (ej. JPMorgan 10-K) es una excelente referencia de divulgación, pero **nunca uses su marco de análisis para una empresa no financiera** — ver sección "Banco vs. empresa no financiera" abajo.

## Paso 1 — Inspeccionar el archivo del usuario

1. Localiza el Excel (normalmente en la carpeta de Reportes del usuario). Si `~$archivo.xlsx` existe junto al archivo real, probablemente está abierto en Excel — no es bloqueante para escribir con `openpyxl`, pero avisa al usuario y evita usar `--force` de recalc si algo falla por bloqueo real.
2. Carga el libro con `openpyxl` (`data_only=True` para ver valores, y por separado sin `data_only` para ver si ya hay fórmulas) y mapea:
   - ¿Qué hoja es el balance? ¿Cuál es el estado de resultados? ¿Hay flujo de caja?
   - ¿En qué fila está cada cuenta? ¿En qué columnas están los años? (anota los números de fila reales — **no asumas que coinciden con los del ejemplo de Ecopetrol**, cada archivo tiene su propio layout).
   - ¿Cuál es la fila de "Total de Activos" (base del análisis vertical del balance) y la de "Ingresos Totales" (base del análisis vertical de resultados)?
   - ¿Los valores son hardcodeados (pegados) o fórmulas? ¿En qué moneda/unidad están (millones, miles, unidades)? ¿Es un banco o una empresa no financiera? (ver clasificación abajo).
3. Si el archivo mezcla texto tipo "-" para celdas sin dato (común en exports de Investing.com/Bloomberg), tus fórmulas deben tratarlas como 0 o "n/d" explícitamente (`ISNUMBER(...)`), nunca dejar que rompan una fórmula con `#VALUE!`.

## Paso 2 — Banco vs. empresa no financiera (decide esto ANTES de construir los indicadores)

**Empresa no financiera** (industrial, comercial, energía, tecnología, etc.) → usa el set de indicadores de la sección "Indicadores" de más abajo (liquidez, endeudamiento, solvencia, eficiencia, rentabilidad, DuPont).

**Banco / entidad financiera** → el marco de arriba **no aplica tal cual**. Un banco no tiene "razón corriente" ni "capital de trabajo" con sentido económico. En su lugar, si el usuario pide analizar un banco, construye estos indicadores (Basilea III / CFA para bancos), documentando de dónde sale cada uno (normalmente solo en el 10-K/informe anual, no en exports estándar de balance):

| Métrica | Qué mide |
|---|---|
| CET1 / CET1 ratio | Capital ordinario de máxima calidad / Activos ponderados por riesgo (RWA) |
| RWA | Activos ponderados por riesgo |
| Leverage ratio | Apalancamiento regulatorio (capital Tier 1 / exposición total) |
| LCR (Liquidity Coverage Ratio) | Liquidez para cubrir salidas de efectivo a 30 días |
| NSFR (Net Stable Funding Ratio) | Estabilidad del fondeo a un año |
| NPL ratio | Cartera vencida/deteriorada sobre cartera total |
| Provisiones / Cartera | Cobertura frente a pérdidas crediticias esperadas |
| NIM (Net Interest Margin) | Margen financiero neto |
| ROE y ROTCE | Rentabilidad sobre patrimonio y sobre patrimonio tangible |
| Loans/Deposits | Cartera de créditos sobre depósitos captados |
| Costo de riesgo | Pérdidas crediticias / cartera promedio |

Fuentes de referencia: BIS — Basel III Monitoring Report, Basel III Capital Adequacy, Basel III Disclosure Requirements. Si el Excel del usuario no trae estos datos (lo normal, salvo que venga directo del 10-K), dilo explícitamente y ofrece construir la hoja con estructura y celdas vacías etiquetadas para que el usuario las llene desde el informe anual, en vez de fabricar cifras.

## Paso 3 — Análisis Vertical (obligatorio, es el entregable principal)

Cada cuenta como **% de una base común**, por cada año de la serie:
- Balance: base = Total de Activos del mismo año.
- Estado de Resultados: base = Ingresos Totales (Ventas) del mismo año.

Formato recomendado (validado en la sesión de referencia): tabla con **valor $ y % lado a lado** por cada año (no solo el %), para que el lector vea la cifra real y su peso relativo sin tener que volver a la hoja fuente. Usa **fórmulas que referencien la hoja original** (`='Balance'!C5/'Balance'!C$16`), nunca copies el resultado como número.

**Color = materialidad**: aplica un `ColorScaleRule` (escala de 3 colores) sobre la columna de "% del total" de cada cuenta — mientras más oscuro, mayor peso sobre el total. Esto hace visualmente evidente cuáles son las cuentas que más importan sin que el lector tenga que leer cada celda.

## Paso 4 — Análisis Horizontal (obligatorio, acompaña siempre al vertical)

Variación % interanual de cada cuenta: `(Año actual / Año anterior) − 1`. Usa `IFERROR` + `ISNUMBER` para blindar contra celdas de texto ("-", "n/a") y contra división por cero.

**Color = dirección del cambio**: `ColorScaleRule` roja-blanca-verde centrada en 0 (rojo = contracción, verde = crecimiento). Esto muestra de inmediato qué líneas se están deteriorando vs. cuáles crecen, cuenta por cuenta.

**Guarda contra "base inmaterial"** (hallazgo de la sesión de referencia, con Ecopetrol): cuando el AÑO BASE de una cuenta es casi cero (ej. una celda con valor 851 en un dataset donde todo lo demás está en miles/millones — típico artefacto de redondeo o de reclasificación puntual de la fuente), la variación % se dispara a cifras sin sentido (se vio un caso real de +215,881%). No es un error de fórmula, es una fórmula matemáticamente correcta aplicada a un dato de base no representativo. Blinda la fórmula con un piso de materialidad: si `ABS(valor_base) < umbral` (en la sesión se usó 5,000, calibrado al orden de magnitud del archivo — ajústalo a la escala real de tus datos), muestra `"n/a (base inmaterial)"` en vez de calcular el %. Importante: el piso se aplica solo al AÑO BASE (denominador) — si en cambio el año ACTUAL colapsa a casi cero partiendo de una base grande y real, esa caída de ~100% sí es información legítima y debe mostrarse como número, no ocultarse.

## Paso 5 — Indicadores (empresa no financiera)

Construye una hoja "Indicadores" con una fila por indicador y una columna por año, agrupada en las categorías de la tabla siguiente. Usa fórmulas que referencien la hoja fuente original directamente (no la hoja de análisis vertical), para minimizar cadenas de referencias.

| Categoría | Indicadores mínimos |
|---|---|
| Liquidez | Razón corriente, prueba ácida, capital de trabajo |
| Endeudamiento | Deuda/Activos, Pasivos/Patrimonio, Deuda Financiera/Patrimonio, Deuda Neta |
| Solvencia | Cobertura de intereses (EBIT/Gastos Financieros), Deuda Neta/EBITDA, vencimientos de deuda (nota si no disponible) |
| Eficiencia (actividad) | Rotación y días de inventario, rotación y días de cartera (DSO), rotación de activos |
| Rentabilidad | Margen bruto, operativo, neto; ROA; ROE (sobre patrimonio **atribuible**, restando interés minoritario si existe) |
| Descomposición DuPont | ROE = Margen Neto × Rotación de Activos × Apalancamiento — verifica que el producto reproduzca el ROE ya calculado (chequeo de consistencia) |
| Calidad del balance | Goodwill/Activos, Intangibles/Patrimonio, Provisiones/Pasivos, pasivos contingentes (nota si no disponible) |
| Caja | FCO/Utilidad Neta, conversión de EBITDA en efectivo — **marca "No disponible" si el archivo no trae Estado de Flujo de Efectivo**; no lo estimes con proxies sin decirlo explícitamente |

### EBITDA cuando la empresa no lo desglosa

Muchos exports de terceros (Investing.com, Bloomberg) no separan D&A por función (COGS vs. Opex) y el estado de resultados no trae una línea de D&A. Proxy validado en la sesión de referencia: **D&A estimado = Δ Depreciación Acumulada del balance** (año actual − año anterior, en valor absoluto) y **EBITDA estimado = EBIT + D&A estimado**. Etiqueta SIEMPRE esta fila como "estimado/proxy" y dile al usuario que la cifra oficial (si existe) puede diferir; el primer año de la serie no tiene D&A estimable (no hay año anterior) → márcalo "n/d", no lo fuerces a 0.

### Semáforos (colores según lo más importante del análisis)

No pintes todo por igual — reserva el semáforo rojo/ámbar/verde (`CellIsRule`) para los indicadores donde existe un umbral de referencia razonable, y usa mapa de calor de tendencia (`ColorScaleRule`) para el resto (rotaciones, márgenes, ROE/ROA histórico). Umbrales de referencia usados en la sesión (ajustables por sector — para una petrolera/O&G; para otros sectores revisa los umbrales antes de reutilizarlos):

| Indicador | Verde | Ámbar | Rojo |
|---|---|---|---|
| Razón corriente | ≥ 1.5x | 1.0x–1.5x | < 1.0x |
| Prueba ácida | ≥ 1.0x | 0.7x–1.0x | < 0.7x |
| Deuda/Activos | < 50% | 50%–65% | > 65% |
| Pasivos/Patrimonio | < 1.0x | 1.0x–1.5x | > 1.5x |
| Deuda Neta/EBITDA | < 1.5x | 1.5x–2.5x | > 2.5x |
| Cobertura de intereses | > 6x | 3x–6x | < 3x |
| Goodwill/Activos | < 5% | 5%–10% | > 10% |
| ROE | > 15% | 8%–15% | < 8% |

El indicador **más importante de toda la hoja** (el que resume mejor la tesis del análisis, normalmente ROE o el que muestre la tendencia más marcada) merece doble tratamiento: mapa de calor de tendencia **y** semáforo de nivel absoluto, para que salte a la vista tanto la trayectoria como el nivel actual.

## Paso 6 — Hoja de Metodología (obligatoria, primera hoja del libro)

Antes de guardar, agrega (o actualiza) una hoja de portada/metodología, primera en el libro, que documente:
1. Los 3-5 niveles del estándar aplicado (tabla de la sección "Estándar técnico" de arriba).
2. Por qué se analiza como empresa no financiera o como banco (justifica la elección).
3. **Fuente exacta de los datos** del archivo original (revisa si hay una columna con URL de origen, como en los exports de Investing.com Pro) y si es primaria o secundaria. Si es secundaria, recomienda al usuario contrastarla contra la fuente primaria:
   - EE. UU. / ADR: SEC EDGAR (10-K/10-Q), `data.sec.gov/api/xbrl/companyfacts/CIK{...}.json` — ver [IncAnalyze](../IncAnalyze/SKILL.md).
   - Colombia: **SIMEV** (Superintendencia Financiera, `www.superfinanciera.gov.co`) para emisores vigilados, o **Superintendencia de Sociedades** (`www.supersociedades.gov.co`, base "SIREM"/10.000 empresas) para no financieras no vigiladas por la Superfinanciera; también el informe anual/reporte integrado en la página de Relación con Inversionistas de la empresa.
4. **Limitaciones explícitas** del archivo (qué falta: flujo de caja, notas a los EEFF, desglose de D&A, vencimientos de deuda, pasivos contingentes) — nunca las rellenes en silencio.
5. Una conclusión de 2-3 líneas con el hallazgo más importante del análisis (para que quien abra el libro entienda el mensaje central sin recorrer todas las hojas).

## Paso 7 — Formato, fórmulas y verificación (obligatorio)

- **Match de convenciones**: si el archivo ya tiene una fuente/formato numérico establecido (revisa `cell.font.name` y `cell.number_format` de una celda existente), úsalo en las hojas nuevas en vez del default de la skill xlsx. En la sesión de referencia el archivo usaba Segoe UI 11 y formato contable con `$` — se respetó en todas las hojas nuevas.
- **Fórmulas reales, nunca valores pegados** — cada celda de análisis vertical/horizontal/indicador debe ser una fórmula que referencie la hoja fuente, para que el libro se recalcule solo si el usuario actualiza los datos originales.
- **Recalcular y verificar cero errores** antes de entregar. `recalc.py` de la skill `xlsx` (basado en LibreOffice) puede fallar en Windows con `module 'socket' has no attribute 'AF_UNIX'` — en ese caso usa el script `scripts/recalc_excel_windows.py` de esta misma skill (Excel vía `pywin32`/COM, `pip install pywin32` si falta): abre el libro, `CalculateFullRebuild()`, guarda y cierra. Después, vuelve a leer el libro con `openpyxl(data_only=True)` y confirma que ningún valor de celda sea un string que empiece por `#` (errores de fórmula).
- **Verificación cruzada obligatoria**: confirma que el % de "Total de Activos" en el análisis vertical dé 100% en cada año, y que "Total de Activos" = "Total Pasivo + Patrimonio" (si el balance lo reporta por separado) — si no cuadra, el problema está en el mapeo de filas, no en la fórmula.
- **Revisión visual**: exporta al menos 2-3 rangos clave como imagen para confirmar que los colores se ven como se espera (columnas no truncadas mostrando `#####`, semáforos visibles) — usa `scripts/export_preview_excel.py` (Excel COM: copia el rango como imagen, la pega en un gráfico temporal y la exporta a PNG; cierra siempre con `SaveChanges=False` para no dejar gráficos residuales en el archivo real) y lee el PNG con la herramienta de lectura de imágenes antes de dar el trabajo por terminado.
- Anchos de columna: para cifras en millones/miles de millones con formato contable, 17 caracteres de ancho suele ser el mínimo para evitar `#####`; las columnas de % pueden ser más angostas (10-11).

## Scripts de referencia

Esta carpeta (`scripts/`) trae el código real usado en la sesión de referencia (Ecopetrol, balance/resultados 2021-2025 desde Investing.com Pro). **No son un motor genérico** — los números de fila están hardcodeados para el layout de ESE archivo. Úsalos como plantilla de patrones (cómo construir las fórmulas con `IFERROR`/`ISNUMBER`, cómo aplicar `ColorScaleRule`/`CellIsRule`, cómo recalcular con Excel COM en Windows, cómo exportar una vista previa) y adáptalos fila por fila al archivo real del usuario en cada nueva sesión:

- `build_analisis_vertical_horizontal.py` — genera las hojas de análisis vertical y horizontal (balance y resultados) a partir de dos hojas fuente.
- `build_indicadores.py` — genera la hoja de Indicadores con las 8 categorías, semáforos y mapas de calor.
- `build_metodologia.py` — genera la hoja de portada/metodología y la mueve al inicio del libro.
- `recalc_excel_windows.py` — recalcula un `.xlsx` vía Excel COM (`Workbooks.Open` → `CalculateFullRebuild()` → `Save` → `Close`). Alternativa a `recalc.py` de la skill `xlsx` cuando LibreOffice no está disponible/falla en Windows.
- `export_preview_excel.py` — exporta un rango de una hoja como PNG (vía Excel COM: `CopyPicture` + pegar en un gráfico temporal + `Export`), para verificación visual rápida de colores/formato.

## Notas y advertencias

- **Nunca fabriques cifras** que el archivo no trae (flujo de caja, D&A oficial, vencimientos de deuda, pasivos contingentes, notas). Dilo explícitamente como "No disponible" y, si aplica, sugiere la fuente primaria donde sí estaría (SEC EDGAR, SIMEV, Supersociedades, informe anual/IR de la empresa).
- **Prioriza la fuente primaria** sobre agregadores de terceros cuando haya discrepancia; si el Excel del usuario viene de un agregador (Investing.com, Bloomberg, etc.), dilo en la hoja de Metodología y recomienda contrastar antes de usar el análisis para una decisión real.
- Si el usuario pide analizar un banco con este flujo, redirígelo a la sección "Banco vs. empresa no financiera" — no le apliques razón corriente ni capital de trabajo a una entidad financiera.
- Cierra siempre con la aclaración de que el análisis es material informativo/educativo, no asesoría de inversión.
