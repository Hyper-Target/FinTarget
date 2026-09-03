---
name: IncAnalyze
description: Investigación financiera profunda de una empresa específica que el usuario nombre (pública o privada, EE. UU., Colombia o LatAm). Consulta las bases de datos financieras más importantes (SEC EDGAR/XBRL, Yahoo Finance, BVC/Superfinanciera, stockanalysis.com, macrotrends, IR de la empresa) y entrega un informe Markdown tremendamente detallado con estados financieros históricos, rentabilidad, apalancamiento, valoración, comparables y gráficas. Úsalo cuando el usuario pida "analiza la empresa X", "dame el perfil financiero de X", "investiga a fondo X" o invoque explícitamente FinTech:IncAnalyze.
---

# IncAnalyze (FinTech)

Skill hermana de [DailyReport](../DailyReport/SKILL.md). Mientras `DailyReport` cubre el pulso diario/semanal del mercado, `IncAnalyze` hace **investigación profunda y estructurada de una sola empresa** a partir de las bases de datos financieras primarias, no de resúmenes de terceros.

## Cuándo usarla

- El usuario nombra una empresa concreta y pide análisis, perfil, "due diligence", o "todo lo que puedas encontrar" sobre ella.
- El usuario invoca explícitamente `FinTech:IncAnalyze`.
- Si el usuario no da ticker/bolsa, pregunta o infiere razonablemente (p. ej. "Ecopetrol" → ECOPETROL.CN / EC en NYSE; "Nvidia" → NVDA en Nasdaq).

## Perfil del usuario (asumir siempre)

Científico de Datos en Finanzas — Maestría en Finanzas, Uninorte. Le interesa el detalle numérico real (series históricas, no solo el último dato), la trazabilidad de cada cifra a su fuente, y visualizaciones. Todo el entregable en **español**, formato **Markdown**, **con gráficas obligatorias** generadas con Python/matplotlib.

## Paso 1 — Identificar la empresa y dónde reporta

Determina:
1. ¿Cotiza en bolsa o es privada?
2. Si cotiza: ¿en qué mercado? (EE. UU. / NYSE-Nasdaq, Colombia / BVC, MGC, ADR, u otra bolsa LatAm).
3. Ticker(s) y, si aplica, CIK de SEC EDGAR (ver Paso 2a).

Si la empresa es privada o no reportante, dilo explícitamente desde el inicio y ajusta expectativas: el informe se construirá con fuentes secundarias (prensa, informes sectoriales, Cámara de Comercio/registro mercantil si es colombiana) y tendrá huecos que hay que señalar, no rellenar con inferencias no soportadas.

## Paso 2 — Bases de datos a consultar (las más importantes primero)

### 2a. SEC EDGAR / XBRL — la fuente primaria para emisores de EE. UU. (o ADRs que reportan 20-F)

Esta es la base de datos más confiable porque son los estados financieros auditados que la empresa reporta por ley, en formato estructurado:

1. Mapeo ticker → CIK: `https://www.sec.gov/files/company_tickers.json` (archivo estático, sin necesidad de scraping).
2. Todos los hechos financieros reportados en XBRL, en JSON estructurado (ingresos, EBIT, activos, pasivos, patrimonio, flujo de caja, por cada periodo/filing):
   `https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK de 10 dígitos con ceros a la izquierda}.json`
   — de aquí se puede reconstruir una **serie histórica multi-año** de `Revenues`, `NetIncomeLoss`, `OperatingIncomeLoss`, `Assets`, `Liabilities`, `StockholdersEquity`, `CashAndCashEquivalentsAtCarryingValue`, etc., sin depender de scraping de HTML.
3. Filings completos (10-K anual, 10-Q trimestral, 8-K hechos relevantes, DEF 14A gobierno corporativo/compensación):
   `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={CIK}&type=10-K`
