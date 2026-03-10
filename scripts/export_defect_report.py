#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from analyze_defect_formation import analyze as analyze_formation
from analyze_defect_structure import analyze as analyze_structure


def render_markdown(formation: dict[str, object], structure: dict[str, object]) -> str:
    lines = [
        "# Defect Analysis Report",
        "",
        "## Formation Energy",
        f"- Species: `{formation['species']}`",
        f"- Delta species: `{formation['delta_species']}`",
        f"- Chemical potential (eV): `{formation['chemical_potential_eV']:.4f}`",
        f"- Formation energy (eV): `{formation['formation_energy_eV']:.4f}`",
        "",
        "## Structural Change",
        f"- Pristine atoms: `{structure['natoms_pristine']}`",
        f"- Defect atoms: `{structure['natoms_defect']}`",
        f"- Relative volume change (%): `{structure['relative_volume_change_percent']:.4f}`",
        f"- Species delta: `{structure['species_delta']}`",
    ]
    return "\n".join(lines).rstrip() + "\n"


def default_output(source: Path) -> Path:
    return source / "DEFECT_REPORT.md" if source.is_dir() else source.parent / "DEFECT_REPORT.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a markdown defect-analysis report.")
    parser.add_argument("pristine")
    parser.add_argument("defect")
    parser.add_argument("--species", required=True)
    parser.add_argument("--delta", type=int, required=True)
    parser.add_argument("--mu", type=float, required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    pristine = Path(args.pristine).expanduser().resolve()
    defect = Path(args.defect).expanduser().resolve()
    formation = analyze_formation(pristine, defect, args.species, args.delta, args.mu)
    structure = analyze_structure(pristine / "POSCAR" if pristine.is_dir() else pristine, defect / "POSCAR" if defect.is_dir() else defect)
    output = Path(args.output).expanduser().resolve() if args.output else default_output(defect.parent)
    output.write_text(render_markdown(formation, structure))
    print(output)


if __name__ == "__main__":
    main()
