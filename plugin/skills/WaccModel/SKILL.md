---
name: WaccModel
description: Construye un modelo profesional de costo promedio ponderado de capital (WACC) en Excel para una empresa. Replica el método que enseña el profesor de Gestión Financiera (fuentes de financiación y pesos, CAPM por dos caminos —beta apalancada bottom-up estilo Damodaran y beta de regresión de la acción en bolsa—, costo de deuda después de impuestos, y WACC), pero a nivel de banca de inversión y corrigiendo sus errores habituales (no descontar el patrimonio con el escudo fiscal, no doble-contar el riesgo país, D/E como celda de input, beta con ventana larga y ajuste de Blume, tasa impositiva efectiva del 10-K, ponderaciones a valor en libros Y a valor de mercado). Úsalo cuando el usuario pida "cálculo del WACC", "costo de capital", "CAPM / Ke", "beta apalancada", "WACC a valor de mercado", o invoque explícitamente FinTech:WaccModel.
---

# WaccModel (FinTech)

Skill hermana de [MarketRatios](../MarketRatios/SKILL.md), [VerticalAnalysis](../VerticalAnalysis/SKILL.md), [RatioAnalysis](../RatioAnalysis/SKILL.md) e [IncAnalyze](../IncAnalyze/SKILL.md).

Toma como referencia el archivo del profesor `Calculos del WACC.xlsx` (caso Ecopetrol) y lo eleva a estándar profesional. El entregable es un Excel con fórmulas reales, una pestaña **Fuentes** (link exacto de cada dato web, ver [MarketRatios](../MarketRatios/SKILL.md)) y una tabla de sensibilidad.

Nació de la sesión del 29-ago-2026 (WACC de Tecnoglass / TGLS en USD, con βU sector "Engineering/Construction" de Damodaran y beta de regresión TGLS vs. S&P 500).

## Cuándo usarla

- El usuario pide el WACC / costo de capital / Ke / CAPM de una empresa, en Excel.
- El usuario quiere "lo mismo que hizo el profesor pero bien hecho".
- El usuario invoca `FinTech:WaccModel`.

Datos de mercado (capitalización, beta, deuda, tasas) → esta skill los trae igual que [MarketRatios](../MarketRatios/SKILL.md): SEC EDGAR primero, agregadores para contrastar, y **todo con su link en la hoja Fuentes**.

## Perfil del usuario (asumir siempre)

Científico de Datos en Finanzas — Maestría en Finanzas, Uninorte. Quiere el modelo **dentro del Excel**, con fórmulas recalculables, celdas de input claramente marcadas, sensibilidad, y cada dato externo trazable a su URL.

## El método del profesor (lo que SÍ se replica)

| Bloque | Qué hace el profesor | Se mantiene |
|---|---|---|
| **Mapa WACC** | Lista cada fuente de financiación con su monto, peso, costo, `Kd(1−T)` y aporte al WACC. | Sí — es la estructura central. |
| **CAPM beta sectorial (Damodaran)** | βU del sector → reapalanca con Hamada `βL = βU·[1+(1−T)·(D/E)]` → `Ke = Rf + βL·PRM + RP`. | Sí — es el "camino de la beta apalancada". |
| **CAPM empresa en bolsa** | Regresión de retornos de la acción vs. índice; `β = COV(ra,rm)/VAR(rm)`; `Ke = Rf + β·PRM + RP`. | Sí — es el "camino de la beta de mercado". |
| **Beta a 5 años mensual** | Beta con datos mensuales de ~5 años (más estable que la diaria). | Sí — es la ventana correcta. |
| **CAPM final / WACC** | Pondera deuda y equity, aplica escudo fiscal a la deuda, suma. | Sí. |
| **Ajuste por inflación / devaluación** (Fisher, paridad de tasas) | Puente entre tasas USD y COP. | **Opcional** — solo si el modelo se pide en COP. Por defecto el modelo va en USD. |

## Errores del profesor que se CORRIGEN (no replicar)

