## Arquitectura AI-First — detalle por componente

[← Volver al inicio](index.md) · [Roadmap](roadmap.md) · [Datos](datos.md)

El orden de lectura es el orden de dependencia: primero el modelo (qué queremos que aprenda),
luego lo que lo alimenta, luego lo que lo sirve, y por último lo que lo vigila.

---

## 1 · Modelos (el núcleo)

### 1.1 EDA — exploración

Caracterización del universo (S&P 500 + Russell 2000 + micro cap), de la cobertura sectorial y
temporal, y de la calidad de las etiquetas de rating y de quiebra. Define el panel de
entrenamiento y las particiones temporales. Resultados en [Datos](datos.md).

### 1.2 Modelos *benchmark*

Líneas base contra las cuales se mide todo lo demás. Ninguna usa texto:

| Nivel | Modelo | Entradas |
|---|---|---|
| Benchmark 0 | Reglas: Altman Z / Z' / Z'' y umbrales de ratios por familia | Solo ratios |
| Benchmark 1 | Regresión logística / ordinal | Ratios estandarizados por sector |
| Benchmark 2 | *Gradient boosting* (LightGBM / XGBoost) | Ratios + variaciones año a año |

El objetivo es un desempeño **honesto y reproducible**: F1 macro, PR-AUC y curva de calibración,
con validación fuera de tiempo (entrenar ≤ 2014, probar 2015–2016).

### 1.3 *Fine-tuning*

Ajuste de un modelo de lenguaje financiero (FinBERT) al dominio concreto: secciones de *Risk
Factors* y *MD&A* de los 10-K, notas a los estados financieros y titulares de noticias. Produce
*embeddings* y puntajes de tono adaptados, no genéricos.

### 1.4 FinTarget-Model (FTM)

El modelo multimodal propio. **Fusión tardía**: se calcula por separado el vector de ratios y el
vector de texto (embedding + sentimiento + dinámica + divergencia), se concatenan y se alimentan
a un único modelo (LightGBM con fusión tardía, o un *transformer* tabular tipo FT-Transformer /
TabNet que recibe los ratios como campos y los *embeddings* como características adicionales).

**Salidas:**
- Clasificación de la **trayectoria del perfil de ratios** a cuatro trimestres: `{mejora, estable, deterioro}`.
- **Rating estimado** / grado de inversión y **probabilidad de estrés financiero**.
- Explicabilidad **SHAP** global (qué características dominan) y local (por qué esta empresa).
- La métrica de **divergencia narrativa–fundamentales**: cuándo el discurso va por delante de los números.

**Resultado principal del proyecto:** el estudio de ablación que aísla el aporte marginal de cada
capa —(a) solo ratios, (b) + MD&A, (c) + Risk Factors y su dinámica, (d) + noticias, (e) +
divergencia—, con intervalos por *bootstrap*. Ese número —positivo o nulo— es en sí un hallazgo.

### 1.5 Compañías estudiadas

Casos de validación fuera de muestra. Cada uno produce una ficha con la predicción, los factores
que la explican y la lectura de narrativa frente a fundamentales.

- **VISA** — *large cap*, EE. UU. Ancla de los *golden tests*: razón corriente 2025 = 1,08x;
  ROIC = 47,5 %; beta de regresión = 0,76; WACC de mercado = 7,9 %; EVA = +18.535 US$ MM.
- **Tecnoglass (TGLS)** — *small cap*, ADR. Prueba de robustez frente a fuentes con
  inconsistencias; reconciliación contra SEC EDGAR.
- **Ecopetrol** — emisor LatAm con control estatal. Prima de riesgo país y fuentes locales
  (Superfinanciera, BVC), como exige un emisor colombiano.

---

## 2 · Plugins FinTech (la fábrica de datos estructurados)

Seis *skills* ya en funcionamiento, creadas y probadas en análisis reales. Son la **fuente del
material estructurado que consume el NLP Model** y la capa de entrega al analista.

