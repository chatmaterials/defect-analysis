#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from defect_io import read_energy


def analyze(pristine: Path, defect: Path, species: str, delta: int, mu: float) -> dict[str, object]:
    backend_pristine, e_bulk = read_energy(pristine)
    backend_defect, e_def = read_energy(defect)
    if backend_pristine != backend_defect:
        raise SystemExit("Pristine and defect states must use the same backend for direct comparison")
    e_form = e_def - e_bulk - delta * mu
    return {
        "backend": backend_pristine,
        "pristine": str(pristine),
        "defect": str(defect),
        "species": species,
        "delta_species": delta,
        "chemical_potential_eV": mu,
        "pristine_energy_eV": e_bulk,
        "defect_energy_eV": e_def,
        "formation_energy_eV": e_form,
        "observations": ["Neutral defect formation energy estimated from pristine and defect total energies."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate a neutral defect formation energy from two states.")
    parser.add_argument("pristine")
    parser.add_argument("defect")
    parser.add_argument("--species", required=True)
    parser.add_argument("--delta", type=int, required=True, help="Change in species count: defect minus pristine.")
    parser.add_argument("--mu", type=float, required=True, help="Chemical potential for the species in eV.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze(
        Path(args.pristine).expanduser().resolve(),
        Path(args.defect).expanduser().resolve(),
        args.species,
        args.delta,
        args.mu,
    )
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
