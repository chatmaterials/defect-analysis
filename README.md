# defect-analysis

Standalone skill for defect-focused DFT result analysis.

## Install

```bash
npx skills add chatmaterials/defect-analysis -g -y
```

## Local Validation

```bash
python3 -m py_compile scripts/*.py
npx skills add . --list
python3 scripts/analyze_defect_formation.py fixtures/pristine fixtures/defect --species O --delta -1 --mu -4.0 --json
python3 scripts/analyze_defect_structure.py fixtures/pristine/POSCAR fixtures/defect/POSCAR --json
python3 scripts/export_defect_report.py fixtures/pristine fixtures/defect --species O --delta -1 --mu -4.0
python3 scripts/run_regression.py
```
