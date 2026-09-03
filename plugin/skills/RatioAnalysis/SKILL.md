---
name: RatioAnalysis
description: Calcula un tablero completo de ratios / indicadores financieros dentro de un archivo Excel que ya tiene el balance y el estado de resultados de una empresa (varios años). Genera una hoja "Indicadores" con fórmulas de Excel reales (vinculadas a las hojas fuente, recalculables), agrupadas en liquidez, endeudamiento, solvencia, eficiencia, rentabilidad, descomposición DuPont del ROE, calidad del balance y caja, con semáforos de color y umbrales de referencia por sector. Distingue empresa no financiera de banco (Basilea III). Úsalo cuando el usuario pida "calcula los ratios / indicadores", "hazme el análisis de razones financieras", "aplícale ratios a este Excel", "análisis DuPont", o invoque explícitamente FinTech:RatioAnalysis.
---

# RatioAnalysis (FinTech)

Skill hermana de [VerticalAnalysis](../VerticalAnalysis/SKILL.md), [IncAnalyze](../IncAnalyze/SKILL.md) y [DailyReport](../DailyReport/SKILL.md).

- `IncAnalyze` recolecta los datos de una empresa desde cero (SEC EDGAR, Yahoo, etc.).
- `VerticalAnalysis` toma un Excel con estados financieros y le añade análisis **vertical** y **horizontal** dentro del mismo libro.
- **`RatioAnalysis` toma ese mismo tipo de Excel y le añade el tablero de RATIOS / INDICADORES**: una hoja `Indicadores` con ~35 razones financieras como fórmulas reales de Excel, semáforos de color y la descomposición DuPont del ROE con chequeo de consistencia.

Se apoya en el mismo estándar de 3 niveles (IFRS + CFA Institute) que `VerticalAnalysis`. El entregable es **el propio archivo Excel**, no un Markdown aparte.

Nació de la sesión del 29-ago-2026 en la que se analizó Tecnoglass (`Data - TGLS.xlsx`, balance y resultados 2021-2025 cargados desde Investing.com), después de aplicarle `VerticalAnalysis`.

## Cuándo usarla

- El usuario tiene un Excel con balance + estado de resultados (varios años) y pide "calcúlame los ratios", "los indicadores", "las razones financieras", "el DuPont", "la cobertura de intereses", "el ROE / ROA", "apalancamiento", etc.
- El usuario acaba de correr `VerticalAnalysis` sobre un archivo y ahora quiere los indicadores en una pestaña más.
- El usuario invoca `FinTech:RatioAnalysis`.

Si el usuario todavía **no tiene los datos**, usa primero `IncAnalyze` para recolectarlos. Si quiere análisis vertical/horizontal además de ratios, corre `VerticalAnalysis` primero (esta skill puede correrse después, sobre el mismo libro).

## Perfil del usuario (asumir siempre)

Científico de Datos en Finanzas — Maestría en Finanzas, Uninorte. Quiere el tablero **dentro del Excel**, con fórmulas recalculables vinculadas a las hojas fuente y colores que comuniquen nivel y tendencia (no una tabla plana). Formato "simple y sencillo".

## Estándar técnico (mismos niveles que VerticalAnalysis)

| Nivel | Recurso | Uso en esta skill |
|---|---|---|
| 1 | IFRS — **IAS 1** | Confirma que el balance y el estado de resultados tienen las líneas que los ratios necesitan (activo/pasivo corriente, EBIT, gastos financieros, patrimonio atribuible). No inventes una línea que el archivo no tiene: márcala "No disponible". |
| 2 | IFRS — **IAS 7** | Si el Excel NO trae Estado de Flujo de Efectivo, los ratios de caja (FCO/Utilidad neta, FCO/EBITDA, FCL) se marcan **"No disponible"** — nunca se estiman en silencio. |
| 3 | CFA Institute — **Financial Analysis Techniques** | Marco maestro del tablero: liquidez, solvencia (endeudamiento), actividad (eficiencia), rentabilidad y **DuPont**. Ver `references/ratios_catalogo.md`. |
| 4 | CFA Institute — **Analyzing Balance Sheets** | Sección "Calidad del balance": goodwill, intangibles, provisiones, impuestos diferidos, deuda fuera de balance. |
| 5 | CFA Institute — **Financial Reporting Quality** | Lectura crítica: sin notas a los EEFF no se puede evaluar a fondo la calidad de las utilidades ni los pasivos contingentes — dilo. |