4. **Importante:** SEC pide un User-Agent identificable con contacto (p. ej. `"NombreApp contacto@correo.com"`) en las peticiones a sus APIs. Si `WebFetch` no permite fijar headers, usa el navegador (Claude_Browser/claude-in-chrome), que ya envía su propio User-Agent válido.
5. El **Item 1A (Risk Factors)** y el **MD&A (Management's Discussion & Analysis)** del 10-K son las mejores fuentes cualitativas de riesgos y contexto de gestión — léelos, no los resumas de memoria.

### 2b. Yahoo Finance — cotización, ratios de mercado y consenso de analistas

- `https://finance.yahoo.com/quote/{TICKER}/` (Summary): precio, rango 52 semanas, market cap, beta.
- `.../key-statistics`: múltiplos (P/E, P/B, EV/EBITDA, PEG), márgenes, ROE/ROA ya calculados por Yahoo (útil para contrastar tu propio cálculo).
- `.../financials`, `.../balance-sheet`, `.../cash-flow`: estados financieros de los últimos periodos.
- `.../analysis`: estimados de consenso de analistas (crecimiento esperado, precio objetivo).
- Nota técnica (ya validada en la skill DailyReport): la página es pesada en JS; para la cotización del encabezado usa `document.querySelector('[data-testid="quote-hdr"]').innerText` vía `javascript_tool`, no `get_page_text` a secas.

### 2c. stockanalysis.com y macrotrends.net — series históricas limpias sin login

- `https://stockanalysis.com/stocks/{TICKER}/financials/` — estado de resultados, balance y flujo de caja de 5-10 años en una sola tabla, ya estandarizados.
- `https://www.macrotrends.net/stocks/charts/{TICKER}/{nombre}/revenue` (y equivalentes para net-income, ebitda, roe, roic, etc.) — excelente para gráficas de tendencia de largo plazo y para verificar cruzado las cifras de SEC EDGAR.

### 2d. Empresas colombianas / LatAm

- **BVC** (`https://www.bvc.com.co`): hechos relevantes, informes de emisores, calendario de pagos/dividendos.
- **Superintendencia Financiera de Colombia** (`https://www.superfinanciera.gov.co`): estados financieros reportados por el emisor bajo supervisión (NIIF), informes de gobierno corporativo.
- **Informes de Bancolombia/Grupo Cibest** ya disponibles localmente en la carpeta `Reportes/` del usuario (p. ej. los PDF "Desayuno con Bancolombia") — revísalos primero por si ya traen cifras, múltiplos o estrategia de largo plazo (Sobreponderar/Neutral/Subponderar) sobre la empresa pedida, antes de salir a buscar en internet.
- Investor Relations de la propia empresa (ej. `investors.ecopetrol.com.co`) para el informe anual/reporte integrado.

### 2e. Contexto cualitativo y de mercado

- Noticias recientes: búsqueda web (`WebSearch`) acotada a los últimos 3-6 meses — earnings calls, guidance, M&A, cambios de management, litigios.
- Página oficial de relación con inversionistas para presentaciones a inversionistas (*investor decks*) — suelen resumir la tesis de inversión mejor que cualquier tercero.

## Paso 3 — Construir las métricas (no te quedes en el último dato)

Con lo recolectado en el Paso 2, arma series de al menos **3-5 años** (o los que existan) para:

- Ingresos, crecimiento y/o (CAGR)
- Utilidad Bruta, EBITDA, EBIT, Utilidad Neta y sus márgenes (%)
- ROE, ROA, ROIC — y su **descomposición DuPont** (Margen Neto × Rotación de Activos × Apalancamiento)
- Deuda Neta / EBITDA, Cobertura de intereses, Deuda/Patrimonio
- Capital de trabajo, razón corriente, prueba ácida, **Ciclo de Conversión de Efectivo** (DIO + DSO − DPO)
- Flujo de Caja Libre (FCF = FCO − Capex) y conversión de EBITDA a caja
- Múltiplos actuales (P/E, EV/EBITDA, P/B) vs. su propio promedio histórico y vs. 3-5 comparables del mismo sector

Si un dato no está disponible en ninguna fuente consultada, dilo explícitamente ("no reportado" / "no aplica" / "no encontrado en las fuentes consultadas al [fecha]") — nunca lo inventes ni lo interpoles silenciosamente.

## Paso 4 — Gráficas (obligatorio)

Usa como base `scripts/plantilla_graficas_empresa.py` en esta misma carpeta de skill: funciones ya parametrizadas (reutilizadas de la sesión de referencia del 22-ago-2026) para:

1. `grafico_cascada_rentabilidad(...)` — cascada Ingresos → COGS → Utilidad Bruta → Opex → **EBITDA** → D&A → EBIT → Intereses → EBT → Impuestos → Utilidad Neta, con las cifras **reales** de la empresa del año más reciente disponible.
2. `grafico_dupont(...)` — descomposición del ROE con las cifras reales.
3. `grafico_evolucion_historica(...)` — serie de tiempo (barras o líneas) de Ingresos/EBITDA/Margen a través de los años disponibles.
4. `grafico_multiplos_peers(...)` — la empresa vs. 3-5 comparables en P/E, EV/EBITDA y P/B (mismo patrón que la gráfica de múltiplos ya construida para el COLCAP).
5. Si hay serie de precios: evolución del precio con medias móviles (reutiliza el estilo de `graficos/generar_graficas.py` de la skill DailyReport).

Verifica siempre los PNG generados (leerlos como imagen) antes de darlos por buenos: títulos cortados, etiquetas solapadas, escalas ilegibles.

## Paso 5 — Estructura del entregable

Archivo `Analisis_{NombreEmpresa}_{fecha}.md` en la carpeta de Reportes del usuario, con esta estructura mínima:

1. **Resumen ejecutivo** (5-8 bullets con lo más importante)
2. **Descripción del negocio** (qué hace, segmentos, geografías, posición competitiva)
3. **Análisis financiero histórico** (tablas + gráficas del Paso 3-4)
4. **Rentabilidad y eficiencia** (DuPont, márgenes)
5. **Estructura de capital y liquidez** (apalancamiento, cobertura, capital de trabajo, CCC)
6. **Valoración** (múltiplos actuales vs. histórico propio vs. peers; precio objetivo/consenso si existe)
7. **Mercado accionario** (si cotiza: performance de la acción, dividendos, volumen, propiedad accionaria relevante)
8. **Riesgos** (extraídos del Item 1A del 10-K o equivalente, no genéricos)
9. **Noticias y eventos recientes** (últimos 3-6 meses, con fecha de cada noticia)
10. **Fuentes consultadas** (URL exacta + fecha/hora de consulta de cada una — trazabilidad total)

Cierra siempre con la aclaración de que es material informativo/educativo, no asesoría de inversión.

## Notas y advertencias

- Prioriza SIEMPRE la fuente primaria (SEC EDGAR / estados financieros reportados a Superfinanciera) sobre agregadores de terceros cuando haya discrepancia; si hay discrepancia entre fuentes, repórtala explícitamente en vez de promediarla o esconderla.
- No fabriques cifras no reportadas, ni "rellenes" años faltantes con interpolación sin decirlo.
- Respeta el mismo estándar de la skill DailyReport: fecha/hora de consulta explícita en cada dato de mercado en vivo; si una fuente no carga, dilo y ofrece una alternativa en vez de inventar.
- Para empresas colombianas ya cubiertas en los informes "Desayuno con Bancolombia" que el usuario guarda localmente, cruza esas cifras (múltiplos, técnicos, estrategia de largo plazo) con lo que encuentres en fuentes públicas — es información valiosa que ya está en su carpeta y no requiere ir a internet.
