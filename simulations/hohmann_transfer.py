import numpy as np
from src.core.bodies import EARTH
from src.core.state import State
from src.dynamics.two_body import two_body_derivative, two_body_energy
from src.dynamics.propagator import OrbitPropagator
from src.orbits.conversions import cartesian_to_keplerian
from src.visualization.plot_3d import plot_3d_orbit, plot_energy
from src.utils.logging import setup_logger, log_simulation_parameters
import matplotlib.pyplot as plt

def calculate_hohmann_maneuver(r1, r2, mu):
    """
    Calculate Hohmann transfer delta-v
    
    Args:
        r1: Initial orbit radius (km)
        r2: Final orbit radius (km)
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        tuple: (v1, v_trans, v2, dv1, dv2)
            v1: Initial orbit velocity
            v_trans: Transfer orbit velocity at periapsis
            v2: Final orbit velocity
            dv1: First delta-v
            dv2: Second delta-v
    """
    # Initial orbit velocity
    v1 = np.sqrt(mu / r1)
    
    # Transfer orbit semi-major axis
    a_trans = (r1 + r2) / 2
    
    # Transfer orbit velocities
    v_trans_periapsis = np.sqrt(mu * (2/r1 - 1/a_trans))
    v_trans_apoapsis = np.sqrt(mu * (2/r2 - 1/a_trans))
    
    # Final orbit velocity
    v2 = np.sqrt(mu / r2)
    
    # Delta-v calculations
    dv1 = v_trans_periapsis - v1
    dv2 = v2 - v_trans_apoapsis
    
    return v1, v_trans_periapsis, v2, dv1, dv2

def run_hohmann_transfer():
    """
    Run Hohmann transfer simulation
    """
    # Setup logger
    logger = setup_logger()
    
    # Simulation parameters
    params = {
        "body": "Earth",
        "mu": EARTH.mu,
        "initial_orbit": "LEO (7000 km altitude)",
        "final_orbit": "GEO (35786 km altitude)",
        "t_span": 3600 * 6,  # 6 hours
        "dt": 60,  # 1 minute
        "integrator": "rk4"
    }
    
    log_simulation_parameters(logger, params)
    
    # Orbit radii
    r1 = 6378.137 + 7000  # LEO
    r2 = 6378.137 + 35786  # GEO
    
    # Calculate Hohmann transfer
    v1, v_trans, v2, dv1, dv2 = calculate_hohmann_maneuver(r1, r2, EARTH.mu)
    
    logger.info(f"Initial orbit velocity: {v1:.3f} km/s")
    logger.info(f"Transfer orbit periapsis velocity: {v_trans:.3f} km/s")
    logger.info(f"Final orbit velocity: {v2:.3f} km/s")
    logger.info(f"Delta-v1: {dv1:.3f} km/s")
    logger.info(f"Delta-v2: {dv2:.3f} km/s")
    logger.info(f"Total delta-v: {dv1 + dv2:.3f} km/s")
    
    # Initial state (LEO)
    state0 = State([r1, 0, 0], [0, v1, 0])
    
    # Apply first delta-v
    state_trans = State([r1, 0, 0], [0, v_trans, 0])
    
    # Create force model and propagator
    force_model = two_body_derivative(EARTH.mu)
    propagator = OrbitPropagator(force_model, params["integrator"])
    
    # Propagate transfer orbit
    logger.info("Propagating transfer orbit...")
    times, states = propagator.propagate(state_trans.to_vector(), params["t_span"], params["dt"])
    
    # Calculate energy
    energy_fn = lambda state: two_body_energy(EARTH.mu, state)
    times, states, energies = propagator.propagate_with_energy(
        state_trans.to_vector(), params["t_span"], params["dt"], energy_fn
    )
    
    # Visualize results
    logger.info("Generating visualizations...")
    
    # 3D orbit plot
    fig1, ax1 = plot_3d_orbit(states, EARTH, "Hohmann Transfer Orbit")
    
    # Energy conservation plot
    fig2, ax2 = plot_energy(times, energies, "Energy Conservation during Transfer")
    
    # Show plots
    plt.show()
    
    logger.info("Simulation completed successfully!")

if __name__ == "__main__":
    run_hohmann_transfer()