Para un **banco**, este marco no aplica: ver "Banco vs. empresa no financiera".

## Paso 1 — Inspeccionar el archivo

1. Localiza el Excel (carpeta de Reportes del usuario). Si `~$archivo.xlsx` existe, avisa que puede estar abierto en Excel.
2. Carga con `openpyxl` **dos veces** (`data_only=True` para valores, sin `data_only` para fórmulas) y mapea, anotando **el número de fila real de cada cuenta** (cada archivo tiene su propio layout — no asumas el de Tecnoglass ni el de Ecopetrol):

   | Necesitas ubicar | En la hoja | Se usa para |
   |---|---|---|
   | Activo corriente, Pasivo corriente | Balance | Liquidez |
   | Inventario, Cuentas por cobrar | Balance | Prueba ácida, DIO, DSO |
   | Efectivo (+ inversiones CP) | Balance | Deuda neta, prueba ácida |
   | Deuda financiera total (corriente + LP + leasing) | Balance | Apalancamiento, deuda neta |
   | Activo total, Pasivo total, Patrimonio total | Balance | Endeudamiento, ROA, DuPont |
   | Interés minoritario (patrimonio) | Balance | Patrimonio **atribuible** (ROE) |
   | Goodwill, Intangibles, Impuesto diferido, Provisiones | Balance | Calidad del balance |
   | Ingresos, Costo de ventas, Utilidad bruta | Resultados | Márgenes, rotaciones |
   | EBIT (utilidad operativa) | Resultados | Margen operativo, cobertura de intereses |
   | Gastos financieros / intereses | Resultados | Cobertura de intereses |
   | EBITDA (o D&A para estimarlo) | Resultados | Deuda neta / EBITDA |
   | Utilidad neta **atribuible a la controladora** | Resultados | Margen neto, ROA, ROE |

3. Trata `"-"`, `"n/a"`, celdas vacías como texto: **todas las fórmulas de ratio deben blindarse con `IFERROR` + `ISNUMBER`** para que nunca devuelvan `#VALUE!` ni `#DIV/0!`.
4. Anota la moneda/unidad (millones, miles) y **si es banco o no** (ver abajo).

## Paso 2 — Banco vs. empresa no financiera (decidir ANTES de construir)

**Empresa no financiera** (industrial, comercial, tecnología, energía, materiales…) → tablero estándar de `references/ratios_catalogo.md`.

**Banco / entidad financiera** → el marco estándar NO aplica (un banco no tiene "razón corriente" ni "capital de trabajo" con sentido). Construye en su lugar: CET1 ratio, RWA, Leverage ratio (Basilea III), LCR, NSFR, NPL ratio, Provisiones/Cartera, NIM, ROE y ROTCE, Loans/Deposits, Costo de riesgo. Referencias: BIS — Basel III Monitoring Report / Capital Adequacy / Disclosure Requirements. Si el Excel no trae estos datos (lo normal salvo que venga del 10-K/informe anual), **dilo y construye la hoja con celdas vacías etiquetadas** para que el usuario las llene desde el informe anual; no fabriques cifras.

## Paso 3 — Construir la hoja `Indicadores`

Una fila por ratio, una columna por año. Agrupada en categorías con fila-título de color. Cada celda es una **fórmula que referencia la hoja fuente directamente** (no la hoja de análisis vertical, para minimizar cadenas de referencias).

Categorías y contenido mínimo (fórmulas y umbrales completos en `references/ratios_catalogo.md`):

