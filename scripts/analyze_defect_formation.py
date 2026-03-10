#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read_energy(path: Path) -> float:
    outcar = path / "OUTCAR" if path.is_dir() else path
    text = outcar.read_text(errors="ignore")
    matches = re.findall(r"TOTEN\s*=\s*([\-0-9.Ee+]+)", text)
    if not matches:
        raise SystemExit(f"No TOTEN found in {outcar}")
    return float(matches[-1])


def analyze(pristine: Path, defect: Path, species: str, delta: int, mu: float) -> dict[str, object]:
    e_bulk = read_energy(pristine)
    e_def = read_energy(defect)
    e_form = e_def - e_bulk - delta * mu
    return {
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
