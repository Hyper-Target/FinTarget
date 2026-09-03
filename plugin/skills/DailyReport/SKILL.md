---
name: DailyReport
description: Genera el reporte financiero diario/semanal del usuario (Científico de Datos en Finanzas) a partir de Forex Factory, el último informe "Desayuno con Bancolombia" en PDF y el índice Russell 2000 en Yahoo Finance, con gráficas incluidas. Úsalo cuando el usuario pida su "reporte diario", "resumen de mercado", "novedades financieras de hoy/de la semana" o mencione explícitamente la skill FinTech:DailyReport.
---

# DailyReport (FinTech)

Skill para producir, de forma repetible, el paquete diario/semanal de inteligencia de mercado del usuario: un informe de noticias económicas de EE. UU. (Forex Factory), un análisis/glosario del último informe "Desayuno con Bancolombia" (PDF), y una lectura del Russell 2000 en Yahoo Finance como referencia de *small caps* de EE. UU. — todo en Markdown y con gráficas generadas con Python/matplotlib.

Esta skill nació de una sesión real (22-ago-2026) en la que se construyeron estos tres entregables a mano; documenta ese flujo para no tener que rederivarlo cada vez.

## Cuándo usarla

- El usuario pide su reporte diario/semanal de mercado.
- El usuario pide "novedades de Forex Factory", "qué pasó en Bancolombia hoy/esta semana" o "cómo va el Russell 2000".
- El usuario invoca explícitamente `FinTech:DailyReport`.

## Perfil del usuario (asumir siempre)

Científico de Datos enfocado en Finanzas. Explica los términos financieros con precisión (no los des por sentados), pero puedes usar lenguaje técnico/estadístico sin rodeos (percentiles, desviación estándar, series de tiempo, etc.). Todo el contenido se produce en **español**, en formato **Markdown**, y **debe incluir gráficas** (no solo texto/tablas).

## Flujo de trabajo

### Paso 1 — Forex Factory (calendario económico de EE. UU.)

1. Abre `https://www.forexfactory.com/calendar` (o la semana relevante vía `?week=<mes><día>.<año>`) con el navegador.
2. La tabla de eventos se renderiza vía JS y no siempre es legible con `get_page_text`/`read_page`. El método más confiable es `javascript_tool` leyendo el DOM directamente:
   ```js
   document.querySelectorAll('tr.calendar__row')  // cada fila de evento
   // columnas: .calendar__date .calendar__time .calendar__currency
   //           .calendar__impact span[title]  .calendar__event
   //           .calendar__actual .calendar__forecast .calendar__previous
   ```
   Ten en cuenta que el calendario carga los días de forma progresiva al hacer scroll; si faltan días, haz `window.scrollTo(0, document.body.scrollHeight)` con una pequeña espera antes de releer el DOM, o navega día por día con `?day=aug18.2026`.
3. Filtra por `currency === 'USD'`. Clasifica cada evento por impacto: 🔴 alto, 🟠 medio, 🟡 bajo (atributo `title` del ícono de impacto).
4. Para cada evento con `forecast` disponible, calcula la sorpresa = `actual − forecast` (en las unidades nativas del indicador; no normalices a un solo eje si las unidades no son comparables).
5. Si el usuario pide contexto adicional de otras monedas (CAD, EUR, etc.) para explicar movimientos cruzados, inclúyelo, pero el foco por defecto es USD.

### Paso 2 — "Desayuno con Bancolombia" (PDF)

1. Busca en la carpeta de Reportes del usuario el PDF más reciente cuyo nombre empiece por `Desayuno+con+Bancolombia` (o similar). Si hay varias fechas, usa la más reciente salvo que el usuario pida otra.
2. Léelo completo con la herramienta de lectura de archivos (soporta PDF nativamente). Extrae:
   - Cifras de mercado accionario local e internacional (COLCAP, índices Latam/globales, tasas, divisas, materias primas).
   - Tabla de múltiplos de valoración (PVL, RPG, EV/EBITDA) y tabla de técnicos (RSI, medias móviles, Bandas de Bollinger, soportes/resistencias).
   - Dividendos propuestos/aprobados si el usuario pide ese detalle.
3. Si el usuario pide un **glosario**, recorre el documento sección por sección y explica cada sigla/término encontrado (no solo una lista genérica de finanzas) — agrupa por temática: índices, MGC/ETFs, múltiplos, análisis técnico, renta fija/divisas, materias primas, dividendos, estrategias de inversión. Conecta cada definición con el dato real del informe cuando sea posible (más útil que una definición de diccionario aislada).
4. Respeta las condiciones de uso del informe: es material informativo, no asesoría de inversión — mantén esa aclaración en el entregable final.

