## Qué es FinTarget

**FinTarget es un modelo multimodal para el diagnóstico y la proyección de indicadores
financieros de una empresa.** Toma lo que hoy hace un analista a mano —análisis vertical y
horizontal, tablero de ratios, costo de capital (WACC), EVA, clasificación de riesgo— y lo
convierte en una tubería reproducible que, además de calcular, **aprende**: combina los números
de los estados financieros con la narrativa de los informes corporativos (10-K, notas a los
estados) y con el flujo de noticias, y devuelve una lectura prospectiva con su explicación.

No reemplaza el criterio del analista. Le da un instrumento auditable —cada cifra apunta a su
fuente, cada predicción viene con los factores que la sustentan— utilizable tanto en la
formación como en la práctica de asesoría a empresas, coticen o no en bolsa.

---

## El problema que resuelve

Un ratio financiero describe un **estado**, no una **trayectoria**. El protocolo estándar
—recopilar, calcular, comparar, interpretar— responde *"¿contra qué?"* pero no *"¿hacia
dónde?"*. En la práctica, el deterioro de una empresa suele ser visible en el lenguaje de la
gerencia y en el flujo de noticias **antes** de que los números lo reflejen del todo.

> Ejemplo del propio trabajo del curso: en VISA la razón corriente cae de 1,75x a 1,08x entre
> 2021 y 2025. El tramo final se explica casi por completo por la reclasificación de unos
> US$ 5.569 millones de deuda de largo a corto plazo —un hecho que se comunica y se contextualiza
> en la narrativa del 10-K antes de que el ratio de liquidez lo muestre. Un modelo que solo mira
> el ratio ve una caída; uno que también lee el texto entiende que es contable, no de solvencia.

FinTarget cuantifica formalmente **cuánto aporta la capa de texto** frente a un modelo
puramente contable, mediante un estudio de ablación con validación temporal estricta.

---

## Arquitectura AI-First

El principio de organización: **el modelo es el producto.** La ingesta de datos, los plugins de
análisis, el backend, el frontend y la orquestación existen para *alimentar*, *servir* y
*vigilar* al modelo. Toda decisión de diseño arranca de una pregunta: *¿qué necesita el modelo?*

```
                       ┌───────────────────────────────────────────────┐
                       │            NÚCLEO · MODELOS                    │
   DATOS               │                                               │        SERVICIO
 ─────────             │   EDA → Benchmark → Fine-tuning → FTM          │      ──────────
 SEC EDGAR (XBRL)  ───▶ │                     ▲            │            │ ───▶  Backend (API /score)
 EDGAR-CORPUS 10-K ───▶ │                     │            ▼            │ ───▶  Frontend (tablero
 Flujo de noticias ───▶ │              NLP Model      Casos de validación│        analista / junta)
 Plugins FinTech   ───▶ │            (10-K · notas ·   VISA · TGLS ·     │
 Datasets de rating───▶ │             noticias)       ECOPETROL          │
                       └───────────────────────────────────────────────┘
                                            │
                       ┌────────────────────┴──────────────────────────┐
                       │   ORQUESTACIÓN Y OBSERVABILIDAD (tipo Dagster) │
                       │   pipelines de ingesta · features · entrenamiento ·
                       │   scoring · monitoreo de drift y de frescura   │
                       └───────────────────────────────────────────────┘
```

### Componentes

| # | Componente | Rol respecto al modelo |
|---|---|---|
| 0 | **[Roadmap](roadmap.md)** | El plan de construcción por fases. |
| 1 | **[Modelos](arquitectura.md#1-modelos-el-nucleo)** | El núcleo. EDA → modelos *benchmark* → *fine-tuning* → **FinTarget-Model (FTM)**. Se valida fuera de muestra con VISA, TGLS y Ecopetrol. |
| 2 | **[Plugins FinTech](arquitectura.md#2-plugins-fintech-la-fabrica-de-datos-estructurados)** | La fábrica de datos estructurados que alimenta el NLP: 6 *skills* que producen informes, tableros de ratios y modelos de WACC, todo trazable. |
| 3 | **[NLP Model](arquitectura.md#3-nlp-model-la-capa-de-lenguaje)** | La capa de lenguaje: parseo de 10-K (Item 1A, Item 7) y notas, *embeddings* y tono, y la métrica de divergencia narrativa–fundamentales. |
| 4 | **[Backend](arquitectura.md#4-backend)** | API que sirve el FTM: `POST /score {ticker\|cik, modo}` → rating estimado + probabilidad de estrés + SHAP + ficha. |
| 5 | **[Frontend](arquitectura.md#5-frontend)** | El tablero para el analista y la junta —heredero del tablero de VISA—: ficha por empresa, comparables y explicabilidad interactiva. |
| 6 | **[Orquestación y observabilidad](arquitectura.md#6-orquestacion-y-observabilidad)** | Tablero tipo Dagster: DAGs de ingesta, *features*, entrenamiento y *scoring*, con monitoreo de *drift* y de frescura de datos. |

---

## Casos de validación

El modelo se entrena con empresas de 2010–2016 y se aplica **fuera de ese período** a tres casos
que cubren el espectro relevante para la práctica de asesoría:

| Caso | Perfil | Qué demuestra |
|---|---|---|
| **VISA Inc.** | *Large cap*, EE. UU., rating AA− | El diagnóstico completo sobre una empresa ya analizada en el taller: ROIC ≈ 47 %, WACC de mercado ≈ 7,9 %, EVA positivo y creciente, y el episodio de reclasificación de deuda de 2025. Ancla de los *golden tests*. |
| **Tecnoglass (TGLS)** | *Small cap*, ADR, manufactura | Que el método viaja a empresas pequeñas y a fuentes con inconsistencias (Investing.com subestima ingresos 2021–22 frente al 10-K; se reconcilia contra SEC EDGAR). |
| **Ecopetrol** | Emisor LatAm, control estatal | Que el método incorpora **prima de riesgo país** y datos locales (Superfinanciera / BVC), siguiendo el enfoque del curso. |

---

## Datos

Todo el universo y las etiquetas provienen de **fuentes públicas con licencia abierta**. La lista
completa, con los enlaces directos de descarga y un primer EDA del universo, está en
**[Datos y descarga →](datos.md)**.

En una línea: **6.314** emisores cotizados de EE. UU. (93 % mapeables a SEC EDGAR), segmentados en
tramos de tamaño estilo Russell —**S&P 500 / Russell 1000** para *large cap* y **Russell 2000**
para las empresas pequeñas, que son la mayoría de las que llegan a una junta directiva.

---

## Alcance y naturaleza del proyecto

FinTarget nace del taller de análisis financiero de VISA Inc. del curso de **Gerencia
Financiera** (Maestría en Finanzas, Universidad del Norte) y se concibe como herramienta de
trabajo, con potencial de proyecto de grado.

Es **material académico y un instrumento de diagnóstico**. Los análisis y modelos **no
constituyen asesoría de inversión ni una calificación crediticia oficial**. El detalle de qué es
factible hoy, con qué evidencia y con cuánto esfuerzo está en el
[análisis de viabilidad](https://github.com/Hyper-Target/FinTarget/blob/main/docs/viabilidad.md).
