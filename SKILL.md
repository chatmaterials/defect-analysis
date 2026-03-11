---
name: "defect-analysis"
description: "Use when the task is to analyze defect-related DFT results, including neutral defect formation energies, automatic defect-type inference, multi-species chemical-potential terms, stoichiometric changes, abundance estimates, candidate ranking, and compact markdown reports from pristine and defect calculations. Supports VASP, QE, and ABINIT-style inputs."
---

# Defect Analysis

Use this skill for defect-focused post-processing rather than generic workflow setup.

## When to use

- estimate a neutral defect formation energy from pristine and defect calculations
- infer whether the defect looks vacancy-, interstitial-, substitutional-, or complex-like
- apply multi-species chemical-potential terms for substitutional or complex defects
- summarize how stoichiometry changes between pristine and defect cells
- quantify structural or volume change caused by a defect
- estimate compact abundance metrics under a temperature and site-density assumption
- rank multiple defect candidates in balanced, abundant, substitutional, or strain-sensitive modes
- write a compact defect-analysis report from finished calculations

Supported backends:

- VASP-like directories with `OUTCAR` and `POSCAR`
- QE-like directories with `.out` and structural input blocks
- ABINIT-like directories with `.abo` and `.abi`

## Use the bundled helpers

- `scripts/analyze_defect_formation.py`
  Estimate a neutral defect formation energy, infer the defect type, and optionally estimate abundance metrics.
- `scripts/analyze_defect_structure.py`
  Compare pristine and defect structures and summarize size, stoichiometry, and inferred defect type.
- `scripts/compare_defect_candidates.py`
  Rank multiple defect candidates with balanced, abundant, substitutional, or strain-sensitive heuristics.
- `scripts/export_defect_report.py`
  Export a markdown defect-analysis report.

## Guardrails

- Do not treat a neutral formation-energy estimate as a full charged-defect treatment.
- State the chemical potential convention explicitly.
- Distinguish raw energetic extraction from final physical interpretation.
