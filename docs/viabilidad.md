# FinTarget — análisis de viabilidad

*Preparado para Andrés Saavedra Camerano · Curso de Gerencia Financiera, Maestría en Finanzas (Universidad del Norte) · Septiembre de 2026*

Este documento responde una pregunta concreta: **de todo lo que plantea la propuesta, ¿qué es realmente
factible, con qué evidencia y con cuánto esfuerzo?** El objetivo no es un ejercicio académico sino una
herramienta que sirva en la práctica de asesoría financiera.

---

## 1. Resumen para decisión

| Bloque | Veredicto | Esfuerzo |
|---|---|---|
| **A. Empaquetar los análisis actuales (ratios, WACC, EVA, informes) como una herramienta de un comando** | **Factible ya** | Bajo (días) |
| **B. Ingesta de datos abiertos (SEC EDGAR, EDGAR-CORPUS, datasets de rating)** | **Factible ya — verificado** | Bajo (días) |
| **C. `finmetrics.py` determinista + *golden tests* del taller VISA** | **Factible ya** | Bajo–medio (1–2 semanas) |
| **D. Modelo de rating estimado / grado de inversión + explicabilidad SHAP** | **Factible como *baseline* creíble**, no como motor de rating de producción | Medio (3–5 semanas) |
| **E. Capa de NLP (10-K + noticias) y métrica de divergencia narrativa–fundamentales** | **Factible técnicamente; es la parte de investigación y la de mayor riesgo** | Alto (6–10 semanas) |
| **F. "Alternativa abierta a una terminal de datos de pago"** | **Reformular** — alcance acotado, no equivalencia | — |
| **G. Asesoría / *fair value* / recomendación de inversión** | **Fuera de alcance** (así se declara en la propuesta) | — |

**Recomendación:** entregar el curso con A + B + C + D. Dejar E como el capítulo de investigación (y posible
proyecto de grado), presentado con honestidad sobre lo que puede salir nulo. Ajustar el lenguaje de F.

---

## 2. Lo que ya está verificado (no es promesa, está probado)

### 2.1 Datos contables — SEC EDGAR / XBRL
- API `companyfacts` / `companyconcept` consultada en vivo para VISA (CIK 0001403161): responde con la serie
  histórica completa de ingresos, EBIT, activos, patrimonio, flujo de caja por año fiscal. HTTP 200, JSON
  estructurado, sin *scraping*. Requiere un `User-Agent` con contacto (política de la SEC).
- Cobertura: **todas** las empresas que reportan a la SEC, desde 2009. Dominio público.

### 2.2 Narrativa de los 10-K — EDGAR-CORPUS
- `eloukas/edgar-corpus` en HuggingFace: **no está *gated***, descarga directa por año en formato JSONL,
  10-K ya parseado por ítem (1A Risk Factors, 7 MD&A, etc.). ~220.000 *filings*, 1993–2020.
- Límite real: **termina en 2020**. El período 2021–2025 exige un *parser* propio sobre el índice EDGAR
  (es trabajo acotado y conocido, pero es trabajo).

### 2.3 Etiquetas de rating — datasets públicos
Dos versiones localizadas y perfiladas (mirrors en GitHub, sin necesidad de credenciales de Kaggle):

| Dataset | Filas | Empresas | Período | Features | Etiqueta | Licencia |
|---|---|---|---|---|---|---|
| *Corporate Credit Rating with Financial Ratios* (vía CCRD-Dataset) | 5.403 | 678 (686 CIK) | 2010–2016 | 16 ratios limpios, 0 % faltantes; incluye **CIK** y **SIC** | 22 escalones (AAA…C) + binaria IG/HY (3.368 / 2.035) | CC BY 4.0 (origen Kaggle) |
| *Corporate Credit Rating* (Agewerc/ML-Finance) | 2.029 | 593 | 2014–2016 | 25 ratios | 10 clases (AAA…D) | Kaggle |

