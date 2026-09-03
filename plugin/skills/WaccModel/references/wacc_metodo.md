# WACC — método de referencia (nivel profesional)

## 1. Ecuación

```
WACC = w_E · Ke  +  w_P · Kp  +  w_D · Kd · (1 − T)
```

- `w_E, w_P, w_D` = pesos de patrimonio común, patrimonio preferente y deuda financiera. Suman 1.
- `Ke` = costo del patrimonio (CAPM). **No lleva (1−T).**
- `Kp` = costo del preferente = dividendo preferente / precio del preferente.
- `Kd` = costo de la deuda **antes de impuestos**. Solo la deuda lleva el escudo `(1−T)`.
- `T` = tasa impositiva **efectiva** (conciliación del 10-K), no la estatutaria redonda.

## 2. Costo del patrimonio — CAPM

```
Ke = Rf  +  β_L · ERP_maduro  +  λ · CRP_país          (modelo en USD)
```

- `Rf` = rendimiento del bono del Tesoro de EE. UU. a 10 años (moneda del modelo = USD).
- `ERP_maduro` = prima de riesgo del mercado maduro (EE. UU.), Damodaran (implícita del S&P 500). Ene-2026 ≈ 4,46 %.
- `CRP_país` = country risk premium del país donde la empresa tiene sus operaciones/activos. Damodaran. Colombia ene-2026 = 2,85 %.
- `λ` = exposición al riesgo país (0 a 1+). 1,0 si activos y operación están en el país emergente. Se puede ponderar por % de activos o de ingresos allí.
- **No** sumar `CRP` si `ERP` ya es el "ERP total del país" (ese ya incluye el CRP). Elegir un enfoque.

### Versión en COP (opcional)

```
Ke_COP = [ (1 + Ke_USD) · (1 + devaluación_esperada) ] − 1
devaluación_esperada = (1 + Rf_COP) / (1 + Rf_US) − 1           (paridad de tasas de interés)
```
o, aproximando con inflación (Fisher): `Ke_COP ≈ Ke_USD + (inflación_COP − inflación_US)`.

## 3. Beta

### 3.1 Bottom-up (Damodaran) — "beta apalancada"

```
β_U (sector)  →  Damodaran, industria más cercana al negocio real.
β_L = β_U · [ 1 + (1 − T_efec) · (D/E) ]                        (Hamada, sin deuda con beta propio)
```
- `D/E` de **la empresa** (no el del sector). Calcular a **libros** y a **mercado** por separado.
- Si se quiere la corrección por caja: partir del "unlevered beta corrected for cash" de Damodaran.
- Fórmula de Hamada completa (con β de la deuda `β_D`, normalmente 0):
  `β_L = β_U + (β_U − β_D)·(1−T)·(D/E)`.

### 3.2 Regresión (empresa en bolsa) — "beta de mercado"

```
r_a,t = (P_a,t / P_a,t−1) − 1          r_m,t = (I_m,t / I_m,t−1) − 1
β = COVARIANCE.P(r_a, r_m) / VAR.P(r_m)        (≡ SLOPE(r_a, r_m))
R² = RSQ(r_a, r_m)      ρ = CORREL(r_a, r_m)
```
- Índice de mercado = **S&P 500** (la acción cotiza en NY → "beta de US").
- Ventana: **60 meses** (o 104 semanas). No usar datos diarios de pocas semanas (ruido, R² ~0).
- Ajuste de Blume: `β_aj = 0,371 + 0,635 · β`.  Bloomberg: `β_aj = 2/3 · β + 1/3`.
- Reportar β cruda, R², y β ajustada. Usar la **ajustada** en el CAPM (mean-reversion).

## 4. Costo de la deuda

- **Preferido:** tasa efectiva de la deuda que reporta el 10-K ("the effective interest rate ... is X%").
- **Sintético:** `Kd = Rf + spread por rating` (spread de Damodaran por *interest coverage ratio* o rating).
- **Contable (piso):** gasto financiero / deuda financiera promedio — suele subestimar si la deuda creció.
- Después de impuestos: `Kd · (1 − T_efec)`.

## 5. Pesos

| | Deuda (D) | Patrimonio (E) |
|---|---|---|
| **Valor en libros** | Deuda financiera bruta del balance (corriente + no corriente + leasing) | Patrimonio contable total |
| **Valor de mercado** | Valor razonable de la deuda ≈ libros si es tasa flotante / cotiza cerca de par; si hay bonos, usar su precio de mercado | Capitalización bursátil = precio × acciones en circulación |

El WACC **a valor de mercado es el estándar** (refleja el costo de oportunidad hoy). El de libros se reporta como comparación y es lo que hace el profesor.

## 6. Errores frecuentes (los del archivo del profesor)

1. Escudo fiscal `(1−T)` sobre el patrimonio. ❌ Solo la deuda.
2. WACC que no suma todas las fuentes (omite el preferente). ❌
3. Riesgo país contado dos veces (prima = ERP total país **y** además + CRP). ❌
4. `D/E` escrito como número dentro de la fórmula del beta. ❌ Va en celda de input.
5. Beta diaria de 20-25 datos (no significativa) usada en el CAPM. ❌ Ventana larga + Blume.
6. `#DIV/0!` sin blindar en las series de retornos. ❌
7. `T` = 35 % redondo en vez de la tasa efectiva del 10-K. ❌ (dejar 35 % como sensibilidad).
8. Solo pesos a libros. ❌ Añadir pesos a mercado.
9. `Kd` = promedio simple de cupones de bonos elegidos a mano. ❌ Tasa efectiva del 10-K.
10. Mezclar tasas USD y COP sin el puente de Fisher / paridad. ❌

## 7. Rango de sanidad

Para una empresa mediana de materiales/construcción con exposición a Colombia, en USD:
`Rf ~4,7 % + β·ERP ~5–6 % + CRP ~2,9 %` ⇒ `Ke ~13 %`; `Kd(1−T) ~4,7 %`;
`WACC ~11–13 %` según pesos y beta. Un WACC < 8 % o > 18 % en este perfil obliga a revisar inputs.
