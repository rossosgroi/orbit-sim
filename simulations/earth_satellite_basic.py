import numpy as np
from src.core.bodies import EARTH
from src.core.state import State
from src.dynamics.two_body import two_body_derivative, two_body_energy
from src.dynamics.propagator import OrbitPropagator
from src.orbits.conversions import cartesian_to_keplerian
from src.visualization.plot_3d import plot_3d_orbit, plot_energy, plot_orbital_elements
from src.utils.logging import setup_logger, log_simulation_parameters, log_energy_drift
import matplotlib.pyplot as plt

def run_earth_satellite_basic():
    """
    Run basic Earth satellite orbit simulation
    """
    # Setup logger
    logger = setup_logger()
    
    # Simulation parameters
    params = {
        "body": "Earth",
        "mu": EARTH.mu,
        "initial_state": "Circular orbit at 7000 km altitude",
        "t_span": 86400,  # 1 day
        "dt": 60,  # 1 minute
        "integrator": "rk4"
    }
    
    log_simulation_parameters(logger, params)
    
    # Initial state: Circular orbit at 7000 km altitude
    r = 6378.137 + 7000  # km
    v = np.sqrt(EARTH.mu / r)  # km/s
    
    state0 = State([r, 0, 0], [0, v, 0])
    logger.info(f"Initial state: {state0}")
    
    # Create force model and propagator
    force_model = two_body_derivative(EARTH.mu)
    propagator = OrbitPropagator(force_model, params["integrator"])
    
    # Propagate orbit
    logger.info("Propagating orbit...")
    times, states = propagator.propagate(state0.to_vector(), params["t_span"], params["dt"])
    
    # Calculate energy
    energy_fn = lambda state: two_body_energy(EARTH.mu, state)
    times, states, energies = propagator.propagate_with_energy(
        state0.to_vector(), params["t_span"], params["dt"], energy_fn
    )
    
    # Log energy drift
    log_energy_drift(logger, energies[0], energies[-1])
    
    # Calculate orbital elements
    elements = [cartesian_to_keplerian(state, EARTH.mu) for state in states]
    
    # Visualize results
    logger.info("Generating visualizations...")
    
    # 3D orbit plot
    fig1, ax1 = plot_3d_orbit(states, EARTH, "Basic Earth Satellite Orbit")
    
    # Energy conservation plot
    fig2, ax2 = plot_energy(times, energies, "Energy Conservation")
    
    # Orbital elements evolution
    fig3, ax3 = plot_orbital_elements(times, elements, "Orbital Elements Evolution")
    
    # Show plots
    plt.show()
    
    logger.info("Simulation completed successfully!")

if __name__ == "__main__":
    run_earth_satellite_basic()