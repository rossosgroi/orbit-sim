import numpy as np
import pytest
from src.core.bodies import EARTH
from src.core.state import State
from src.dynamics.two_body import two_body_derivative
from src.dynamics.propagator import OrbitPropagator
from src.orbits.conversions import cartesian_to_keplerian

def test_circular_orbit_period():
    """
    Test circular orbit period
    """
    # Initial state: Circular orbit at 7000 km altitude
    r = 6378.137 + 7000  # km
    v = np.sqrt(EARTH.mu / r)  # km/s
    state0 = State([r, 0, 0], [0, v, 0])
    
    # Create force model and propagator
    force_model = two_body_derivative(EARTH.mu)
    propagator = OrbitPropagator(force_model, 'rk4')
    
    # Theoretical period
    T_theoretical = 2 * np.pi * np.sqrt(r**3 / EARTH.mu)
    
    # Propagate for one period
    t_span = T_theoretical
    dt = 60  # 1 minute
    
    times, states = propagator.propagate(state0.to_vector(), t_span, dt)
    
    # Calculate final state
    final_state = State(states[-1][:3], states[-1][3:])
    
    # Check if satellite returns to near initial position
    position_error = np.linalg.norm(final_state.position - state0.position)
    
    # Position error should be less than 200 km
    assert position_error < 200, f"Satellite not returned to initial position: {position_error:.2f} km"
    
    print(f"Circular orbit period test passed! Position error: {position_error:.2f} km")

def test_elliptical_orbit_period():
    """
    Test elliptical orbit period
    """
    # Initial state: Elliptical orbit
    a = 6378.137 + 10000  # km
    e = 0.5
    r = a * (1 - e)  # Periapsis
    v = np.sqrt(EARTH.mu * (2/r - 1/a))  # Periapsis velocity
    state0 = State([r, 0, 0], [0, v, 0])
    
    # Create force model and propagator
    force_model = two_body_derivative(EARTH.mu)
    propagator = OrbitPropagator(force_model, 'rk4')
    
    # Theoretical period
    T_theoretical = 2 * np.pi * np.sqrt(a**3 / EARTH.mu)
    
    # Propagate for one period
    t_span = T_theoretical
    dt = 60  # 1 minute
    
    times, states = propagator.propagate(state0.to_vector(), t_span, dt)
    
    # Calculate final state
    final_state = State(states[-1][:3], states[-1][3:])
    
    # Check if satellite returns to near initial position
    position_error = np.linalg.norm(final_state.position - state0.position)
    
    # Position error should be less than 200 km
    assert position_error < 200, f"Satellite not returned to initial position: {position_error:.2f} km"
    
    print(f"Elliptical orbit period test passed! Position error: {position_error:.2f} km")

if __name__ == "__main__":
    test_circular_orbit_period()
    test_elliptical_orbit_period()
    print("All orbit period tests passed!")