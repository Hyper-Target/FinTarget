# FinTarget

**Diagnóstico financiero reproducible y explicable para cualquier empresa — cotice o no en bolsa.**

FinTarget es un flujo de trabajo de datos parametrizado por empresa que produce, con un comando y de forma auditable,
el mismo diagnóstico que hoy se arma a mano en Excel: análisis vertical y horizontal, tablero de ratios por
familia, descomposición DuPont, costo de capital (WACC) y valor económico agregado (EVA), clasificación de
riesgo (rating estimado / probabilidad de estrés) y una lectura de la narrativa corporativa frente a los
fundamentales. Cada cifra es trazable a su fuente; cada predicción viene con su explicación (SHAP).

No es una terminal de datos ni un servicio de asesoría de inversión. Es el **componente cuantitativo abierto**
de un diagnóstico financiero profesional: una alternativa reproducible al trabajo manual, pensada para
sustentarse ante un comité, una junta o un cliente.

📄 **Sitio del proyecto (descripción completa, arquitectura y datos):** <https://hyper-target.github.io/FinTarget/>

Primer proyecto de **HyperTarget**, una iniciativa de **código abierto** para resolver problemas
reales de la industria financiera con herramientas públicas, gratuitas y auditables.

---

## Para qué sirve

| Caso de uso | Qué entrega FinTarget |
|---|---|
| Entender una empresa nueva antes de una reunión o un comité | Ficha ejecutiva + tablero de ratios + WACC/EVA en horas, no días |
| Due diligence / evaluación de contraparte | Rating estimado, grado de inversión y probabilidad de estrés, con los factores que más pesan |
| Seguimiento de un portafolio de empresas | Panel que marca deterioros de liquidez, cobertura, apalancamiento y márgenes antes del cierre anual |
| Preparar una reunión sobre una empresa con mucha documentación | Resumen de lo relevante del 10-K / informe de gestión y de los cambios año a año en los factores de riesgo |
| Empresas que no cotizan | El mismo diagnóstico con datos de Supersociedades / notas a los estados, beta *bottom-up* y Altman Z'/Z'' |

## Arquitectura

```
INGESTA
  SEC EDGAR (XBRL)        EDGAR-CORPUS + parser 10-K       Noticias (ventana 7 días)
        |                          |                              |
        v                          v                              v
   [ RATIOS ]                [ TEXTO 10-K ]                 [ NOTICIAS ]
   finmetrics.py             Item 1A / Item 7              volumen / sentimiento / eventos
        |                          |                              |
        |                    FinBERT: embeddings + tono            |
        |                          |                              |
        |        --> divergencia narrativa vs. fundamentales <-----+
        |                          |
        +------------+-------------+
                     v
        [ FUSIÓN: concatenación de vectores ]
                     v
        [ MODELO: LightGBM  /  FT-Transformer ]
                     v
   Rating / trayectoria de ratios  +  explicabilidad SHAP  -->  ficha por empresa
```

Dos modos sobre el mismo flujo: **cotizada** (SEC EDGAR + mercado) y **privada** (Supersociedades + notas
a los estados). La capa de *features* y el modelo son compartidos.

## Estructura del repositorio

```
fintarget/
  ingest/     edgar.py (companyfacts XBRL) · tenk.py (parser 10-K por ítem) · news.py
              supersociedades.py (PIE / SIREM) · notes.py (notas a los EEFF)
  features/   finmetrics.py (ratios, DuPont, Altman Z/Z'/Z'', WACC, ROIC, EVA)
              text.py (FinBERT: embeddings + tono + dinámica)
              divergence.py (narrativa vs. fundamentales)
  models/     gbm.py · tabular_transformer.py · ablation.py · transfer.py
  explain/    shap_report.py · company_sheet.py
  cli.py      fintarget score --company <id> --mode {listed|private}
data/         raw/ · processed/ (panel) · external/ (datasets públicos, ver data/README.md)
  ingest/     ... · build_universe.py (universo S&P 500 + Russell 2000)
notebooks/    00_eda · 01_panel · 02_text · 03_fusion · 04_case_visa · 05_case_co
tests/        golden tests anclados a los valores del taller VISA
reports/      eda/ (resumen del universo + figuras) · fichas por empresa
plugin/       plugin de Claude Code (FinTech): las 6 skills + el comando de dossier
docs/         sitio del proyecto (GitHub Pages) · viabilidad.md
```

## Estado del proyecto

Fase 0 — cimientos. Ver [`docs/viabilidad.md`](docs/viabilidad.md) para el análisis de qué es factible,
con qué evidencia y con cuánto esfuerzo.

- [x] Propuesta formal (curso Gerencia Financiera, Maestría en Finanzas — Universidad del Norte)
- [x] Datasets públicos localizados y verificados (rating crediticio, EDGAR-CORPUS, SEC EDGAR/XBRL)
- [x] Skills de análisis empaquetadas como plugin de Claude Code (`plugin/`)
- [x] Universo S&P 500 + Russell 2000 construido y primer EDA (`fintarget/ingest/build_universe.py`, `notebooks/00_eda.py`)
- [x] Sitio del proyecto (GitHub Pages) con la descripción completa y los enlaces de datos
- [ ] `finmetrics.py` extraído del modelo VISA + golden tests
- [ ] `ingest/edgar.py` + `cli.py` (validar con VISA, TGLS y Ecopetrol)
- [ ] Panel contable S&P 500 (2010–2025) y tablero de ratios
- [ ] Baseline de rating (LightGBM) + estudio de ablación con la capa de texto

## Origen

FinTarget nace del taller de análisis financiero de VISA Inc. (2021–2025) del curso de Gerencia Financiera.
Ese taller —análisis vertical/horizontal, ratios, WACC y EVA reconstruidos y corregidos— es el caso de
validación y el ancla de los *golden tests* del proyecto.

## Licencia y uso

Material académico y herramienta de trabajo. Los análisis y modelos tienen fines de diagnóstico y de
formación; **no constituyen asesoría de inversión ni una calificación crediticia oficial**. Los datasets
externos conservan su licencia de origen (ver [`data/README.md`](data/README.md)).
