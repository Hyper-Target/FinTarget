## Qué es FinTarget

**FinTarget es una herramienta que hace el diagnóstico financiero de una empresa —y lo proyecta
hacia adelante— combinando sus números con lo que dicen sus informes.** Toma lo que hoy hace un
analista a mano —análisis vertical y horizontal, tablero de ratios, costo de capital (WACC), EVA,
clasificación de riesgo— y lo convierte en un flujo de trabajo reproducible que, además de
calcular, **aprende de miles de empresas** para anticipar hacia dónde va una compañía. Y no da un
número "porque sí": explica en qué se basó y de dónde salió cada dato.

No reemplaza el criterio del analista. Le da un instrumento **auditable** —cada cifra apunta a su
fuente, cada conclusión viene con los factores que la sustentan— útil tanto en la formación como
en la asesoría a empresas, **coticen o no en bolsa**.

---

## Una iniciativa de código abierto: HyperTarget

FinTarget es el primer proyecto de **HyperTarget**, una iniciativa que construye herramientas de
**código abierto** para resolver problemas reales de la industria financiera.

**"Código abierto"** significa que el proyecto es **público, gratuito y verificable**: cualquiera
puede ver exactamente cómo funciona, revisar de dónde sale cada número y usarlo o adaptarlo. Lo
contrario de una caja negra o de una terminal de datos de pago cuyo cálculo no se puede auditar.
Para un financiero eso se traduce en tres cosas concretas: **no hay licencias costosas**, **nada
está oculto** (todo cálculo se puede señalar y reproducir) y **la herramienta mejora con el
tiempo** en lugar de quedar congelada.

El objetivo de HyperTarget no es un ejercicio académico: es que estas herramientas **sirvan de
verdad** —a un profesor, a un asesor, a una junta directiva, a cualquier tomador de decisiones
financieras—.

---

## En palabras de un financiero (sin tecnicismos)

Si usted dirige un área financiera o asesora empresas, esto es lo que le importa entender —sin una
sola palabra técnica que no le explique aquí mismo.

### El problema de fondo

Cuando llega una empresa a la mesa —un cliente, un proveedor, una contraparte de crédito, una
compañía de la junta— hoy el diagnóstico se arma **a mano en Excel**: se descargan los estados
financieros, se calculan los ratios, se hace el análisis vertical y horizontal, se estima el WACC,
se mira el EVA. Es un trabajo cuidadoso pero **lento, difícil de repetir igual dos veces, y
propenso a errores de copiar y pegar**. Y sobre todo: los ratios le dicen **cómo está** la empresa
hoy, no **hacia dónde va**.

FinTarget hace tres cosas que ese proceso manual no hace:

1. **Lo automatiza.** El mismo diagnóstico completo —vertical, horizontal, ratios, WACC, EVA— sale
   con un comando, siempre en el mismo formato, y con cada número trazable a su fuente. Lo que hoy
   toma días, en horas.
2. **Aprende de la historia de miles de empresas** para estimar el riesgo: qué tan probable es que
   la calificación de crédito de esta empresa sea de "grado de inversión", o qué tan cerca está de
   un estrés financiero. No es una opinión: es un patrón aprendido de miles de casos reales.
3. **Lee los informes, no solo los números.** Un deterioro casi siempre aparece **primero en el
   lenguaje** de la gerencia —en el informe de gestión, en las notas a los estados, en las
   noticias— y solo después en los ratios. FinTarget lee ese lenguaje y avisa cuando el discurso y
   los números no cuadran.

### Lo importante para Colombia: sirve para empresas que NO cotizan en bolsa

La mayoría de las compañías que llegan a una junta directiva en Colombia **no cotizan en bolsa**.
No tienen un precio de acción, ni informes públicos trimestrales, ni una calificación de una
agencia. Para la mayoría de las herramientas del mercado, esas empresas son invisibles.

**FinTarget está pensado también para ellas.** Con lo mínimo que cualquier empresa tiene —sus
**estados financieros, su estado de resultados (PyG) y, a partir de ahí, sus ratios**— el modelo
produce el mismo diagnóstico: estructura del balance, márgenes, apalancamiento, rentabilidad
(ROE / ROA / ROIC), costo de capital y una lectura de riesgo. La empresa se ubica **frente a su
propio sector**, comparándola con las empresas parecidas de las que sí tenemos historia.

Las fuentes cambian —en vez de la bolsa, se usan los estados que las sociedades reportan a la
**Superintendencia de Sociedades**, las **notas a los estados financieros** y datos del sector—
pero el diagnóstico sigue siendo posible. Para el costo de capital, en lugar de sacar el riesgo
del precio de la acción (que no existe), se usa el método que enseña el curso: la referencia del
sector más la **prima de riesgo país** de Colombia.