**El dato clave:** la primera versión trae el **CIK**. Eso permite unir *ratios ↔ texto del 10-K ↔ XBRL en
vivo* por la misma llave. Es exactamente el puente que la propuesta necesita para el modelo multimodal, y
estaba en duda hasta ahora.

**Limitaciones que hay que decir en voz alta:**
- Solo 2010–2016, y la fecha es **anual** (no día): hay que tratar el riesgo de fuga temporal con cuidado
  (usar el 10-K del año *anterior* al rating).
- Mezcla agencias (S&P, Moody's, Fitch, Egan-Jones). Egan-Jones califica distinto; conviene modelar S&P/Moody's
  y usar el resto como robustez.
- Muy desbalanceado en las colas (AAA = 71 filas, C = 8). Un rating a 22 clases no es realista; a grado de
  inversión (binario) o a 7 grupos (AAA/AA/A/BBB/BB/B/CCC-C) sí.
- VISA **no está** en el dataset de 5.403 → el caso VISA es validación *fuera de muestra* (que es justo lo que
  pide la propuesta): el modelo predice y se contrasta con el rating real AA−.

### 2.4 Bankruptcy / probabilidad de estrés
- *US Company Bankruptcy Prediction* (utkarshx27, CC0): ~78k empresa-año, 1999–2018, 18 variables tipo Altman.
  Disponible en Kaggle; requiere token o mirror. No verificado en esta pasada — pendiente, pero de bajo riesgo.

---

## 3. Empaquetar lo que ya existe: las skills como plugin

Hoy hay **6 skills** de Claude Code funcionando (creadas en sesiones reales del curso):

| Skill | Qué produce | Naturaleza |
|---|---|---|
| `DailyReport` | Reporte semanal de mercado (Forex Factory + Desayuno Bancolombia + Russell 2000) + gráficas | **Escrito** |
| `IncAnalyze` | Investigación profunda de una empresa (SEC EDGAR, Yahoo, BVC…) → informe Markdown + gráficas | **Escrito** (con series numéricas) |
| `VerticalAnalysis` | Análisis vertical / horizontal / DuPont dentro del Excel del usuario, con fórmulas reales | **Numérico** (Excel) |
| `RatioAnalysis` | Hoja "Indicadores" con ratios por familia, fórmulas vinculadas y semáforos | **Numérico** (Excel) |
| `MarketRatios` | Tablero de múltiplos de mercado + pestaña "Fuentes" celda a celda | **Numérico** (Excel) |
| `WaccModel` | Modelo WACC / CAPM (regresión + *bottom-up*) / EVA a nivel banca de inversión | **Numérico** (Excel) |

**Sí es factible y recomendable convertirlo en un plugin.** Un plugin de Claude Code es una carpeta con
`.claude-plugin/plugin.json` + `skills/` (+ opcional `commands/`, `agents/`, MCP). Las 6 skills ya cumplen el
formato. El plugin agrega un **comando orquestador**:

```
/fintarget-dossier <empresa>
  1. IncAnalyze        -> recolecta datos + informe escrito
  2. (construye el Excel base: balance + PyG)
  3. VerticalAnalysis + RatioAnalysis   -> numérico dentro del Excel
  4. MarketRatios       -> múltiplos (si cotiza)
  5. WaccModel          -> WACC + EVA
  6. (opcional) fintarget score --company <CIK>  -> rating estimado + SHAP
  =>  un solo dossier por empresa: lo escrito de 1, lo numérico de 3-5, el modelo de 6
```

Esto es la "capa de entrega al analista". El repo `FinTarget` es la "capa de ciencia de datos" (flujo +
modelos + notebooks). Se conectan por el CLI `fintarget score`. El *scaffold* del plugin está en
[`../plugin/`](../plugin/).

Esfuerzo: el empaquetado en sí es de días. Lo que toma tiempo es el paso 2 (hoy el Excel base se arma a mano
o se exporta de Investing.com) — automatizarlo desde XBRL es parte de `ingest/edgar.py`.

---

## 4. El modelo de ML: qué prometer y qué no

**Factible y defendible:**
- *Baseline* de rating: LightGBM sobre los 16 ratios → grado de inversión (binario) o 7 grupos. Estos problemas
  tabulares pequeños entrenan en minutos; F1 macro y PR-AUC con validación *fuera de tiempo* (entrenar ≤2014,
  probar 2015–2016).
- Explicabilidad: SHAP global y por empresa. Contraste explícito con el caso VISA (predicción vs. AA− real,
  ROIC ≈ 47 %, WACC de mercado ≈ 7,9 %, EVA positivo).
- Reglas Altman Z / Z' / Z'' como *baseline 0* (deterministas, sin entrenamiento).

**No prometer:**
- Un "motor de rating" que compita con una agencia. El dataset es corto (2010–2016), anual y mezcla agencias.
- Precisión por escalón fino (BBB+ vs BBB vs BBB−). No hay datos para eso con rigor.

## 5. La capa de NLP: el capítulo de investigación

Es la contribución original de la propuesta y también la de mayor riesgo:

- **Técnicamente factible:** FinBERT sobre Item 1A / Item 7, léxico Loughran–McDonald, similitud coseno año a
  año (efecto "Lazy Prices"), métrica de divergencia `D = tono narrativo (z) − salud fundamental (z)`.
- **Riesgos reales:**
  1. EDGAR-CORPUS se corta en 2020 → *parser* propio para 2021–2025.
  2. La capa de noticias hoy es semi-manual (el reporte semanal del autor); como *feature* a nivel empresa es
     delgada. Tratarla como experimental, no como señal central.
  3. **El estudio de ablación puede dar que el texto no aporta.** Eso *sigue siendo* un resultado válido y
     publicable — pero el profesor debe saber que ese es un desenlace posible antes de comprometerlo como
     proyecto de grado.

## 6. Ajustes de lenguaje recomendados en la propuesta

| Dice | Debería decir |
|---|---|
| "alternativa abierta a una terminal de datos de pago" | "flujo auditable para un conjunto definido de empresas, con cada dato trazable a su fuente" |
| "para cualquier empresa, cotice o no" | "para empresas que reportan a la SEC (modo cotizada) o a Supersociedades (modo privada); otras jurisdicciones quedan fuera de la Fase 1" |
| "flujo de noticias" como capa central | "capa experimental de noticias; el núcleo son ratios + narrativa del 10-K" |

## 7. Ruta sugerida

| Fase | Entregable | Semanas |
|---|---|---|
| 0 | `finmetrics.py` + golden tests VISA · `ingest/edgar.py` · `cli.py` · repo + CI + plugin publicado | 2–3 |
| 1 | Panel contable (S&P 500, 2010–2016 para entrenar; 2017–2025 para aplicar) · tablero de ratios | 2 |
| 2 | Baseline de rating (LightGBM) + SHAP + validación fuera de tiempo + caso VISA | 2–3 |
| 3 | Capa de texto (EDGAR-CORPUS) + estudio de ablación | 4–6 |
| 4 | Modo privado (un caso anonimizado real) + informe final + *model card* | 2 |

**Para el curso** basta con Fase 0–2. Fase 3–4 es el proyecto de grado.

---

## Anexo — fuentes verificadas en esta pasada

- SEC EDGAR XBRL: `https://data.sec.gov/api/xbrl/companyconcept/CIK0001403161/us-gaap/Revenues.json` → 200 OK
- EDGAR-CORPUS: `https://huggingface.co/api/datasets/eloukas/edgar-corpus` → `gated: false`, 4.261 descargas
- Rating (CCRD): `https://raw.githubusercontent.com/Mengmeara/CCRD-Dataset/main/CCRDataset/raw/ccrd_financial_raw.csv` → 5.403 × 25
- Rating (Agewerc): `https://raw.githubusercontent.com/Agewerc/ML-Finance/master/data/corporate_rating.csv` → 2.029 × 31
