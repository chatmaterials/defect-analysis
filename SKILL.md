---
name: "defect-analysis"
description: "Use when the task is to analyze defect-related DFT results, including neutral defect formation energies, automatic defect-type inference, stoichiometric changes, structural distortion around a defect, candidate ranking, and compact markdown reports from pristine and defect calculations. Supports VASP, QE, and ABINIT-style inputs."
---

# Defect Analysis

Use this skill for defect-focused post-processing rather than generic workflow setup.

## When to use

- estimate a neutral defect formation energy from pristine and defect calculations
- infer whether the defect looks vacancy-, interstitial-, substitutional-, or complex-like
- summarize how stoichiometry changes between pristine and defect cells
- quantify structural or volume change caused by a defect
- rank multiple defect candidates with a compact formation-plus-strain heuristic
- write a compact defect-analysis report from finished calculations

Supported backends:

- VASP-like directories with `OUTCAR` and `POSCAR`
- QE-like directories with `.out` and structural input blocks
- ABINIT-like directories with `.abo` and `.abi`

## Use the bundled helpers

- `scripts/analyze_defect_formation.py`
  Estimate a neutral defect formation energy, infer the defect type, and optionally estimate an equilibrium fraction.
- `scripts/analyze_defect_structure.py`
  Compare pristine and defect structures and summarize size, stoichiometry, and inferred defect type.
- `scripts/compare_defect_candidates.py`
  Rank multiple defect candidates with a compact formation-plus-strain heuristic.
- `scripts/export_defect_report.py`
  Export a markdown defect-analysis report.

## Guardrails

- Do not treat a neutral formation-energy estimate as a full charged-defect treatment.
- State the chemical potential convention explicitly.
- Distinguish raw energetic extraction from final physical interpretation.
