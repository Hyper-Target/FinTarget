# -*- coding: utf-8 -*-
"""Genera las graficas para los informes de Forex Factory y Bancolombia."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.size": 10.5,
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})

GREEN = "#1a7a3c"
RED = "#b3241c"
GRAY = "#8a8a8a"
BLUE = "#1f4e8c"
ORANGE = "#c9791b"

# ---------------------------------------------------------------
# GRAFICA 1 - Sorpresas economicas USD (Actual - Forecast) semana Ago 16-22 2026
# ---------------------------------------------------------------
indicadores = [
    ("Philly Fed Mfg. Index (pts)", 47.4, 24.1),
    ("Empire State Mfg. Index (pts)", 20.6, 10.6),
    ("TIC Long-Term Purchases (US$B)", 172.7, 151.4),
    ("Natural Gas Storage (Bcf)", 16, 15),
    ("Building Permits (M, anualizado)", 1.44, 1.37),
    ("NAHB Housing Market Index (pts)", 35, 33),
    ("CB Leading Index m/m (%)", 0.2, 0.1),
    ("Capacity Utilization (%)", 76.3, 76.3),
    ("Flash Services PMI (pts)", 56.8, 54.0),
    ("Unemployment Claims (miles)*", 206, 210),
    ("Industrial Production m/m (%)", 0.2, 0.3),
    ("Flash Manufacturing PMI (pts)", 53.2, 53.9),
    ("Crude Oil Inventories (M barriles)*", 4.4, 0.2),
    ("Pending Home Sales m/m (%)", -2.3, 0.1),
    ("Import Prices m/m (%)", -0.4, 0.1),
    ("Housing Starts (M, anualizado)", 1.24, 1.34),
]

labels = [x[0] for x in indicadores]
actual = np.array([x[1] for x in indicadores])
forecast = np.array([x[2] for x in indicadores])
surprise = actual - forecast
order = np.argsort(surprise)
labels = [labels[i] for i in order]
surprise = surprise[order]

colors = [GREEN if s > 0 else (RED if s < 0 else GRAY) for s in surprise]

fig, ax = plt.subplots(figsize=(9.5, 7.2))
bars = ax.barh(labels, surprise, color=colors, height=0.62, edgecolor="none")
ax.axvline(0, color="#444444", linewidth=1)
ax.set_xlabel("Diferencia Actual vs. Consenso (Dato − Forecast, en unidades del indicador)")
ax.set_title("Sorpresas económicas en EE. UU.\nSemana del 16 al 22 de agosto de 2026",
              fontsize=13, fontweight="bold", pad=14)
for b, s in zip(bars, surprise):
    x = b.get_width()
    align = "left" if x >= 0 else "right"
    pad = 0.15 if x >= 0 else -0.15
    ax.text(x + pad, b.get_y() + b.get_height()/2, f"{s:+.2f}",
            va="center", ha=align, fontsize=8.7, color="#222222")
ax.grid(axis="x", color="#dddddd", linewidth=0.8)
ax.set_axisbelow(True)
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
fig.text(0.02, 0.01,
         "* En Unemployment Claims y Crude Oil Inventories, un valor por encima del pronóstico no es necesariamente\n"
         "favorable (más solicitudes de desempleo o más inventarios de crudo se suelen leer como señal débil).\n"
         "Fuente: Forex Factory (forexfactory.com/calendar), consultado el 22-ago-2026.",
         fontsize=7.6, color="#666666")
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(OUT, "01_sorpresas_economicas_usd.png"), dpi=170)
plt.close(fig)

# ---------------------------------------------------------------
# GRAFICA 2 - Reaccion de mercado (cierre 21-ago-2026, Yahoo Finance)
# ---------------------------------------------------------------
mercado = [
    ("Dow Jones", 0.98),
    ("S&P 500", 0.43),
    ("Nasdaq Composite", 0.43),
    ("Russell 2000", 0.85),
    ("VIX (volatilidad)", -5.50),
    ("UST 10Y yield (^TNX)", 0.89),
]
m_labels = [x[0] for x in mercado]
m_vals = np.array([x[1] for x in mercado])
m_colors = [GREEN if v > 0 else RED for v in m_vals]

fig, ax = plt.subplots(figsize=(8.2, 4.8))
bars = ax.bar(m_labels, m_vals, color=m_colors, width=0.55)
ax.axhline(0, color="#444444", linewidth=1)
ax.set_ylabel("Variación % (cierre del día)")
ax.set_title("Reacción de los mercados de EE. UU. — Viernes 21 de agosto de 2026",
              fontsize=12.5, fontweight="bold", pad=12)
for b, v in zip(bars, m_vals):
    ax.text(b.get_x() + b.get_width()/2, v + (0.15 if v >= 0 else -0.35),
            f"{v:+.2f}%", ha="center", fontsize=9.2)
ax.grid(axis="y", color="#dddddd", linewidth=0.8)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.setp(ax.get_xticklabels(), rotation=12, ha="right")
fig.text(0.02, 0.01, "Fuente: Yahoo Finance (finance.yahoo.com), datos de cierre 21-ago-2026, consultado el 22-ago-2026.",
          fontsize=7.6, color="#666666")
fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig(os.path.join(OUT, "02_reaccion_mercado_21ago.png"), dpi=170)
plt.close(fig)

# ---------------------------------------------------------------
# GRAFICA 3 - Multiplos de valoracion (Desayuno con Bancolombia, 20-ago-2026)
# ---------------------------------------------------------------
multiplos = [
    ("Grupo Cibest", 2.0, 22.0),
    ("Banco de Bogotá", 0.8, 10.4),
    ("Celsia", 1.6, 32.9),
    ("Cementos Argos", 1.5, 24.9),
    ("Corficol", 0.6, 11.8),
    ("Ecopetrol", 1.3, 12.6),
    ("GEB", 1.4, 9.1),
    ("Grupo Aval PF", 1.1, 11.5),
    ("Grupo Sura", 1.1, 10.3),
    ("Grupo Argos", 1.3, 29.7),
    ("ISA", 1.9, 12.6),
    ("Promigas", 1.2, 7.1),
    ("Mineros", 2.7, 8.9),
    ("Terpel", 1.0, 5.2),
    ("PEI", 0.4, 5.1),
]
mm_labels = [x[0] for x in multiplos]
pvl = np.array([x[1] for x in multiplos])
rpg = np.array([x[2] for x in multiplos])

order2 = np.argsort(rpg)
mm_labels = [mm_labels[i] for i in order2]
pvl = pvl[order2]
rpg = rpg[order2]

fig, axes = plt.subplots(1, 2, figsize=(11, 6.4), sharey=True)
y = np.arange(len(mm_labels))

axes[0].barh(y, pvl, color=BLUE, height=0.6)
axes[0].set_yticks(y)
axes[0].set_yticklabels(mm_labels, fontsize=9.3)
axes[0].set_xlabel("PVL 12M (x) — Precio / Valor en Libros")
axes[0].set_title("PVL", fontsize=11, fontweight="bold")
axes[0].grid(axis="x", color="#dddddd", linewidth=0.8)
axes[0].set_axisbelow(True)
for i, v in enumerate(pvl):
    axes[0].text(v + 0.05, i, f"{v:.1f}x", va="center", fontsize=8.3)

axes[1].barh(y, rpg, color=ORANGE, height=0.6)
axes[1].set_xlabel("RPG 12M (x) — Precio / Ganancia (P/E)")
axes[1].set_title("RPG", fontsize=11, fontweight="bold")
axes[1].grid(axis="x", color="#dddddd", linewidth=0.8)
axes[1].set_axisbelow(True)
for i, v in enumerate(rpg):
    axes[1].text(v + 0.3, i, f"{v:.1f}x", va="center", fontsize=8.3)

for ax in axes:
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

fig.suptitle("Múltiplos de valoración — Emisores COLCAP bajo cobertura (cierre 20-ago-2026)",
             fontsize=13, fontweight="bold")
fig.text(0.02, 0.01, "Fuente: Grupo Cibest, LSEG Refinitiv — Desayuno con Bancolombia, 21-ago-2026.",
          fontsize=7.6, color="#666666")
fig.tight_layout(rect=[0, 0.04, 1, 0.95])
fig.savefig(os.path.join(OUT, "03_multiplos_valoracion.png"), dpi=170)
plt.close(fig)

# ---------------------------------------------------------------
# GRAFICA 4 - Ejemplo ilustrativo de analisis tecnico (Bandas de Bollinger, medias moviles, RSI)
# ---------------------------------------------------------------
rng = np.random.default_rng(42)
n = 120
t = np.arange(n)
trend = np.linspace(100, 118, n)
noise = np.cumsum(rng.normal(0, 0.9, n))
price = trend + noise - noise[0]

def sma(x, w):
    out = np.full_like(x, np.nan, dtype=float)
    for i in range(w - 1, len(x)):
        out[i] = x[i - w + 1:i + 1].mean()
    return out

pm10 = sma(price, 10)
pm30 = sma(price, 30)

std20 = np.array([price[max(0, i - 19):i + 1].std() if i >= 19 else np.nan for i in range(n)])
mid = sma(price, 20)
upper = mid + 2 * std20
lower = mid - 2 * std20

delta = np.diff(price, prepend=price[0])
gain = np.where(delta > 0, delta, 0.0)
loss = np.where(delta < 0, -delta, 0.0)
def rma(x, w):
    out = np.full_like(x, np.nan, dtype=float)
    out[w-1] = x[:w].mean()
    for i in range(w, len(x)):
        out[i] = (out[i-1] * (w - 1) + x[i]) / w
    return out
avg_gain = rma(gain, 14)
avg_loss = rma(loss, 14)
rs = avg_gain / np.where(avg_loss == 0, np.nan, avg_loss)
rsi = 100 - (100 / (1 + rs))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.8, 6.6), sharex=True,
                                gridspec_kw={"height_ratios": [3, 1]})

ax1.plot(t, price, color="#222222", linewidth=1.3, label="Precio (ejemplo ilustrativo)")
ax1.plot(t, pm10, color=BLUE, linewidth=1.1, label="Media móvil 10 (PM10)")
ax1.plot(t, pm30, color=ORANGE, linewidth=1.1, label="Media móvil 30 (PM30)")
ax1.plot(t, upper, color=GRAY, linewidth=1.0, linestyle="--", label="Banda de Bollinger sup./inf. (±2σ)")
ax1.plot(t, lower, color=GRAY, linewidth=1.0, linestyle="--")
ax1.fill_between(t, lower, upper, color=GRAY, alpha=0.08)
last = n - 1
ax1.axhline(price[last], color="#aaaaaa", linewidth=0.6)
ax1.set_title("Ejemplo ilustrativo — Medias móviles, Bandas de Bollinger y RSI",
               fontsize=12.5, fontweight="bold", pad=10)
ax1.set_ylabel("Precio (unidades arbitrarias)")
ax1.legend(loc="upper left", fontsize=8, frameon=False)
ax1.grid(color="#eeeeee", linewidth=0.8)
for spine in ["top", "right"]:
    ax1.spines[spine].set_visible(False)

ax2.plot(t, rsi, color="#6a1b9a", linewidth=1.2)
ax2.axhline(70, color=RED, linewidth=0.9, linestyle="--")
ax2.axhline(30, color=GREEN, linewidth=0.9, linestyle="--")
ax2.fill_between(t, 70, 100, color=RED, alpha=0.06)
ax2.fill_between(t, 0, 30, color=GREEN, alpha=0.06)
ax2.set_ylim(0, 100)
ax2.set_ylabel("RSI (14)")
ax2.set_xlabel("Periodos (días de negociación)")
ax2.text(2, 73, "Sobrecompra (>70)", fontsize=7.5, color=RED)
ax2.text(2, 18, "Sobreventa (<30)", fontsize=7.5, color=GREEN)
ax2.grid(color="#eeeeee", linewidth=0.8)
for spine in ["top", "right"]:
    ax2.spines[spine].set_visible(False)

fig.text(0.02, 0.005, "Datos sintéticos con fines exclusivamente pedagógicos: ilustran cómo se leen estos indicadores, "
                       "no corresponden a ninguna acción real del informe.",
          fontsize=7.4, color="#666666")
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(os.path.join(OUT, "04_ejemplo_analisis_tecnico.png"), dpi=170)
plt.close(fig)

print("Graficas generadas en:", OUT)