1. **Escudo fiscal aplicado al patrimonio.** En su hoja `CAPM ecopetrol USD` hace `E4 = D4*(1-35%)` sobre el equity. **El patrimonio entra a su costo pleno**; el `(1−T)` es solo para la deuda.
2. **Suma incompleta del WACC.** `Mapa WACC!F10 = SUM(F2:F8)` omite el patrimonio preferente (F9). **El WACC suma TODAS las fuentes.**
3. **Doble conteo del riesgo país.** Usa como "prima" el ERP total de Colombia de Damodaran (7,08%, que YA incluye el CRP) y además le suma el riesgo país (2,85%). **O** se usa `PRM_madura(EE.UU.) + λ·CRP_país`, **o** se usa `ERP_total_país` con `β`, **nunca las dos cosas**. Por defecto: `Ke = Rf_US + βL·ERP_maduro_US + λ·CRP_país`.
4. **D/E incrustado en la fórmula.** `E4 = E3*(1+(1-35%)*(3300000/750000))` — los números van en **celdas de input** referenciadas, no dentro de la fórmula.
5. **Beta diaria no robusta.** Mezcla una beta diaria (R²≈0,02, no significativa, incluso negativa) con la mensual. **Usar solo la beta de ventana larga** (5 años mensual o 2 años semanal) y aplicarle el **ajuste de Blume** `β_aj = 0,371 + 0,635·β` (o Bloomberg `2/3·β + 1/3`). Documentar la beta cruda y la ajustada; no usar la diaria.
6. **`#DIV/0!` en las series.** Toda fórmula de retorno/ratio se blinda (`IFERROR`, `ISNUMBER`).
7. **Tasa impositiva redonda del 35%.** Usar la **tasa efectiva** de la conciliación del 10-K (para TGLS 2025 = 32,2%); dejar el 35% estatutario como fila de sensibilidad.
8. **`B14 = B4+(B9-B9)`** y demás fórmulas redundantes / celdas de texto en medio de rangos numéricos: limpiar.
9. **Solo pesos a valor en libros.** Añadir SIEMPRE la versión a **valor de mercado** (equity = capitalización bursátil; deuda = valor razonable ≈ libros si es tasa flotante). El WACC a valor de mercado es el estándar; el de libros se deja como comparación.
10. **Costo de deuda = promedio de cupones arbitrario.** Usar la **tasa efectiva de la deuda** que reporta el 10-K (nota de deuda), o un `Kd sintético = Rf + spread por rating`. Documentar cuál.

## Estructura del Excel (hojas)

1. **Fuentes** — una fila por dato web, con URL exacta e hipervínculo (ver [MarketRatios](../MarketRatios/SKILL.md), sección "pestaña Fuentes"). Todo dato externo del modelo referencia esta hoja.
2. **Supuestos** — celdas de input (amarillas): Rf, ERP maduro, CRP país, λ, tasa efectiva de impuesto, tasa estatutaria, precio de la acción y fecha, # de acciones, deuda financiera bruta, caja, βU del sector, D/E objetivo si aplica.
3. **Beta** — dos sub-bloques:
   - **Bottom-up (Damodaran):** βU del sector elegido → βL con Hamada usando D/E de la empresa (a libros y a mercado, en celdas separadas).
   - **Regresión (empresa en bolsa):** serie de precios mensuales (≥60 meses) de la acción y del índice **estadounidense** (S&P 500) → retornos → `β = COVARIANCE.P/VAR.P` (y `PENDIENTE`/`SLOPE` como verificación) → R², correlación → β ajustada (Blume). El índice es el de EE. UU. porque la acción cotiza en NY ("beta de US").
4. **Costo de patrimonio (Ke)** — dos columnas, una por cada beta:
   - `Ke_bottom-up = Rf + βL_Hamada · ERP_maduro + λ·CRP`
   - `Ke_regresión = Rf + β_acción(ajustada) · ERP_maduro + λ·CRP`
   Mostrar también la variante en COP si el usuario la pide (sumar devaluación esperada por paridad de tasas y/o diferencial de inflación de Fisher — documentado).
5. **Costo de deuda (Kd)** — tasa efectiva del 10-K (o sintética) · `Kd·(1−T_efectiva)` · sensibilidad con `T` estatutaria.
6. **Pesos** — bloque a **valor en libros** (D = deuda financiera bruta; E = patrimonio contable) y bloque a **valor de mercado** (D = deuda ≈ libros; E = precio × acciones). Los pesos suman 100 % en cada bloque.
7. **WACC** — **matriz** de resultados: {beta bottom-up, beta regresión} × {pesos libros, pesos mercado} → 4 WACC. Marcar los dos "titulares" (pesos de mercado).
8. **Sensibilidad** — tablas de doble entrada: WACC vs (β, ERP), WACC vs (Rf, peso de deuda), WACC vs (Kd, T).
9. **Notas / Metodología** — método aplicado, errores del profesor corregidos, fuente de cada bloque, límites, y aviso de material informativo (no asesoría).

## Fórmulas clave (patrón Excel)