| Categoría | Ratios mínimos |
|---|---|
| **Liquidez** | Razón corriente · Prueba ácida · Razón de efectivo · Capital de trabajo · Capital de trabajo / Ventas |
| **Endeudamiento** | Deuda total / Activos · Pasivos / Patrimonio · Deuda financiera / Patrimonio · Deuda financiera / (Deuda + Patrimonio) · Deuda neta · Multiplicador de apalancamiento (Activos / Patrimonio) |
| **Solvencia** | Cobertura de intereses (EBIT / Gastos financieros) · Cobertura con EBITDA · Deuda neta / EBITDA · Deuda / EBITDA · FCO / Deuda (o "No disponible") · Perfil de vencimientos (nota si no disponible) |
| **Eficiencia (actividad)** | Rotación y días de inventario (DIO) · Rotación y días de cartera (DSO) · Días de proveedores (DPO) · Ciclo de conversión de efectivo (CCC = DIO + DSO − DPO) · Rotación de activos · Rotación de activo fijo |
| **Rentabilidad** | Margen bruto · Margen operativo (EBIT) · Margen EBITDA · Margen neto · ROA · ROE (sobre patrimonio **atribuible**) · ROIC (NOPAT / capital invertido) |
| **DuPont (3 y 5 factores)** | ROE = Margen neto × Rotación de activos × Apalancamiento — y verifica que el producto reproduzca el ROE ya calculado (chequeo de consistencia, fila aparte con la diferencia). Añade la versión de 5 factores (carga fiscal × carga de intereses × margen EBIT × rotación × apalancamiento) si el archivo trae EBT y EBIT por separado. |
| **Calidad del balance** | Goodwill / Activos · Intangibles / Patrimonio · Impuesto diferido neto / Patrimonio · Provisiones / Pasivos · Activo corriente sin caja / Pasivo corriente · (pasivos contingentes: nota si no disponible) |
| **Caja** | FCO / Utilidad neta · FCO / EBITDA (conversión de caja) · FCL / Ventas — **marca "No disponible" si no hay Estado de Flujo de Efectivo**; no lo estimes con proxies sin decirlo. |

### Promedios vs. saldo de cierre

Los ratios que mezclan una cuenta de flujo (Resultados) con una de saldo (Balance) — ROA, ROE, rotaciones — se calculan idealmente con el **saldo promedio** `(inicio + fin)/2`. Como el primer año de la serie no tiene saldo inicial:
- Ofrece las dos versiones o usa **saldo de cierre** de forma consistente en toda la hoja (es lo que hicimos con Tecnoglass) y **anótalo** en la fila de metodología de la hoja.
- Si usas promedios, el primer año va marcado `"n/d"` (no fuerces a usar solo el saldo de cierre en un año y promedio en el resto).

### EBITDA cuando la empresa no lo reporta

Si el estado de resultados no trae EBITDA ni una línea de D&A:
**D&A estimado = Δ Depreciación acumulada del balance** (año actual − anterior, en valor absoluto) y **EBITDA estimado = EBIT + D&A estimado**. Etiqueta SIEMPRE la fila como "[proxy]"; el primer año va `"n/d"`.
Si el archivo (como el de Tecnoglass) **sí trae EBITDA reportado**, úsalo y calcula la D&A implícita como `EBITDA − EBIT` (fila memo).

### Semáforos vs. mapa de calor

- **Semáforo rojo/ámbar/verde** (`CellIsRule`): solo donde hay un umbral de referencia razonable (tabla abajo).
- **Mapa de calor de tendencia** (`ColorScaleRule`): para el resto (rotaciones, márgenes históricos, días de ciclo).
- El **ROE** (indicador más importante del tablero) lleva **doble tratamiento**: mapa de calor de tendencia **y** semáforo de nivel absoluto.

Umbrales de referencia por defecto — **calíbralos al sector antes de reutilizarlos** (`references/ratios_catalogo.md` trae variantes por sector):

| Indicador | Verde | Ámbar | Rojo |
|---|---|---|---|
| Razón corriente | ≥ 1.5x | 1.0x–1.5x | < 1.0x |
| Prueba ácida | ≥ 1.0x | 0.7x–1.0x | < 0.7x |
| Razón de efectivo | ≥ 0.5x | 0.2x–0.5x | < 0.2x |
| Deuda total / Activos | < 50% | 50%–65% | > 65% |
| Pasivos / Patrimonio | < 1.0x | 1.0x–2.0x | > 2.0x |
| Deuda financiera / Patrimonio | < 0.5x | 0.5x–1.0x | > 1.0x |
| Deuda neta / EBITDA | < 1.5x | 1.5x–3.0x | > 3.0x |
| Cobertura de intereses | > 6x | 3x–6x | < 3x |
| Margen neto | > 10% | 3%–10% | < 3% |
| ROA | > 6% | 2%–6% | < 2% |
| ROE | > 15% | 8%–15% | < 8% |
| Goodwill / Activos | < 5% | 5%–15% | > 15% |
| CCC (ciclo de caja) | < 60 días | 60–120 días | > 120 días |

