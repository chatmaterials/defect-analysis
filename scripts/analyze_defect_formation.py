#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from defect_io import equilibrium_fraction, infer_species_and_delta, read_energy


def analyze(
    pristine: Path,
    defect: Path,
    species: str | None,
    delta: int | None,
    mu: float,
    temperature_K: float | None = None,
    site_density_cm3: float | None = None,
) -> dict[str, object]:
    backend_pristine, e_bulk = read_energy(pristine)
    backend_defect, e_def = read_energy(defect)
    if backend_pristine != backend_defect:
        raise SystemExit("Pristine and defect states must use the same backend for direct comparison")
    species, delta, defect_type, delta_map = infer_species_and_delta(pristine, defect, species, delta)
    if species is None or delta is None:
        raise SystemExit("Could not infer species and delta from the pristine/defect pair; provide --species and --delta explicitly")
    e_form = e_def - e_bulk - delta * mu
    fraction = equilibrium_fraction(e_form, temperature_K) if temperature_K is not None else None
    concentration = fraction * site_density_cm3 if fraction is not None and site_density_cm3 is not None else None
    observations = ["Neutral defect formation energy estimated from pristine and defect total energies."]
    observations.append(f"Defect type inferred as `{defect_type}`.")
    return {
        "backend": backend_pristine,
        "pristine": str(pristine),
        "defect": str(defect),
        "species": species,
        "delta_species": delta,
        "species_delta_map": delta_map,
        "defect_type": defect_type,
        "chemical_potential_eV": mu,
        "pristine_energy_eV": e_bulk,
        "defect_energy_eV": e_def,
        "formation_energy_eV": e_form,
        "temperature_K": temperature_K,
        "site_density_cm3": site_density_cm3,
        "equilibrium_fraction": fraction,
        "equilibrium_concentration_cm3": concentration,
        "observations": observations,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate a neutral defect formation energy from two states.")
    parser.add_argument("pristine")
    parser.add_argument("defect")
    parser.add_argument("--species")
    parser.add_argument("--delta", type=int, help="Change in species count: defect minus pristine.")
    parser.add_argument("--mu", type=float, required=True, help="Chemical potential for the species in eV.")
    parser.add_argument("--temperature-k", type=float)
    parser.add_argument("--site-density-cm3", type=float)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze(
        Path(args.pristine).expanduser().resolve(),
        Path(args.defect).expanduser().resolve(),
        args.species,
        args.delta,
        args.mu,
        args.temperature_k,
        args.site_density_cm3,
    )
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
