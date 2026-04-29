import numpy as np
from typing import List, Callable, Tuple
from core.bodies import CelestialBody


def multi_body_derivative(bodies: List[CelestialBody]):
    """
    Create derivative function for multi-body dynamics
    
    Args:
        bodies: List of celestial bodies
        
    Returns:
        function: Derivative function f(t, y)
    """
    def derivative(t: float, y: np.ndarray) -> np.ndarray:
        """
        Calculate derivative for multi-body problem
        
        Args:
            t: Current time (s)
            y: State vector containing positions and velocities of all bodies
                Format: [x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, ...]
            
        Returns:
            numpy array: Derivative of the state vector
        """
        n_bodies = len(bodies)
        state_size = 6  # 3 position + 3 velocity components per body
        
        # Initialize derivative vector
        dy = np.zeros_like(y)
        
        # Extract positions and velocities
        positions = np.reshape(y[:n_bodies*3], (n_bodies, 3))
        velocities = np.reshape(y[n_bodies*3:], (n_bodies, 3))
        
        # Set velocities as the derivative of positions
        dy[:n_bodies*3] = velocities.flatten()
        
        # Calculate accelerations due to gravitational interactions
        accelerations = np.zeros((n_bodies, 3))
        
        for i in range(n_bodies):
            for j in range(n_bodies):
                if i != j:
                    # Calculate vector from body j to body i
                    r_ji = positions[i] - positions[j]
                    r_ji_norm = np.linalg.norm(r_ji)
                    
                    if r_ji_norm > 0:
                        # Calculate gravitational acceleration
                        a = -bodies[j].mu * r_ji / r_ji_norm**3
                        accelerations[i] += a
        
        # Set accelerations as the derivative of velocities
        dy[n_bodies*3:] = accelerations.flatten()
        
        return dy
    
    return derivative


def create_multi_body_state(bodies: List[CelestialBody], initial_states: List[Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
    """
    Create initial state vector for multi-body simulation
    
    Args:
        bodies: List of celestial bodies
        initial_states: List of (position, velocity) tuples for each body
        
    Returns:
        numpy array: Initial state vector
    """
    if len(bodies) != len(initial_states):
        raise ValueError("Number of bodies must match number of initial states")
    
    state = []
    for pos, vel in initial_states:
        state.extend(pos)
        state.extend(vel)
    
    return np.array(state)
