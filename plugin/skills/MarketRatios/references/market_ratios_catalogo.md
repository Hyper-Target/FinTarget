# Catálogo de ratios de mercado — MarketRatios

Referencia: CFA Institute — *Equity Valuation: Concepts and Basic Tools* y *Free Cash Flow Valuation*.
Todo múltiplo se calcula **por año fiscal** (numerador de mercado a la fecha de cierre fiscal) y
**TTM/actual** (precio de hoy vs. últimos 12 meses). Blindar denominadores con `IFERROR`/`ISNUMBER`.

---

## 0. Bloques de construcción

| Concepto | Fórmula | Nota |
|---|---|---|
| Capitalización de mercado | Precio × Acciones en circulación | acciones de la **portada** del 10-K/10-Q, no el promedio ponderado |
| Enterprise Value (EV) | Capitalización + Deuda financiera − Efectivo e inversiones CP + Interés minoritario + Preferentes | usar deuda financiera bruta, no pasivos totales |
| UPA diluida (EPS) | Utilidad neta atribuible / Acciones diluidas promedio | del propio estado de resultados |
| FCF (a la firma, FCFF) | FCO − Capex | si no hay estado de flujos → "No disponible" |
| FCFE | FCO − Capex + Deuda neta emitida | idem |

---

## 1. Métricas por acción

| Ratio | Fórmula |
|---|---|
| UPA (EPS) básica / diluida | Utilidad neta atribuible / acciones (básicas / diluidas) |
| Valor en libros por acción (BVPS) | Patrimonio atribuible / acciones en circulación |
| Ventas por acción (SPS) | Ingresos / acciones |
| FCF por acción (FCFPS) | FCF / acciones |
| Dividendo por acción (DPS) | Dividendos declarados / acciones |

---

## 2. Múltiplos de precio (equity)

| Ratio | Fórmula | n/s cuando |
|---|---|---|
| P/E *trailing* | Precio / UPA diluida TTM | UPA ≤ 0 |
| P/E *forward* | Precio / UPA estimada próximo año | sin estimado |
| P/VL (P/B) | Precio / BVPS | patrimonio ≤ 0 |
| P/Ventas (P/S) | Precio / SPS | — |
| P/FCF | Precio / FCFPS | FCF ≤ 0 |
| PEG | (P/E) / (crecimiento esperado de UPA en %, p. ej. 15 para 15 %) | crecimiento ≤ 0 |

---

## 3. Múltiplos de firm value (EV)

| Ratio | Fórmula |
|---|---|
| EV/EBITDA | EV / EBITDA | 
| EV/EBIT | EV / EBIT |
| EV/Ventas | EV / Ingresos |
| EV/FCF (FCFF) | EV / (FCO − Capex) |
| EV/(EBITDA − Capex) | EV / (EBITDA − Capex) — corrige la intensidad de capital |

---

## 4. Rendimientos (yields)

| Ratio | Fórmula |
|---|---|
| Earnings yield | UPA diluida TTM / Precio  (= 1 / P/E) |
| FCF yield | FCFPS / Precio |
| Dividend yield | DPS / Precio |
| Buyback yield | Recompras netas de acciones (12m) / Capitalización |
| **Shareholder yield** | (Dividendos + Recompras netas) / Capitalización |

---

## 5. Política de capital

| Ratio | Fórmula | Lectura |
|---|---|---|
| Payout | DPS / UPA | > 100 % = paga más de lo que gana |
| Cobertura del dividendo con FCF | FCF / Dividendos pagados | < 1x = dividendo no cubierto por caja |

---

## 6. Verificaciones (fila de chequeo, ~0 o dentro de tolerancia)

1. `Capitalización − Precio × Acciones` = 0
2. `EV reconstruido − EV de la fuente de contraste` ≈ 0 (tolerancia por fecha)
3. `Earnings yield − 1/(P/E)` = 0
4. `P/E − (P/B ÷ ROE)` ≈ 0   (identidad: P/E = P/B / ROE)
5. `P/S − (P/E × margen neto)` ≈ 0

---

## 7. Contexto (sin umbral absoluto)

- Mapa de calor de cada múltiplo **contra su propia serie histórica** (5 años).
- Fila "premio/descuento vs. promedio de 5 años" por múltiplo: `múltiplo_actual / promedio_5a − 1`
  (verde = barato vs. su historia, rojo = caro).
- Si el usuario da comparables: columna con la **mediana del set** y el premio/descuento vs. esa mediana.
- Nota automática cuando el denominador sea negativo o < 5 % de su media (múltiplo "no significativo").

---

## 8. Errores comunes

1. Mezclar **precio de hoy** con **utilidad de un FY viejo** (hay que usar el precio al cierre de ese FY).
2. Usar **acciones promedio ponderadas** para la capitalización (son para la UPA).
3. Usar **pasivos totales** en vez de **deuda financiera** al construir el EV.
4. Ignorar **interés minoritario y preferentes** en el EV.
5. No ajustar por **splits / reorganización de holding / cambio de cierre fiscal**.
6. Reportar P/E con UPA negativa (es "n/s", no un número).
7. Tomar el # de acciones de **una sola fuente** sin contrastar (portada 10-K vs. agregador difieren por buybacks recientes).
8. No registrar **la fecha del precio** — el modelo debe decir "a qué día" está.
