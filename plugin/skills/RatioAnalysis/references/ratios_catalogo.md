# Catálogo de ratios financieros — RatioAnalysis

Referencia maestra: **CFA Institute — Financial Analysis Techniques** (y *Analyzing Balance Sheets*).
Todas las fórmulas asumen dos hojas fuente en el mismo libro: `Balance` y `Resultados`
(ajusta los nombres). `A`, `B` = celdas de las hojas fuente; los ratios se blindan con
`=IFERROR(IF(AND(ISNUMBER(A),ISNUMBER(B),B<>0), A/B, "n/d"), "n/d")`.

Convención de signos: costos y gastos financieros se toman en **valor absoluto** (`ABS(...)`)
porque algunos exports los traen negativos y otros positivos.

---

## 1. Liquidez

| Ratio | Fórmula | Formato | Interpretación |
|---|---|---|---|
| Razón corriente | Activo corriente / Pasivo corriente | `0.00"x"` | Veces que el activo líquido cubre la deuda a < 1 año. |
| Prueba ácida (quick) | (Activo corriente − Inventario) / Pasivo corriente | `0.00"x"` | Igual, sin depender de vender inventario. |
| Razón de efectivo | (Efectivo + Inversiones CP) / Pasivo corriente | `0.00"x"` | Cobertura inmediata, solo con caja. |
| Capital de trabajo | Activo corriente − Pasivo corriente | monto | Colchón de liquidez en unidades monetarias. |
| Capital de trabajo / Ventas | (Act. corr. − Pas. corr.) / Ingresos | `0.0%` | Cuánto capital de trabajo consume cada peso de venta; sube = más intensivo. |

**Umbrales (genéricos):** razón corriente verde ≥ 1.5x / ámbar 1.0–1.5x / rojo < 1.0x ·
prueba ácida verde ≥ 1.0x / ámbar 0.7–1.0x / rojo < 0.7x · razón de efectivo verde ≥ 0.5x.
*Retail y utilities operan sanos con razón corriente ~1.0–1.2x; software/servicios suelen > 2x.*

---

## 2. Endeudamiento (estructura de capital)

| Ratio | Fórmula | Formato |
|---|---|---|
| Deuda total / Activos | Pasivo total / Activo total | `0.0%` |
| Pasivos / Patrimonio (D/E contable) | Pasivo total / Patrimonio total | `0.00"x"` |
| Deuda financiera / Patrimonio | Deuda financiera total / Patrimonio total | `0.00"x"` |
| Deuda financiera / Capitalización | Deuda fin. / (Deuda fin. + Patrimonio) | `0.0%` |
| Deuda neta | Deuda financiera total − Efectivo − Inversiones CP | monto |
| Multiplicador de apalancamiento | Activo total / Patrimonio atribuible | `0.00"x"` |

**Deuda financiera total** = porción corriente de deuda LP + deuda LP + arrendamientos
(corrientes + no corrientes). NO incluye cuentas por pagar, impuestos ni ingresos diferidos.
**Deuda neta < 0 ⇒ caja neta** (posición de tesorería positiva); no es un error, marca con
mapa de calor "menos es mejor".

**Umbrales:** Deuda/Activos verde < 50% / ámbar 50–65% / rojo > 65% · Deuda fin./Patrimonio
verde < 0.5x / ámbar 0.5–1.0x / rojo > 1.0x. *Utilities e infraestructura toleran > 65%
por flujos estables; O&G y cíclicas deben estar más bajas.*

---

## 3. Solvencia (capacidad de servir la deuda)

| Ratio | Fórmula | Formato |
|---|---|---|
| Cobertura de intereses (TIE) | EBIT / ABS(Gastos financieros) | `0.00"x"` |
| Cobertura con EBITDA | EBITDA / ABS(Gastos financieros) | `0.00"x"` |
| Deuda neta / EBITDA | Deuda neta / EBITDA | `0.00"x"` |
| Deuda total / EBITDA | Deuda financiera total / EBITDA | `0.00"x"` |
| FCO / Deuda total | Flujo de caja operativo / Deuda financiera total | `0.0%` |
| Perfil de vencimientos | (nota) | — |

**Umbrales:** cobertura de intereses verde > 6x / ámbar 3–6x / rojo < 3x · Deuda neta/EBITDA
verde < 1.5x / ámbar 1.5–3.0x / rojo > 3.0x.
FCO/Deuda y perfil de vencimientos suelen requerir Estado de Flujo de Efectivo y notas a los
EEFF → **"No disponible"** si el archivo no los trae.

---

## 4. Eficiencia (actividad)

| Ratio | Fórmula | Formato |
|---|---|---|
| Rotación de inventario | Costo de ventas / Inventario | `0.00"x"` |
| Días de inventario (DIO) | 365 / (Costo de ventas / Inventario) | `0" días"` |
| Rotación de cartera | Ingresos / Cuentas por cobrar | `0.00"x"` |
| Días de cartera (DSO) | 365 / (Ingresos / Cuentas por cobrar) | `0" días"` |
| Días de proveedores (DPO) | 365 / (Costo de ventas / Cuentas por pagar) | `0" días"` |
| Ciclo de conversión de efectivo (CCC) | DIO + DSO − DPO | `0" días"` |
| Rotación de activos | Ingresos / Activo total | `0.00"x"` |
| Rotación de activo fijo | Ingresos / PP&E neto | `0.00"x"` |

Todos con **mapa de calor** (no semáforo): la lectura es de tendencia y comparación
sectorial, no de umbral absoluto. Para DIO/DSO/DPO/CCC, "menos días es mejor" (excepto DPO,
donde más días = más financiación gratis de proveedores, aunque muy alto puede señalar
tensión de caja). Idealmente con saldos promedio `(inicio+fin)/2`; ver SKILL.md.