## Paso 4 — Hoja / fila de metodología

Si el libro **ya tiene** hoja `Metodologia` (porque se corrió `VerticalAnalysis`), **añade un bloque** al final: qué estándar guía los ratios (CFA Financial Analysis Techniques), si se usó saldo de cierre o promedio, qué ratios quedaron "No disponible" y por qué (falta flujo de caja / notas), y una conclusión de 2-3 líneas con la lectura principal del tablero.
Si el libro **no tiene** hoja de metodología, créala como primera hoja (ver `VerticalAnalysis` Paso 6).

## Paso 5 — Formato, fórmulas y verificación (obligatorio)

- **Match de convenciones**: lee `cell.font.name` y `cell.number_format` de una celda de la hoja fuente y reutilízalos. Formatos: ratios `0.00"x"`, porcentajes `0.0%;(0.0%);"-"`, días `0" días"`, montos con el formato de la hoja fuente.
- **Fórmulas reales, nunca valores pegados.** Cada celda de ratio referencia la hoja fuente.
- **Blindaje**: `=IFERROR(IF(AND(ISNUMBER(a),ISNUMBER(b),b<>0), a/b, "n/d"), "n/d")`.
- **Chequeo de consistencia DuPont**: fila con `ROE(directo) − ROE(DuPont)` — debe dar ~0 en todos los años. Si no, hay un error de mapeo de filas.
- **Recalcular**: `recalc.py` de la skill `xlsx` falla en Windows (`socket has no attribute AF_UNIX`). Usa `scripts/recalc_excel_windows.py` de esta carpeta (Excel COM vía `pywin32`). Después vuelve a abrir con `openpyxl(data_only=True)` y confirma que **ninguna celda sea un string que empiece por `#`**.
- **Verificación cruzada**: ROA ≈ Margen neto × Rotación de activos; Cobertura de intereses > 1 si la empresa es rentable; Deuda neta negativa ⇒ caja neta (no es error).
- **Revisión visual**: exporta 2-3 rangos con `scripts/export_preview_excel.py` y léelos como imagen antes de entregar (columnas sin `#####`, semáforos visibles).
- Ancho de columna A ≈ 60; columnas de año ≈ 15-17.

## Scripts de referencia

`scripts/` trae el código de la sesión de Tecnoglass. **No es un motor genérico**: el diccionario `ROWS` al inicio de `build_ratios.py` tiene los números de fila del layout de `Data - TGLS.xlsx`. En cada sesión nueva: abre el Excel del usuario, reconstruye `ROWS` fila por fila, y corre el script.

- `build_ratios.py` — genera la hoja `Indicadores` con las 8 categorías, DuPont (3 y 5 factores), semáforos y mapas de calor. Parametrizado por el dict `ROWS` y los nombres de las hojas fuente.
- `recalc_excel_windows.py` — recalcula un `.xlsx` vía Excel COM.
- `export_preview_excel.py` — exporta un rango como PNG para revisión visual.

## Notas y advertencias

- **Nunca fabriques cifras** que el archivo no trae (flujo de caja, D&A oficial, vencimientos de deuda, pasivos contingentes). Márcalas "No disponible" y sugiere la fuente primaria (SEC EDGAR 10-K, SIMEV/Superfinanciera, Supersociedades, IR de la empresa).
- **Patrimonio para el ROE = patrimonio atribuible a la controladora** (patrimonio total − interés minoritario). Si el archivo no separa el interés minoritario, usa el total y anótalo.
- **Deuda financiera ≠ pasivo total.** La deuda financiera es deuda con costo (bonos, préstamos, leasing); no incluye cuentas por pagar ni ingresos diferidos.
- Si el archivo viene de un agregador (Investing.com, Bloomberg), recuérdalo y sugiere contrastar contra la fuente primaria antes de usar los ratios para una decisión real.
- Cierra siempre con la aclaración de que es material informativo/educativo, no asesoría de inversión.