### Paso 3 — Yahoo Finance: Russell 2000 (y contexto de mercado)

1. Abre `https://finance.yahoo.com/quote/%5ERUT/` (el símbolo del Russell 2000 es `^RUT`, va URL-encoded como `%5ERUT`).
2. `fin-streamer` genérico puede traer datos mezclados de otros tickers de la página; para el precio/variación del encabezado principal, lee específicamente:
   ```js
   document.querySelector('[data-testid="quote-hdr"]').innerText
   ```
3. Extrae también, de la sección "Summary" (`get_page_text`): Previous Close, Open, Day's Range, 52 Week Range.
4. Para contexto de mercado más amplio (Dow, S&P 500, Nasdaq, VIX, UST 10Y ^TNX), la sección "Trending Indices" / "People Also Watch" de la misma página trae esos datos sin necesidad de navegar a cada ticker por separado.
5. Relaciona el movimiento del Russell 2000 con lo encontrado en Forex Factory (p. ej., reacción a minutas del FOMC, datos de empleo/manufactura) y, si aplica, con el informe de Bancolombia (tasas TES, USD/COP) para dar una lectura cruzada, no tres bloques desconectados.

### Paso 4 — Gráficas (obligatorio)

Genera las gráficas con Python + matplotlib (backend `Agg`), guardadas como PNG en una subcarpeta `graficos/` junto a los `.md` finales, y **embébelas en los Markdown** con `![alt](graficos/archivo.png)`. Verifica los PNG con la herramienta de lectura de imágenes antes de darlos por buenos (títulos cortados, solapamientos, etc.).

Gráficas mínimas recomendadas (usa `scripts/plantilla_graficas.py` en esta misma carpeta de skill como punto de partida — mismo estilo de colores y layout ya validado):

1. **Sorpresas económicas USD de la semana**: barras horizontales divergentes (verde = superó el consenso, rojo = por debajo), una fila por indicador, con nota al pie aclarando qué indicadores "más alto no es necesariamente mejor" (p. ej. Unemployment Claims, inventarios de crudo).
2. **Reacción de mercado del día/semana**: barras de variación % (Dow, S&P 500, Nasdaq, Russell 2000, VIX, UST 10Y).
3. **Múltiplos de valoración**: paneles PVL y RPG (o EV/EBITDA) por emisor, usando los datos reales de la tabla de múltiplos del PDF de Bancolombia.
4. **Análisis técnico ilustrativo**: medias móviles + Bandas de Bollinger + RSI sobre una serie sintética (déjalo explícito en el pie: "datos sintéticos con fines pedagógicos"), útil para explicar visualmente esos conceptos del glosario.

Si no hay matplotlib instalado, instálalo primero (`pip install matplotlib numpy`) — ya se validó que funciona en este entorno.

### Paso 5 — Entregables

Por defecto, produce **dos archivos Markdown** en la carpeta de Reportes del usuario (mismo patrón de nombres que la corrida de referencia):

- `Informe_Forex_Factory_USD_Semana_<rango-fechas>.md` — resumen ejecutivo, gráfica de sorpresas, tabla detallada de eventos, reacción de mercado (incluye Russell 2000), lectura hacia la semana siguiente.
- `Glosario_Financiero_Desayuno_Bancolombia_<fecha>.md` — glosario agrupado por secciones con las gráficas de múltiplos y análisis técnico, más un anexo con las cifras clave del informe.

Si el usuario pide "un solo reporte diario" en vez de dos documentos separados, combina ambos en un único Markdown con secciones claras, sin perder ninguna de las gráficas ni el detalle de eventos/glosario.

## Notas y advertencias

- Todos los datos son de mercado en tiempo real/casi real: dilos con fecha y hora de consulta explícitas, y aclara que es información, no asesoría de inversión.
- Si Forex Factory o Yahoo Finance no cargan (extensión de navegador desconectada, timeout), dilo explícitamente en vez de inventar cifras; ofrece reintentar o usar los datos más recientes disponibles en el PDF de Bancolombia como respaldo parcial.
- No fabriques series de tiempo históricas que el PDF no publica (p. ej. no inventes el detalle diario detrás de una cifra YTD); si necesitas una serie para ilustrar un concepto (como en la gráfica de análisis técnico), dilo explícitamente como dato sintético/ilustrativo.