**Umbral CCC (genérico):** verde < 60 días / ámbar 60–120 / rojo > 120. Manufactura con
inventario pesado (como vidrio/aluminio) suele estar en 90–150 días.

---

## 5. Rentabilidad

| Ratio | Fórmula | Formato |
|---|---|---|
| Margen bruto | Utilidad bruta / Ingresos | `0.0%` |
| Margen operativo (EBIT) | EBIT / Ingresos | `0.0%` |
| Margen EBITDA | EBITDA / Ingresos | `0.0%` |
| Margen neto | Utilidad neta atribuible / Ingresos | `0.0%` |
| ROA | Utilidad neta atribuible / Activo total | `0.0%` |
| ROE | Utilidad neta atribuible / Patrimonio **atribuible** | `0.0%` |
| ROIC | NOPAT / Capital invertido | `0.0%` |

**NOPAT** = EBIT × (1 − tasa efectiva de impuesto), con tasa efectiva = Impuesto de renta / EBT.
**Capital invertido** = Deuda financiera total + Patrimonio total − Efectivo (aprox.).
**Patrimonio atribuible** = Patrimonio total − Interés minoritario.

**Umbrales:** margen neto verde > 10% / ámbar 3–10% / rojo < 3% · ROA verde > 6% / ámbar 2–6%
/ rojo < 2% · ROE verde > 15% / ámbar 8–15% / rojo < 8% (referencia: costo de patrimonio
~8–12% USD, ~13–16% COP). El **ROE lleva doble formato**: mapa de calor + semáforo.

---

## 6. Descomposición DuPont del ROE

**3 factores:**
```
ROE = Margen neto           ×  Rotación de activos      ×  Multiplicador de apalancamiento
    = (Ut. neta / Ingresos) ×  (Ingresos / Activo tot.) ×  (Activo tot. / Patrimonio atrib.)
```

**5 factores** (si el archivo trae EBT y EBIT por separado):
```
ROE = (Ut. neta / EBT)  ×  (EBT / EBIT)      ×  (EBIT / Ingresos)  ×  (Ingresos / Activo)  ×  (Activo / Patrim. atrib.)
      carga fiscal          carga de intereses   margen EBIT           rotación               apalancamiento
```

Fila obligatoria de **chequeo de consistencia**: `ROE(directo) − ROE(DuPont)`, formato `0.00%`,
debe dar ≈ 0 en todos los años. Si no, revisa el mapeo de filas (típicamente el patrimonio
atribuible o el activo total).

Cada factor con mapa de calor; el ROE reconstruido además con semáforo.

---

## 7. Calidad del balance

| Ratio | Fórmula | Formato | Umbral |
|---|---|---|---|
| Goodwill / Activos | Goodwill / Activo total | `0.0%` | verde < 5% / ámbar 5–15% / rojo > 15% |
| Intangibles / Patrimonio | Intangibles (incl. goodwill) / Patrimonio total | `0.0%` | verde < 15% / ámbar 15–40% / rojo > 40% |
| Impuesto diferido neto / Patrimonio | (Activo por imp. dif. − Pasivo por imp. dif.) / Patrimonio | `0.0%` | mapa de calor |
| Provisiones / Pasivos | Provisiones (pensiones, litigios) / Pasivo total | `0.0%` | mapa de calor |
| Activo corriente sin caja / Pasivo corriente | (Act. corr. − Efectivo − Inv. CP) / Pas. corr. | `0.00"x"` | mapa de calor — mide dependencia de working capital |
| Pasivos contingentes | (nota) | — | requiere notas a los EEFF |

Goodwill alto y creciente = riesgo de deterioro (impairment); un cargo por deterioro no es
caja pero destruye patrimonio y dispara el apalancamiento.

---

## 8. Caja (requiere Estado de Flujo de Efectivo)

| Ratio | Fórmula | Formato |
|---|---|---|
| FCO / Utilidad neta | Flujo de caja operativo / Utilidad neta | `0.00"x"` |
| Conversión de EBITDA en caja | FCO / EBITDA | `0.0%` |
| FCL / Ventas | (FCO − Capex) / Ingresos | `0.0%` |
| Capex / D&A | Capex / Depreciación y amortización | `0.00"x"` |

Si el Excel no trae Estado de Flujo de Efectivo → **todas "No disponible"**. No sustituir FCO
por "Utilidad neta + D&A" sin decirlo explícitamente (es un proxy grosero que ignora el
cambio en capital de trabajo).

**Regla de lectura:** FCO/Utilidad neta persistentemente < 1 es señal de baja calidad de
utilidades (la utilidad no se está volviendo caja).

---

## Errores comunes a evitar

1. **Usar patrimonio total en vez de atribuible** para el ROE cuando hay interés minoritario.
2. **Confundir deuda financiera con pasivo total** en los ratios de apalancamiento.
3. **Dividir por una base casi cero** y reportar un ratio de miles de %: blindar con `ISNUMBER` y, si hace falta, piso de materialidad.
4. **Mezclar saldo promedio en unos años y de cierre en otros.** Sé consistente y anótalo.
5. **Estimar EBITDA o FCO sin etiquetar la fila como "[proxy]".**
6. **Reutilizar umbrales de un sector en otro** (una utility con Deuda/Activos 60% está sana; una tecnológica, no).
7. **Semáforo en todo.** Reserva el semáforo para umbrales con respaldo; usa mapa de calor para tendencias.
