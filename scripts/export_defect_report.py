#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from analyze_defect_formation import analyze as analyze_formation
from analyze_defect_structure import analyze as analyze_structure


def screening_note(formation: dict[str, object], structure: dict[str, object]) -> str:
    e_form = float(formation["formation_energy_eV"])
    strain = abs(float(structure["relative_volume_change_percent"]))
    abundance = formation.get("abundance_class")
    if e_form <= 1.0 and strain <= 5.0:
        return "This defect looks relatively accessible in a compact neutral-defect screen: low formation energy and limited structural swelling."
    if e_form > 2.5:
        return "The neutral formation energy is high enough that this defect is unlikely to be abundant without strong thermodynamic driving forces."
    if abundance == "trace-like":
        return "This defect is thermodynamically allowed in the compact model, but the estimated abundance remains trace-like under the supplied conditions."
    if strain > 10.0:
        return "The structural response is large enough that local strain accommodation may be important."
    return "The defect is intermediate in this compact screen and may need charged-defect or concentration analysis before stronger claims."


def render_markdown(formation: dict[str, object], structure: dict[str, object]) -> str:
    lines = [
        "# Defect Analysis Report",
        "",
        "## Formation Energy",
        f"- Defect type: `{formation['defect_type']}`",
        f"- Species: `{formation['species']}`",
        f"- Delta species: `{formation['delta_species']}`",
        f"- Chemical potential terms: `{formation['chemical_potential_terms']}`",
        f"- Formation energy (eV): `{formation['formation_energy_eV']:.4f}`",
        f"- Equilibrium fraction: `{formation['equilibrium_fraction']:.4e}`" if formation["equilibrium_fraction"] is not None else "- Equilibrium fraction: `n/a`",
        f"- Equilibrium concentration (cm^-3): `{formation['equilibrium_concentration_cm3']:.4e}`" if formation["equilibrium_concentration_cm3"] is not None else "- Equilibrium concentration (cm^-3): `n/a`",
        f"- Abundance class: `{formation['abundance_class']}`" if formation["abundance_class"] is not None else "- Abundance class: `n/a`",
        "",
        "## Structural Change",
        f"- Pristine atoms: `{structure['natoms_pristine']}`",
        f"- Defect atoms: `{structure['natoms_defect']}`",
        f"- Relative volume change (%): `{structure['relative_volume_change_percent']:.4f}`",
        f"- Volume change per changed atom (A^3): `{structure['volume_change_per_changed_atom_A3']:.4f}`" if structure["volume_change_per_changed_atom_A3"] is not None else "- Volume change per changed atom (A^3): `n/a`",
        f"- Species delta: `{structure['species_delta']}`",
    ]
    lines.extend(["", "## Screening Note", f"- {screening_note(formation, structure)}"])
    return "\n".join(lines).rstrip() + "\n"


def default_output(source: Path) -> Path:
    return source / "DEFECT_REPORT.md" if source.is_dir() else source.parent / "DEFECT_REPORT.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a markdown defect-analysis report.")
    parser.add_argument("pristine")
    parser.add_argument("defect")
    parser.add_argument("--species")
    parser.add_argument("--delta", type=int)
    parser.add_argument("--mu", type=float, required=True)
    parser.add_argument("--temperature-k", type=float)
    parser.add_argument("--site-density-cm3", type=float)
    parser.add_argument("--output")
    args = parser.parse_args()
    pristine = Path(args.pristine).expanduser().resolve()
    defect = Path(args.defect).expanduser().resolve()
    formation = analyze_formation(pristine, defect, args.species, args.delta, args.mu, args.temperature_k, args.site_density_cm3)
    structure = analyze_structure(pristine, defect)
    output = Path(args.output).expanduser().resolve() if args.output else default_output(defect.parent)
    output.write_text(render_markdown(formation, structure))
    print(output)


if __name__ == "__main__":
    main()
