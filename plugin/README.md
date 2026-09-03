# Plugin FinTech (para Claude Code)

Empaqueta las 6 skills de análisis financiero + el comando orquestador `/fintarget-dossier`.

```
plugin/
  .claude-plugin/plugin.json
  skills/      DailyReport · IncAnalyze · VerticalAnalysis · RatioAnalysis · MarketRatios · WaccModel
  commands/    fintarget-dossier.md
```

## Instalar (local, para desarrollo)

```bash
claude plugin marketplace add Hyper-Target/FinTarget
claude plugin install fintech@FinTarget
```

o apuntando a esta carpeta directamente en `~/.claude/config.json`.

## Skills

| Skill | Entrega | Tipo |
|---|---|---|
| DailyReport | Reporte semanal de mercado + gráficas | escrito |
| IncAnalyze | Investigación profunda de una empresa → Markdown + gráficas | escrito |
| VerticalAnalysis | Análisis vertical/horizontal/DuPont dentro del Excel | numérico |
| RatioAnalysis | Hoja "Indicadores" con ratios por familia y semáforos | numérico |
| MarketRatios | Tablero de múltiplos + pestaña "Fuentes" celda a celda | numérico |
| WaccModel | WACC / CAPM / EVA a nivel banca de inversión | numérico |

Las skills se mantienen como fuente de verdad en este repo; para trabajar en ellas desde la carpeta de
Reportes basta con copiar `plugin/skills/*` a `.claude/skills/` (o al revés con el script de sync).
