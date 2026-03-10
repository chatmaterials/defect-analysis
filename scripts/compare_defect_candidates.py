#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_defect_formation import analyze as analyze_formation, parse_mu_terms
from analyze_defect_structure import analyze as analyze_structure


def analyze_case(
    root: Path,
    mu: float | None,
    species: str | None,
    delta: int | None,
    max_volume_change_percent: float,
    mu_terms: dict[str, float] | None,
    temperature_K: float | None,
    site_density_cm3: float | None,
    target_defect_type: str | None,
    target_concentration_cm3: float | None,
) -> dict[str, object]:
    pristine = root / "pristine"
    defect = root / "defect"
    formation = analyze_formation(pristine, defect, species, delta, mu, temperature_K, site_density_cm3, mu_terms)
    structure = analyze_structure(pristine, defect)
    formation_penalty = max(0.0, float(formation["formation_energy_eV"]))
    strain_penalty = max(0.0, abs(float(structure["relative_volume_change_percent"])) - max_volume_change_percent) / 5.0
    type_penalty = 0.0 if target_defect_type is None or formation["defect_type"].startswith(target_defect_type) else 2.0
    concentration = formation["equilibrium_concentration_cm3"]
    abundance_penalty = 0.0
    if target_concentration_cm3 is not None:
        abundance_penalty = max(0.0, target_concentration_cm3 - (float(concentration) if concentration is not None else 0.0)) / target_concentration_cm3
    score = formation_penalty + strain_penalty + type_penalty + abundance_penalty
    return {
        "case": root.name,
        "path": str(root),
        "defect_type": formation["defect_type"],
        "species": formation["species"],
        "delta_species": formation["delta_species"],
        "formation_energy_eV": formation["formation_energy_eV"],
        "equilibrium_concentration_cm3": concentration,
        "abundance_class": formation["abundance_class"],
        "relative_volume_change_percent": structure["relative_volume_change_percent"],
        "formation_penalty": formation_penalty,
        "strain_penalty": strain_penalty,
        "type_penalty": type_penalty,
        "abundance_penalty": abundance_penalty,
        "screening_score": score,
    }


def analyze_cases(
    roots: list[Path],
    mu: float | None,
    species: str | None,
    delta: int | None,
    max_volume_change_percent: float,
    mu_terms: dict[str, float] | None,
    temperature_K: float | None,
    site_density_cm3: float | None,
    target_defect_type: str | None,
    target_concentration_cm3: float | None,
) -> dict[str, object]:
    cases = [
        analyze_case(root, mu, species, delta, max_volume_change_percent, mu_terms, temperature_K, site_density_cm3, target_defect_type, target_concentration_cm3)
        for root in roots
    ]
    ranked = sorted(cases, key=lambda item: item["screening_score"])
    return {
        "chemical_potential_eV": mu,
        "chemical_potential_terms": mu_terms,
        "max_volume_change_percent": max_volume_change_percent,
        "ranking_basis": "screening_score = formation_penalty + strain_penalty + type_penalty + abundance_penalty",
        "cases": ranked,
        "best_case": ranked[0]["case"] if ranked else None,
        "observations": [
            "This is a compact neutral-defect screening heuristic intended for candidate ranking, not a charged-defect thermodynamic treatment."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank defect candidates with a compact formation-plus-strain heuristic.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--mu", type=float)
    parser.add_argument("--mu-term", action="append")
    parser.add_argument("--species")
    parser.add_argument("--delta", type=int)
    parser.add_argument("--max-volume-change-percent", type=float, default=5.0)
    parser.add_argument("--temperature-k", type=float)
    parser.add_argument("--site-density-cm3", type=float)
    parser.add_argument("--target-defect-type")
    parser.add_argument("--target-concentration-cm3", type=float)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.mu is None and not args.mu_term:
        raise SystemExit("Provide either --mu or at least one --mu-term")
    payload = analyze_cases(
        [Path(path).expanduser().resolve() for path in args.paths],
        args.mu,
        args.species,
        args.delta,
        args.max_volume_change_percent,
        parse_mu_terms(args.mu_term),
        args.temperature_k,
        args.site_density_cm3,
        args.target_defect_type,
        args.target_concentration_cm3,
    )
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
