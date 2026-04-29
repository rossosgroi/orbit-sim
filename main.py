#!/usr/bin/env python3
import argparse
from simulations.earth_satellite_basic import run_earth_satellite_basic
from simulations.hohmann_transfer import run_hohmann_transfer
from simulations.j2_perturbation_study import run_j2_perturbation_study
from tests.test_energy_conservation import test_energy_conservation, test_energy_conservation_adaptive
from tests.test_orbit_period import test_circular_orbit_period, test_elliptical_orbit_period

def main():
    """
    Main entry point for the orbital mechanics simulator
    """
    parser = argparse.ArgumentParser(description="Orbital Mechanics Simulator")
    
    parser.add_argument(
        "--scenario",
        choices=["earth_satellite", "hohmann_transfer", "j2_perturbation", "test"],
        default="earth_satellite",
        help="Simulation scenario to run"
    )
    
    parser.add_argument(
        "--test",
        choices=["energy", "period", "all"],
        default="all",
        help="Test to run (only applicable when scenario=test)"
    )
    
    args = parser.parse_args()
    
    if args.scenario == "earth_satellite":
        run_earth_satellite_basic()
    elif args.scenario == "hohmann_transfer":
        run_hohmann_transfer()
    elif args.scenario == "j2_perturbation":
        run_j2_perturbation_study()
    elif args.scenario == "test":
        if args.test == "energy" or args.test == "all":
            test_energy_conservation()
            test_energy_conservation_adaptive()
        if args.test == "period" or args.test == "all":
            test_circular_orbit_period()
            test_elliptical_orbit_period()
        if args.test == "all":
            print("All tests passed!")

if __name__ == "__main__":
    main()