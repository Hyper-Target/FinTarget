# -*- coding: utf-8 -*-
"""
Plantilla de graficas reutilizables para IncAnalyze (analisis profundo de una empresa).
Adaptada de las graficas construidas en la sesion de referencia (22-ago-2026) para
DailyReport y el glosario de clase. Cada funcion recibe datos REALES de la empresa
(no valores hardcodeados) y guarda un PNG.

Uso tipico:
    from plantilla_graficas_empresa import *
    grafico_cascada_rentabilidad(
        out_path="graficos/empresa_cascada.png",
        empresa="Ecopetrol", anio=2025,
        ingresos=137_000, cogs=-95_000, opex=-12_000, da=-9_500,
        intereses=-3_200, tasa_impuesto=0.35, moneda="COP miles de millones",
    )
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

GREEN = "#1a7a3c"
RED = "#b3241c"
GRAY = "#8a8a8a"
BLUE = "#1f4e8c"
ORANGE = "#c9791b"
LIGHTBLUE = "#a9c4e8"
PURPLE = "#6a1b9a"

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


def grafico_cascada_rentabilidad(out_path, empresa, anio, ingresos, cogs, opex, da,
                                  intereses, tasa_impuesto, moneda="millones"):
    """Cascada Ingresos -> EBITDA -> EBIT -> EBT -> Utilidad Neta con cifras reales."""
    gross = ingresos + cogs
    ebitda = gross + opex
    ebit = ebitda + da
    ebt = ebit + intereses
    tax = -round(tasa_impuesto * ebt)
    net = ebt + tax

    bars = [
        ("Ingresos", 0, ingresos, "total"),
        ("(–) COGS", ingresos, gross, "delta"),
        ("Utilidad\nBruta", 0, gross, "total"),
        ("(–) Gastos\nOperativos*", gross, ebitda, "delta"),
        ("EBITDA", 0, ebitda, "highlight"),
        ("(–) D&A", ebitda, ebit, "delta"),
        ("EBIT", 0, ebit, "total"),
        ("(–) Intereses", ebit, ebt, "delta"),
        ("EBT", 0, ebt, "total"),
        (f"(–) Impuestos\n({tasa_impuesto:.0%})", ebt, net, "delta"),
        ("Utilidad\nNeta", 0, net, "final"),
    ]
    colors = {"total": BLUE, "delta": RED, "highlight": ORANGE, "final": GREEN}

    fig, ax = plt.subplots(figsize=(13.5, 6.8))
    for i, (label, start, end, kind) in enumerate(bars):
        bottom, height = min(start, end), abs(end - start)
        ax.bar(i, height, bottom=bottom, color=colors[kind], width=0.62,
               edgecolor="white", linewidth=1.2, zorder=3)
        val = f"{end:,.0f}" if kind != "delta" else f"{end - start:+,.0f}"
        ax.text(i, max(start, end) + abs(ingresos) * 0.02, val, ha="center",
                fontsize=9.4, fontweight="bold")
        if kind in ("total", "highlight", "final") and i < len(bars) - 1:
            ax.plot([i + 0.31, i + 0.69], [end, end], color="#999999",
                     linewidth=1, linestyle=":", zorder=2)

    ax.set_xticks(range(len(bars)))
    ax.set_xticklabels([b[0] for b in bars], fontsize=9)
    ax.set_ylabel(moneda)
    ax.set_title(f"{empresa} — Cascada de rentabilidad ({anio})", fontsize=14,
                 fontweight="bold", pad=16)
    ax.set_ylim(0, ingresos * 1.15)
    ax.grid(axis="y", color="#eeeeee", linewidth=0.9)
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    fig.text(0.01, 0.01, "* Gastos Operativos (SG&A) sin incluir D&A. Fuente: estados financieros de la empresa.",
              fontsize=8, color="#666666")
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(out_path, dpi=170)
    plt.close(fig)
    return dict(utilidad_bruta=gross, ebitda=ebitda, ebit=ebit, ebt=ebt, utilidad_neta=net)


def grafico_dupont(out_path, empresa, anio, ventas, utilidad_neta, activos, patrimonio):
    """Descomposicion DuPont del ROE con cifras reales."""
    margen_neto = utilidad_neta / ventas
    rotacion = ventas / activos
    apalancamiento = activos / patrimonio
    roe = margen_neto * rotacion * apalancamiento

    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    def box(x, y, w, h, text, color, fontsize=10.2, textcolor="white"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                     linewidth=0, facecolor=color, zorder=3))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=textcolor, zorder=4)

    def arrow(x0, y0, x1, y1, text=None):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16,
                                      color="#555555", linewidth=1.4, zorder=2))
        if text:
            ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.18, text, ha="center", fontsize=15, color="#555555")

    box(0.1, 2.35, 2.55, 1.0, f"Margen Neto\n{margen_neto:.1%}", BLUE)
    box(3.05, 2.35, 2.55, 1.0, f"Rotación de Activos\n{rotacion:.2f}x", ORANGE)
    box(6.0, 2.35, 2.55, 1.0, f"Apalancamiento\n{apalancamiento:.2f}x", PURPLE)
    arrow(2.65, 2.85, 3.02, 2.85, "×")
    arrow(5.6, 2.85, 5.97, 2.85, "×")
    arrow(4.5, 2.32, 4.5, 1.45)
    box(3.2, 0.55, 3.6, 0.9, f"ROE = {roe:.1%}", GREEN, fontsize=13.5)

    ax.set_title(f"{empresa} — Descomposición DuPont del ROE ({anio})",
                 fontsize=14.5, fontweight="bold", pad=6, x=0.5)
    fig.tight_layout(rect=[0, 0.04, 1, 0.94])
    fig.savefig(out_path, dpi=170)
    plt.close(fig)
    return dict(margen_neto=margen_neto, rotacion=rotacion, apalancamiento=apalancamiento, roe=roe)


def grafico_evolucion_historica(out_path, empresa, anios, ingresos, ebitda):
    """Barras de Ingresos + linea de margen EBITDA a traves de varios anios."""
    anios = list(anios)
    ingresos = np.array(ingresos, dtype=float)
    ebitda = np.array(ebitda, dtype=float)
    margen = ebitda / ingresos

    fig, ax1 = plt.subplots(figsize=(10.5, 5.6))
    ax1.bar(anios, ingresos, color=BLUE, width=0.55, label="Ingresos")
    ax1.bar(anios, ebitda, color=ORANGE, width=0.32, label="EBITDA")
    ax1.set_ylabel("Valor (unidades de reporte)")
    ax1.legend(loc="upper left", fontsize=9, frameon=False)

    ax2 = ax1.twinx()
    ax2.plot(anios, margen * 100, color=GREEN, marker="o", linewidth=2, label="Margen EBITDA (%)")
    ax2.set_ylabel("Margen EBITDA (%)")
    ax2.legend(loc="upper right", fontsize=9, frameon=False)

    ax1.set_title(f"{empresa} — Evolución de Ingresos, EBITDA y margen", fontsize=13.5,
                  fontweight="bold", pad=12)
    ax1.grid(axis="y", color="#eeeeee", linewidth=0.9)
    ax1.set_axisbelow(True)
    for s in ["top"]:
        ax1.spines[s].set_visible(False)
        ax2.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=170)
    plt.close(fig)


def grafico_multiplos_peers(out_path, empresa, peers, pe_dict, ev_ebitda_dict, pb_dict):
    """Compara la empresa (resaltada) contra peers en P/E, EV/EBITDA y P/B.
    peers: lista de nombres incluyendo el de la empresa analizada.
    *_dict: {nombre: valor} para cada multiplo.
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.6))
    specs = [("P/E (x)", pe_dict, BLUE), ("EV/EBITDA (x)", ev_ebitda_dict, ORANGE),
             ("P/B (x)", pb_dict, PURPLE)]
    for ax, (title, d, color) in zip(axes, specs):
        names = [n for n in peers if n in d]
        vals = [d[n] for n in names]
        colors = [GREEN if n == empresa else color for n in names]
        y = np.arange(len(names))
        ax.barh(y, vals, color=colors, height=0.6)
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=9.3)
        ax.set_xlabel(title)
        ax.grid(axis="x", color="#eeeeee", linewidth=0.9)
        ax.set_axisbelow(True)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        for i, v in enumerate(vals):
            ax.text(v, i, f" {v:.1f}x", va="center", fontsize=8.3)
    fig.suptitle(f"{empresa} vs. comparables — Múltiplos de valoración", fontsize=14,
                 fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out_path, dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    import os
    os.makedirs("_demo", exist_ok=True)
    grafico_cascada_rentabilidad("_demo/demo_cascada.png", "Empresa Demo", 2025,
                                  ingresos=1000, cogs=-600, opex=-150, da=-50,
                                  intereses=-40, tasa_impuesto=0.30, moneda="millones USD")
    grafico_dupont("_demo/demo_dupont.png", "Empresa Demo", 2025,
                    ventas=1000, utilidad_neta=112, activos=800, patrimonio=400)
    grafico_evolucion_historica("_demo/demo_evolucion.png", "Empresa Demo",
                                 anios=[2021, 2022, 2023, 2024, 2025],
                                 ingresos=[700, 780, 860, 930, 1000],
                                 ebitda=[150, 175, 200, 225, 250])
    grafico_multiplos_peers("_demo/demo_peers.png", "Empresa Demo",
                             peers=["Empresa Demo", "Peer A", "Peer B", "Peer C"],
                             pe_dict={"Empresa Demo": 12.5, "Peer A": 15.2, "Peer B": 9.8, "Peer C": 18.0},
                             ev_ebitda_dict={"Empresa Demo": 7.1, "Peer A": 8.5, "Peer B": 6.2, "Peer C": 9.9},
                             pb_dict={"Empresa Demo": 1.6, "Peer A": 2.1, "Peer B": 1.1, "Peer C": 2.8})
    print("Demo generada en ./_demo")
