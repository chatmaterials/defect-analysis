#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=True)


def run_json(*args: str):
    return json.loads(run(*args).stdout)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    formation = run_json("scripts/analyze_defect_formation.py", "fixtures/pristine", "fixtures/defect", "--species", "O", "--delta", "-1", "--mu", "-4.0", "--json")
    ensure(abs(formation["formation_energy_eV"] - 2.0) < 1e-6, "defect formation energy should parse")
    structure = run_json("scripts/analyze_defect_structure.py", "fixtures/pristine/POSCAR", "fixtures/defect/POSCAR", "--json")
    ensure(structure["species_delta"]["O"] == -1, "defect structure analysis should detect one missing O atom")
    ensure(structure["relative_volume_change_percent"] > 0, "defect structure analysis should detect positive volume expansion")
    temp_dir = Path(tempfile.mkdtemp(prefix="defect-analysis-report-"))
    try:
        report_path = Path(
            run(
                "scripts/export_defect_report.py",
                "fixtures/pristine",
                "fixtures/defect",
                "--species",
                "O",
                "--delta",
                "-1",
                "--mu",
                "-4.0",
                "--output",
                str(temp_dir / "DEFECT_REPORT.md"),
            ).stdout.strip()
        )
        report_text = report_path.read_text()
        ensure("# Defect Analysis Report" in report_text, "defect report should have a heading")
        ensure("Formation energy" in report_text, "defect report should include the formation energy")
    finally:
        shutil.rmtree(temp_dir)
    print("defect-analysis regression passed")


if __name__ == "__main__":
    main()
