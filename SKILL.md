---
name: "defect-analysis"
description: "Use when the task is to analyze defect-related DFT results, including neutral defect formation energies, stoichiometric changes, structural distortion around a defect, and compact markdown reports from pristine and defect calculations."
---

# Defect Analysis

Use this skill for defect-focused post-processing rather than generic workflow setup.

## When to use

- estimate a neutral defect formation energy from pristine and defect calculations
- summarize how stoichiometry changes between pristine and defect cells
- quantify structural or volume change caused by a defect
- write a compact defect-analysis report from finished calculations

## Use the bundled helpers

- `scripts/analyze_defect_formation.py`
  Estimate a neutral defect formation energy from pristine and defect states.
- `scripts/analyze_defect_structure.py`
  Compare pristine and defect structures and summarize size or stoichiometry changes.
- `scripts/export_defect_report.py`
  Export a markdown defect-analysis report.

## Guardrails

- Do not treat a neutral formation-energy estimate as a full charged-defect treatment.
- State the chemical potential convention explicitly.
- Distinguish raw energetic extraction from final physical interpretation.
