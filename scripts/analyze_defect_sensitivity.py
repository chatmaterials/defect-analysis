#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_defect_formation import analyze as analyze_formation, parse_mu_terms


def classify_sensitivity(span_orders: float) -> str:
    if span_orders >= 10.0:
        return "strong-temperature-sensitivity"
    if span_orders >= 3.0:
        return "moderate-temperature-sensitivity"
    return "weak-temperature-sensitivity"


def analyze(
    pristine: Path,
    defect: Path,
    species: str | None,
    delta: int | None,
    mu: float | None,
    mu_terms: dict[str, float] | None,
    temperatures: list[float],
    site_density_cm3: float | None,
) -> dict[str, object]:
    if not temperatures:
        raise SystemExit("Provide at least one temperature")
    samples = []
    concentrations = []
    for temperature in temperatures:
        payload = analyze_formation(pristine, defect, species, delta, mu, temperature, site_density_cm3, mu_terms)
        concentration = payload["equilibrium_concentration_cm3"]
        samples.append(
            {
                "temperature_K": temperature,
                "formation_energy_eV": payload["formation_energy_eV"],
                "equilibrium_fraction": payload["equilibrium_fraction"],
                "equilibrium_concentration_cm3": concentration,
                "abundance_class": payload["abundance_class"],
            }
        )
        if concentration is not None and concentration > 0.0:
            concentrations.append(float(concentration))
    span_orders = 0.0
    if len(concentrations) >= 2:
        span_orders = abs(__import__("math").log10(max(concentrations) / min(concentrations)))
    return {
        "pristine": str(pristine),
        "defect": str(defect),
        "site_density_cm3": site_density_cm3,
        "temperature_window_K": [min(temperatures), max(temperatures)],
        "samples": samples,
        "concentration_span_orders": span_orders,
        "sensitivity_class": classify_sensitivity(span_orders),
        "observations": [
            "Defect abundance sensitivity was summarized by sweeping the neutral formation model over a temperature window."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze how a defect abundance changes over a temperature window.")
    parser.add_argument("pristine")
    parser.add_argument("defect")
    parser.add_argument("--species")
    parser.add_argument("--delta", type=int)
    parser.add_argument("--mu", type=float)
    parser.add_argument("--mu-term", action="append")
    parser.add_argument("--temperature", type=float, action="append", required=True)
    parser.add_argument("--site-density-cm3", type=float)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.mu is None and not args.mu_term:
        raise SystemExit("Provide either --mu or at least one --mu-term")
    payload = analyze(
        Path(args.pristine).expanduser().resolve(),
        Path(args.defect).expanduser().resolve(),
        args.species,
        args.delta,
        args.mu,
        parse_mu_terms(args.mu_term),
        args.temperature,
        args.site_density_cm3,
    )
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