| Skill | Qué entrega | Tipo |
|---|---|---|
| `IncAnalyze` | Investigación profunda de una empresa (SEC EDGAR, Yahoo, BVC) → informe + gráficas | Escrito |
| `DailyReport` | Reporte semanal de mercado (Forex Factory, Desayuno Bancolombia, Russell 2000) | Escrito |
| `VerticalAnalysis` | Análisis vertical / horizontal / DuPont dentro del Excel, con fórmulas reales | Numérico |
| `RatioAnalysis` | Hoja de indicadores por familia con semáforos y umbrales por sector | Numérico |
| `MarketRatios` | Tablero de múltiplos de mercado + pestaña "Fuentes" celda a celda | Numérico |
| `WaccModel` | WACC / CAPM (regresión y *bottom-up*) / EVA a nivel banca de inversión | Numérico |

Un comando orquestador —`/fintarget-dossier <empresa>`— corre `IncAnalyze` (lo escrito),
construye el Excel base, aplica `VerticalAnalysis` + `RatioAnalysis` + `MarketRatios` +
`WaccModel` (lo numérico) y, si está disponible, anexa el *score* del FTM. El resultado es un
**dossier único por empresa**. Empaquetadas como *plugin* en [`/plugin`](https://github.com/Hyper-Target/FinTarget/tree/main/plugin).

---

## 3 · NLP Model (la capa de lenguaje)

- **Ingesta y parseo.** 10-K por ítem (Item 1A *Risk Factors*, Item 7 *MD&A*) del corpus
  EDGAR-CORPUS (1993–2020) y de un *parser* propio para 2021–2025; notas a los estados
  financieros para empresas privadas; flujo de noticias en ventana de 7 días antes de cada corte.
- ***Features* de texto.** *Embeddings* FinBERT del Item 1A y del Item 7; proporción de términos
  negativos, positivos, de incertidumbre y de litigio del léxico de Loughran–McDonald; Δtono y
  Δlongitud año a año; similitud del texto respecto al año previo (un cambio grande es señal —
  efecto *"Lazy Prices"*).
- **Métrica de divergencia.** `D = (tono de la narrativa, estandarizado) − (score de salud
  fundamental, estandarizado)`. Un valor positivo alto: *"el discurso es más optimista que los
  números"*; uno negativo: *"los números son mejores de lo que sugiere el tono"*.

---

## 4 · Backend

API en Python (FastAPI) que sirve el FTM entrenado. Contrato mínimo:

```
POST /score
  { "identificador": "V" | "0001403161", "modo": "listed" | "private" }
→ { "rating_estimado": "AA-", "prob_grado_inversion": 0.94,
    "prob_estres_12m": 0.03, "trayectoria_ratios": "estable",
    "shap_top": [...], "divergencia": -0.4, "ficha_url": "..." }
```

Cachea los *companyfacts* de SEC EDGAR y los *embeddings* de texto; registra cada llamada para
trazabilidad y para monitoreo de *drift*.

---

## 5 · Frontend

El tablero para el analista y la junta, heredero directo del tablero interactivo de VISA
(cinco vistas: resumen, análisis vertical, horizontal, ratios, costo de capital). Añade:

- **Ficha por empresa**: predicción, factores SHAP, narrativa vs. fundamentales.
- **Comparables**: la empresa frente a la distribución de pares del mismo sector y tamaño.
- **Explicabilidad interactiva**: pasar el cursor sobre un indicador muestra su definición, su
  fórmula y su fuente. Autocontenido, se abre en cualquier navegador y se comparte por enlace.

---

## 6 · Orquestación y observabilidad

Tablero tipo **Dagster** para supervisar todo el flujo como un conjunto de DAGs con estado
visible:

| DAG | Qué hace | Frecuencia |
|---|---|---|
| `ingest_edgar` | Descarga incremental de *companyfacts* y de 10-K nuevos | Diaria |
| `ingest_news` | Recolección y filtrado del flujo de noticias por entidad | Diaria |
| `build_features` | Ratios (`finmetrics.py`), *features* de texto, divergencia; *joins* point-in-time | Por corte |
| `train_ftm` | Reentrenamiento y estudio de ablación; registro en MLflow | Mensual / bajo demanda |
| `score_universe` | *Scoring* del universo y actualización de fichas | Semanal |
| `monitor_drift` | *Drift* de características entre el período de entrenamiento y el de aplicación; frescura y completitud de los datos | Diaria |

Cada DAG expone su última ejecución, su estado y sus métricas. Es la diferencia entre un
*notebook* que corrió una vez y un sistema del que se puede responder *"¿está bien hoy?"*.
