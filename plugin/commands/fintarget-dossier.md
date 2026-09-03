---
description: Arma el dossier financiero completo de una empresa combinando las skills FinTech (lo escrito de IncAnalyze + lo numérico de VerticalAnalysis, RatioAnalysis, MarketRatios y WaccModel) en un solo entregable.
argument-hint: <empresa o ticker> [--modo listed|private]
---

Construye el **dossier financiero** de: $ARGUMENTS

Ejecuta en orden y consolida todo en una sola carpeta `reports/<empresa>/`:

1. **IncAnalyze** — investigación profunda desde las fuentes primarias (SEC EDGAR/XBRL, Yahoo, BVC/Superfinanciera).
   Entrega el informe Markdown con gráficas. *(capa escrita)*
2. **Construir el Excel base** con el balance y el estado de resultados históricos que recolectó el paso 1
   (varios años, moneda y unidad explícitas). Si la empresa ya tiene un Excel, úsalo.
3. **VerticalAnalysis** + **RatioAnalysis** sobre ese Excel — análisis vertical/horizontal, DuPont y tablero de
   indicadores por familia, con fórmulas reales. *(capa numérica)*
4. **MarketRatios** — múltiplos de precio y de *firm value*, solo si la empresa cotiza. *(capa numérica)*
5. **WaccModel** — WACC (CAPM por regresión y *bottom-up*), Kd después de impuestos, y EVA. *(capa numérica)*
6. Si está disponible el CLI de FinTarget, correr `fintarget score --company <CIK> --mode <modo>` y anexar el
   **rating estimado + probabilidad de estrés + SHAP**. *(capa de modelo)*

Cierra con una **ficha ejecutiva de una página**: qué hace la empresa, estructura del balance, márgenes,
ROE/ROA/ROIC frente al WACC, EVA, señales de riesgo y —si hay divulgación pública— el contraste entre la
narrativa (10-K, noticias) y los fundamentales. Todo trazable a su fuente.
