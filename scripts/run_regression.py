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
    formation = run_json("scripts/analyze_defect_formation.py", "fixtures/pristine", "fixtures/defect", "--mu", "-4.0", "--temperature-k", "1000", "--site-density-cm3", "1e22", "--json")
    ensure(abs(formation["formation_energy_eV"] - 2.0) < 1e-6, "defect formation energy should parse")
    ensure(formation["defect_type"] == "vacancy-like", "defect-analysis should infer a vacancy-like defect")
    ensure(formation["species"] == "O" and formation["delta_species"] == -1, "defect-analysis should infer the missing species and count")
    ensure(formation["equilibrium_fraction"] is not None and formation["equilibrium_fraction"] > 0, "defect-analysis should estimate an equilibrium fraction when temperature is provided")
    ensure(formation["abundance_class"] == "trace-like", "defect-analysis should classify the dilute abundance scale")
    qe_formation = run_json("scripts/analyze_defect_formation.py", "fixtures/qe/pristine", "fixtures/qe/defect", "--mu", "-4.0", "--json")
    ensure(abs(qe_formation["formation_energy_eV"] - 2.0) < 1e-4, "QE defect formation energy should parse")
    abinit_formation = run_json("scripts/analyze_defect_formation.py", "fixtures/abinit/pristine", "fixtures/abinit/defect", "--mu", "-4.0", "--json")
    ensure(abs(abinit_formation["formation_energy_eV"] - 2.0) < 1e-4, "ABINIT defect formation energy should parse")
    substitutional = run_json(
        "scripts/analyze_defect_formation.py",
        "fixtures/substitutional/pristine",
        "fixtures/substitutional/defect",
        "--mu-term",
        "Fe=-6.0",
        "--mu-term",
        "Li=-1.5",
        "--json",
    )
    ensure(abs(substitutional["formation_energy_eV"] - 1.5) < 1e-6, "defect-analysis should support multi-species chemical-potential terms")
    ensure("substitutional-like" in substitutional["defect_type"], "defect-analysis should infer a substitutional-like defect")
    sensitivity = run_json(
        "scripts/analyze_defect_sensitivity.py",
        "fixtures/pristine",
        "fixtures/defect",
        "--mu",
        "-4.0",
        "--temperature",
        "300",
        "--temperature",
        "600",
        "--temperature",
        "1000",
        "--site-density-cm3",
        "1e22",
        "--json",
    )
    ensure(sensitivity["sensitivity_class"] == "strong-temperature-sensitivity", "defect-analysis should detect strong abundance sensitivity across temperature")
    structure = run_json("scripts/analyze_defect_structure.py", "fixtures/pristine/POSCAR", "fixtures/defect/POSCAR", "--json")
    ensure(structure["species_delta"]["O"] == -1, "defect structure analysis should detect one missing O atom")
    ensure(structure["relative_volume_change_percent"] > 0, "defect structure analysis should detect positive volume expansion")
    ensure(structure["defect_type"] == "vacancy-like", "defect structure analysis should infer a vacancy-like defect")
    qe_structure = run_json("scripts/analyze_defect_structure.py", "fixtures/qe/pristine", "fixtures/qe/defect", "--json")
    ensure(qe_structure["species_delta"]["O"] == -1, "QE defect structure analysis should detect one missing O atom")
    abinit_structure = run_json("scripts/analyze_defect_structure.py", "fixtures/abinit/pristine", "fixtures/abinit/defect", "--json")
    ensure(abinit_structure["species_delta"]["O"] == -1, "ABINIT defect structure analysis should detect one missing O atom")
    ranked = run_json(
        "scripts/compare_defect_candidates.py",
        "fixtures",
        "fixtures/candidates/high-energy-vacancy",
        "--mu",
        "-4.0",
        "--max-volume-change-percent",
        "5.0",
        "--temperature-k",
        "1000",
        "--site-density-cm3",
        "1e22",
        "--target-defect-type",
        "vacancy-like",
        "--target-concentration-cm3",
        "1e10",
        "--mode",
        "balanced",
        "--json",
    )
    ensure(ranked["best_case"] == "fixtures", "defect-analysis should rank the lower-energy vacancy ahead of the high-energy candidate")
    substitutional_ranked = run_json(
        "scripts/compare_defect_candidates.py",
        "fixtures/substitutional",
        "fixtures",
        "--mu",
        "-4.0",
        "--mu-term",
        "Fe=-6.0",
        "--mu-term",
        "Li=-1.5",
        "--max-volume-change-percent",
        "5.0",
        "--target-defect-type",
        "substitutional-like",
        "--mode",
        "substitutional",
        "--json",
    )
    ensure(substitutional_ranked["best_case"] == "substitutional", "defect-analysis should rank the substitutional candidate first in substitutional mode")
    temp_dir = Path(tempfile.mkdtemp(prefix="defect-analysis-report-"))
    try:
        report_path = Path(
            run(
                "scripts/export_defect_report.py",
                "fixtures/pristine",
                "fixtures/defect",
                "--mu",
                "-4.0",
                "--temperature-k",
                "1000",
                "--output",
                str(temp_dir / "DEFECT_REPORT.md"),
            ).stdout.strip()
        )
        report_text = report_path.read_text()
        ensure("# Defect Analysis Report" in report_text, "defect report should have a heading")
        ensure("Formation energy" in report_text, "defect report should include the formation energy")
        ensure("## Screening Note" in report_text, "defect report should include a screening note")
    finally:
        shutil.rmtree(temp_dir)
    print("defect-analysis regression passed")


if __name__ == "__main__":
    main()
