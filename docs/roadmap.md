## Roadmap

[← Volver al inicio](index.md) · [Arquitectura](arquitectura.md) · [Datos](datos.md)

El proyecto se construye de adentro hacia afuera: primero el motor determinista de indicadores
(donde ya hay trabajo hecho y verificable), luego el panel de datos, luego los modelos, y por
último la capa de texto —que es la contribución de investigación y la de mayor riesgo—.

| Fase | Entregable | Estado | Horizonte |
|---|---|---|---|
| **0 · Cimientos** | `finmetrics.py` (ratios, DuPont, Altman Z/Z'/Z'', WACC, ROIC, EVA) extraído del modelo de VISA + *golden tests*. `ingest/edgar.py` (companyfacts XBRL). `cli.py`. Repo, CI, plugin publicado, sitio de proyecto. | En curso | 2–3 semanas |
| **1 · Panel y EDA** | Universo S&P 500 + Russell 2000 construido y perfilado. Panel contable trimestral y anual 2010–2025 desde SEC EDGAR. Tablero de ratios reproducible. Particiones temporales fijadas. | Universo y primer EDA hechos | 2 semanas |
| **2 · Modelos *benchmark*** | Reglas Altman + regresión + *gradient boosting* sobre ratios. Validación fuera de tiempo. SHAP. Caso VISA contrastado contra el rating real AA−. | Pendiente | 2–3 semanas |
| **3 · NLP y FTM** | EDGAR-CORPUS integrado + *parser* propio 2021–2025. *Fine-tuning* de FinBERT. FinTarget-Model multimodal. **Estudio de ablación** (el resultado principal). | Pendiente | 4–6 semanas |
| **4 · Servicio y observabilidad** | Backend (API `/score`). Frontend (tablero heredero del de VISA). Tablero tipo Dagster con los DAGs de ingesta, *features*, entrenamiento y monitoreo de *drift*. | Pendiente | 3–4 semanas |
| **5 · Casos y cierre** | TGLS y Ecopetrol de extremo a extremo. Modo empresa privada sobre un caso anonimizado real. Informe final y *model card*. | Pendiente | 2 semanas |

### Qué está verificado hoy

- **SEC EDGAR / XBRL** responde con la serie histórica completa (probado con VISA, CIK 0001403161).
- **EDGAR-CORPUS** es de acceso abierto (no *gated*); el hueco 2021–2025 exige un *parser* propio.
- Los **datasets de rating** se descargan sin credenciales y el principal trae **CIK** → se pueden
  unir *ratios ↔ texto del 10-K ↔ XBRL en vivo* por la misma llave.
- Las **6 skills** de análisis funcionan y están empaquetadas como *plugin*.

### Qué prometer y qué no

- **Sí:** un *baseline* de rating creíble (grado de inversión / 7 grupos), con explicabilidad y
  validación fuera de tiempo; el diagnóstico completo (vertical/horizontal, ratios, WACC, EVA)
  automatizado; la medición formal del aporte del texto.
- **No:** un motor de rating que compita con una agencia (el dataset es corto, 2010–2016, y
  mezcla agencias); precisión por escalón fino; *fair value* o recomendación de inversión.
- El **estudio de ablación puede dar que el texto no aporta**. Sigue siendo un resultado válido —
  y conviene tenerlo presente antes de comprometerlo como proyecto de grado.

El análisis completo de viabilidad —qué es factible, con qué evidencia y con cuánto esfuerzo—
está en
[`docs/viabilidad.md`](https://github.com/Hyper-Target/FinTarget/blob/main/docs/viabilidad.md).
