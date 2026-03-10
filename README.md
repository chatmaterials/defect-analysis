# defect-analysis

[![CI](https://img.shields.io/github/actions/workflow/status/chatmaterials/defect-analysis/ci.yml?branch=main&label=CI)](https://github.com/chatmaterials/defect-analysis/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/chatmaterials/defect-analysis?display_name=tag)](https://github.com/chatmaterials/defect-analysis/releases)

Standalone skill for defect-focused DFT result analysis, including automatic defect-type inference, multi-species chemical-potential support, and multi-candidate screening.

Supports VASP, QE, and ABINIT-style pristine/defect inputs.

## Install

```bash
npx skills add chatmaterials/defect-analysis -g -y
```

## Local Validation

```bash
python3 -m py_compile scripts/*.py
npx skills add . --list
python3 scripts/analyze_defect_formation.py fixtures/pristine fixtures/defect --mu -4.0 --temperature-k 1000 --site-density-cm3 1e22 --json
python3 scripts/analyze_defect_formation.py fixtures/qe/pristine fixtures/qe/defect --mu -4.0 --json
python3 scripts/analyze_defect_formation.py fixtures/abinit/pristine fixtures/abinit/defect --mu -4.0 --json
python3 scripts/analyze_defect_formation.py fixtures/substitutional/pristine fixtures/substitutional/defect --mu-term Fe=-6.0 --mu-term Li=-1.5 --json
python3 scripts/analyze_defect_structure.py fixtures/pristine/POSCAR fixtures/defect/POSCAR --json
python3 scripts/compare_defect_candidates.py fixtures fixtures/candidates/high-energy-vacancy --mu -4.0 --max-volume-change-percent 5.0 --temperature-k 1000 --site-density-cm3 1e22 --target-defect-type vacancy-like --target-concentration-cm3 1e10 --json
python3 scripts/export_defect_report.py fixtures/pristine fixtures/defect --mu -4.0 --temperature-k 1000
python3 scripts/run_regression.py
```
