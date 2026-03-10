#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_defect_formation import analyze as analyze_formation
from analyze_defect_structure import analyze as analyze_structure


def analyze_case(
    root: Path,
    mu: float,
    species: str | None,
    delta: int | None,
    max_volume_change_percent: float,
) -> dict[str, object]:
    pristine = root / "pristine"
    defect = root / "defect"
    formation = analyze_formation(pristine, defect, species, delta, mu)
    structure = analyze_structure(pristine, defect)
    formation_penalty = max(0.0, float(formation["formation_energy_eV"]))
    strain_penalty = max(0.0, abs(float(structure["relative_volume_change_percent"])) - max_volume_change_percent) / 5.0
    score = formation_penalty + strain_penalty
    return {
        "case": root.name,
        "path": str(root),
        "defect_type": formation["defect_type"],
        "species": formation["species"],
        "delta_species": formation["delta_species"],
        "formation_energy_eV": formation["formation_energy_eV"],
        "relative_volume_change_percent": structure["relative_volume_change_percent"],
        "formation_penalty": formation_penalty,
        "strain_penalty": strain_penalty,
        "screening_score": score,
    }


def analyze_cases(
    roots: list[Path],
    mu: float,
    species: str | None,
    delta: int | None,
    max_volume_change_percent: float,
) -> dict[str, object]:
    cases = [analyze_case(root, mu, species, delta, max_volume_change_percent) for root in roots]
    ranked = sorted(cases, key=lambda item: item["screening_score"])
    return {
        "chemical_potential_eV": mu,
        "max_volume_change_percent": max_volume_change_percent,
        "ranking_basis": "screening_score = formation_penalty + strain_penalty",
        "cases": ranked,
        "best_case": ranked[0]["case"] if ranked else None,
        "observations": [
            "This is a compact neutral-defect screening heuristic intended for candidate ranking, not a charged-defect thermodynamic treatment."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank defect candidates with a compact formation-plus-strain heuristic.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--mu", type=float, required=True)
    parser.add_argument("--species")
    parser.add_argument("--delta", type=int)
    parser.add_argument("--max-volume-change-percent", type=float, default=5.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze_cases(
        [Path(path).expanduser().resolve() for path in args.paths],
        args.mu,
        args.species,
        args.delta,
        args.max_volume_change_percent,
    )
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