> Ya hoy tenemos **asistentes** que hacen partes de esto (ver el diccionario abajo). El siguiente
> paso natural es **crear un asistente nuevo, específico para la empresa colombiana no cotizada**,
> que sepa leer un juego de estados de Supersociedades y sus notas, y arme el diagnóstico
> completo. Es un desarrollo acotado y de alto valor práctico.

### El diccionario: qué significa cada palabra técnica

Más abajo, en la parte de arquitectura, aparecen términos de tecnología. Aquí están traducidos:

| Palabra técnica | Qué es, en cristiano |
|---|---|
| **Modelo (de *machine learning*)** | Un programa que **aprende de ejemplos** en vez de seguir reglas fijas. Igual que un analista de crédito con veinte años de oficio "sabe" reconocer una empresa riesgosa por haber visto miles, el modelo aprende ese patrón de miles de casos con desenlace conocido, y lo aplica a una empresa nueva. |
| **NLP (procesamiento de lenguaje natural)** | La capacidad de que el computador **lea texto y lo entienda**: un informe de gestión, las notas a los estados, una noticia. No solo cuenta palabras: capta el **tono** (optimista, cauto, preocupado) y detecta cuándo la empresa **cambió** lo que venía diciendo de un año a otro. Es el analista que se lee las 200 páginas del informe que nadie alcanza a leer. |
| **Plugin / *skill* (asistente)** | Un **complemento especializado** que se le "instala" a la inteligencia artificial para que sepa hacer una tarea concreta muy bien. Piense en un practicante entrenado para una sola cosa —"hazme el análisis vertical de este Excel", "arma el modelo de WACC"— que la hace siempre igual y sin cansarse. Ya tenemos seis (ver abajo). Un *plugin* es simplemente **varios de esos asistentes empaquetados juntos**. |
| **Explicabilidad (SHAP)** | La garantía de que el modelo **no es una caja negra**. Por cada conclusión, muestra **qué pesó y cuánto**: "esta empresa da riesgo alto sobre todo por su bajo cubrimiento de intereses y su caída de margen". Sin esto, ningún comité debería aceptar un resultado. |
| **Trazabilidad / auditable** | Que **cada número apunta a su origen** —a la línea exacta del estado financiero, al archivo, a la fuente pública— y que el análisis **se puede volver a correr y da lo mismo**. Nada sale de un lugar que no se pueda señalar. |
| **API / *backend*** | El "motor" que atiende pedidos: usted le pide "diagnostica esta empresa" y le devuelve el resultado. Es la parte que no se ve. |
| ***Frontend* / tablero** | La pantalla que **sí** se ve: un tablero que la junta explora por sí misma —elegir años, comparar, ver la explicación de cada indicador al pasar el cursor—. Como el tablero que ya se hizo para VISA. |
| **Datos públicos (SEC EDGAR, XBRL)** | La base de datos oficial y **gratuita** donde las empresas de EE. UU. depositan por ley sus estados financieros auditados, en un formato que el computador lee directo. Para Colombia, el equivalente son los reportes a **Supersociedades**. |
| **Orquestación (tipo Dagster)** | Un **tablero de control** que vigila que todo el proceso corra bien y con datos frescos —como el panel de una planta que muestra en verde/rojo si cada etapa está funcionando—. |

Con esas equivalencias, la parte técnica de abajo se lee sin tropiezos.

---

## El problema que resuelve (con un ejemplo real)

Un ratio financiero describe un **estado**, no una **trayectoria**. El protocolo estándar
—recopilar, calcular, comparar, interpretar— responde *"¿contra qué?"* pero no *"¿hacia
dónde?"*. En la práctica, el deterioro de una empresa suele ser visible en el lenguaje de la
gerencia y en el flujo de noticias **antes** de que los números lo reflejen del todo.

> Ejemplo del propio trabajo del curso: en VISA la razón corriente cae de 1,75x a 1,08x entre
> 2021 y 2025. El tramo final se explica casi por completo por la reclasificación de unos
> US$ 5.569 millones de deuda de largo a corto plazo —un hecho que se comunica y se contextualiza
> en la narrativa del 10-K antes de que el ratio de liquidez lo muestre. Un modelo que solo mira
> el ratio ve una caída; uno que también lee el texto entiende que es contable, no de solvencia.

FinTarget mide con rigor **cuánto aporta leer el texto** frente a mirar solo los números —y lo
comprueba con datos de años que el modelo no vio al entrenarse, para que la mejora sea real y no
un espejismo—.

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
                       │   flujos de ingesta · features · entrenamiento ·
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
