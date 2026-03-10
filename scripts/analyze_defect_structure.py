#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from defect_io import read_structure, volume


def analyze(pristine: Path, defect: Path) -> dict[str, object]:
    backend_a, a = read_structure(pristine)
    backend_b, b = read_structure(defect)
    if backend_a != backend_b:
        raise SystemExit("Pristine and defect structures must use the same backend for direct comparison")
    vol_a = volume(a["lattice"])
    vol_b = volume(b["lattice"])
    species_delta = {}
    all_species = sorted(set(a["species"]) | set(b["species"]))
    for specie in all_species:
        count_a = a["counts"][a["species"].index(specie)] if specie in a["species"] else 0
        count_b = b["counts"][b["species"].index(specie)] if specie in b["species"] else 0
        species_delta[specie] = count_b - count_a
    return {
        "backend": backend_a,
        "pristine": str(pristine),
        "defect": str(defect),
        "natoms_pristine": a["natoms"],
        "natoms_defect": b["natoms"],
        "volume_initial_A3": vol_a,
        "volume_final_A3": vol_b,
        "relative_volume_change_percent": (vol_b - vol_a) / vol_a * 100.0,
        "species_delta": species_delta,
        "observations": ["Structural and stoichiometric changes were summarized from the two POSCAR-like structures."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare pristine and defect structures.")
    parser.add_argument("pristine")
    parser.add_argument("defect")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze(Path(args.pristine).expanduser().resolve(), Path(args.defect).expanduser().resolve())
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