```
βL (Hamada)        = βU * (1 + (1 - T_efec) * (D/E))
Ke                 = Rf + βL * ERP_maduro + lambda * CRP_pais
β regresión        = _xlfn.COVARIANCE.P(rango_ra, rango_rm) / _xlfn.VAR.P(rango_rm)
β ajustada Blume   = 0.371 + 0.635 * β_cruda
Kd después de imp. = Kd * (1 - T_efec)
peso_i (mercado)   = valor_mercado_i / (E_mercado + D_mercado)
WACC               = w_E * Ke + w_D * Kd * (1 - T_efec)     [+ w_P * Kp  si hay preferentes]
```

Para funciones post-2007 usar el prefijo `_xlfn.` al escribir con openpyxl (`_xlfn.COVARIANCE.P`, `_xlfn.VAR.P`); `SLOPE`, `RSQ`, `CORREL`, `AVERAGE` van sin prefijo. Recalcular con Excel COM (`scripts/recalc_excel_windows.py`), no LibreOffice.

## Datos que se necesitan y de dónde salen

| Dato | Fuente primaria | Contraste |
|---|---|---|
| Rf (bono soberano 10 años, moneda del modelo) | US Treasury (home.treasury.gov, daily yield curve) / FRED `DGS10` | tradingeconomics |
| ERP maduro (mercado de EE. UU.) | Damodaran `ctryprem.html` / `histimpl` | — |
| CRP país | Damodaran `ctryprem.html` (country risk premium por país) | — |
| βU del sector | Damodaran `Betas.html` (US) — elegir la industria más cercana al negocio real | `totalbeta.html` |
| Beta de regresión + R² | serie de precios: Yahoo `query1.finance.yahoo.com/v8/finance/chart/{T}?range=6y&interval=1mo` | stockanalysis "Beta (5Y)" |
| Precio y # de acciones | SEC EDGAR 10-K/10-Q (portada) | Yahoo / stockanalysis |
| Deuda financiera y **tasa efectiva** | SEC EDGAR 10-K (nota de deuda: "effective interest rate ... is X%") | — |
| Tasa impositiva efectiva | SEC EDGAR 10-K (conciliación de la tasa estatutaria a la efectiva) | — |
| Capitalización de mercado | precio × acciones (calculado) | stockanalysis / Yahoo |

## Paso a paso

1. Corre [MarketRatios](../MarketRatios/SKILL.md) primero si el usuario también quiere múltiplos — comparten la hoja `Fuentes` y los datos de mercado. Si no, arma una `Fuentes` mínima aquí.
2. Elige la **industria de Damodaran** más cercana al negocio (con el usuario si hay duda): p. ej. Tecnoglass → "Engineering/Construction" o "Building Materials". Anota βU y el año del dato.
3. Baja ≥60 meses de precios de la acción y del **índice de EE. UU.** Calcula retornos y beta con `COVARIANCE.P/VAR.P`; verifica con `SLOPE`. Aplica Blume.
4. Reapalanca βU con el D/E de la empresa (a libros y a mercado).
5. Arma `Ke` por los dos caminos. Arma `Kd(1−T)`.
6. Arma los pesos a libros y a mercado.
7. Construye la matriz WACC y la sensibilidad.
8. Recalcula (Excel COM), confirma cero `#`, revisa vistas previas.
9. Notas: método, errores corregidos, límites, aviso.

## Scripts

`scripts/build_wacc.py` — genera todas las hojas. Parametrizado por dicts `SUPUESTOS`, `FUENTES` y la serie de precios `PRECIOS` (lista de `(mes, precio_accion, nivel_indice)`). **No es genérico**: se rellena por empresa en cada sesión. `recalc_excel_windows.py` y `export_preview_excel.py` como en las otras skills.

## Notas y advertencias

- **Moneda consistente:** si el modelo va en USD, todo en USD (Rf US, ERP US, precios en USD). Para COP, sumar devaluación esperada (paridad de tasas: `(1+Rf_COP)/(1+Rf_US)−1`) y usar Rf COP — documentarlo, no mezclar como hace el profesor.
- **λ (lambda) de riesgo país:** 1,0 si activos/operaciones están en el país emergente; menor si la empresa vende mayormente a mercados desarrollados (juício, documentado). Para TGLS: produce en Colombia (λ≈1) aunque ~98 % de clientes están en Norteamérica.
- **Beta bottom-up vs. regresión:** si convergen (caso TGLS: ~1,27 vs ~1,25 ajustada), reportar el promedio como base y el rango como sensibilidad. Si divergen mucho, explicar por qué (float bajo, iliquidez, cambio de negocio).
- **Nunca** fabriques un dato. Sin fuente → celda vacía + nota en `Fuentes`.
- Cierra con la aclaración de material informativo/educativo, no asesoría de inversión.
