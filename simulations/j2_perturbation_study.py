import numpy as np
from src.core.bodies import EARTH
from src.core.state import State
from src.dynamics.two_body import two_body_derivative, two_body_energy
from src.dynamics.perturbations import j2_derivative
from src.dynamics.propagator import OrbitPropagator
from src.orbits.conversions import cartesian_to_keplerian
from src.visualization.plot_3d import plot_3d_orbit, plot_energy, plot_orbital_elements
from src.utils.logging import setup_logger, log_simulation_parameters
import matplotlib.pyplot as plt

def run_j2_perturbation_study():
    """
    Run J2 perturbation study
    """
    # Setup logger
    logger = setup_logger()
    
    # Simulation parameters
    params = {
        "body": "Earth",
        "mu": EARTH.mu,
        "j2": EARTH.j2,
        "r_body": EARTH.radius,
        "initial_state": "Sun-synchronous orbit candidate",
        "t_span": 86400 * 3,  # 3 days
        "dt": 60,  # 1 minute
        "integrator": "rk4"
    }
    
    log_simulation_parameters(logger, params)
    
    # Initial state: Sun-synchronous orbit candidate
    # Semi-major axis
    a = 6378.137 + 700  # 700 km altitude
    # Inclination for sun-synchronous orbit
    # Approximate value, actual calculation more complex
    i = 98.6 * np.pi / 180  # ~98.6 degrees
    # Circular orbit
    e = 0.0
    
    # Calculate circular orbit velocity
    v = np.sqrt(EARTH.mu / a)
    
    # Initial state vector
    state0 = State([a, 0, 0], [0, v * np.cos(i), v * np.sin(i)])
    logger.info(f"Initial state: {state0}")
    
    # Create force models
    force_model_two_body = two_body_derivative(EARTH.mu)
    force_model_j2 = j2_derivative(EARTH.mu, EARTH.radius, EARTH.j2)
    
    # Create propagators
    propagator_two_body = OrbitPropagator(force_model_two_body, params["integrator"])
    propagator_j2 = OrbitPropagator(force_model_j2, params["integrator"])
    
    # Propagate with two-body model
    logger.info("Propagating with two-body model...")
    times_tb, states_tb = propagator_two_body.propagate(
        state0.to_vector(), params["t_span"], params["dt"]
    )
    
    # Propagate with J2 model
    logger.info("Propagating with J2 model...")
    times_j2, states_j2 = propagator_j2.propagate(
        state0.to_vector(), params["t_span"], params["dt"]
    )
    
    # Calculate energy for J2 model
    energy_fn = lambda state: two_body_energy(EARTH.mu, state)
    times_j2, states_j2, energies_j2 = propagator_j2.propagate_with_energy(
        state0.to_vector(), params["t_span"], params["dt"], energy_fn
    )
    
    # Calculate orbital elements
    elements_j2 = [cartesian_to_keplerian(state, EARTH.mu) for state in states_j2]
    
    # Visualize results
    logger.info("Generating visualizations...")
    
    # 3D orbit plot (J2 model)
    fig1, ax1 = plot_3d_orbit(states_j2, EARTH, "Orbit with J2 Perturbation")
    
    # Energy conservation plot
    fig2, ax2 = plot_energy(times_j2, energies_j2, "Energy Conservation with J2")
    
    # Orbital elements evolution
    fig3, ax3 = plot_orbital_elements(times_j2, elements_j2, "Orbital Elements Evolution with J2")
    
    # Show plots
    plt.show()
    
    logger.info("Simulation completed successfully!")

if __name__ == "__main__":
    run_j2_perturbation_study()