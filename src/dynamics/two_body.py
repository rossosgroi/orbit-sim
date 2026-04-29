import numpy as np
from typing import Callable, Union, List
from src.core.exceptions import ForceModelError


def two_body_derivative(mu: float) -> Callable[[float, Union[List[float], np.ndarray]], np.ndarray]:
    """
    Create derivative function for two-body problem
    
    Args:
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        function: Derivative function f(t, y)
    """
    def derivative(t: float, y: Union[List[float], np.ndarray]) -> np.ndarray:
        """
        Calculate derivative for two-body problem
        
        Args:
            t: Current time (s)
            y: State vector [x, y, z, vx, vy, vz]
            
        Returns:
            numpy array: Derivative [vx, vy, vz, ax, ay, az]
        """
        r = y[:3]
        v = y[3:]
        
        r_norm = np.linalg.norm(r)
        if r_norm == 0:
            raise ForceModelError("Position vector cannot be zero")
        
        a = -mu * r / r_norm**3
        
        return np.concatenate([v, a])
    
    return derivative

def two_body_energy(mu: float, state: Union[List[float], np.ndarray]) -> float:
    """
    Calculate total energy for two-body problem
    
    Args:
        mu: Gravitational parameter (km^3/s^2)
        state: State vector [x, y, z, vx, vy, vz]
        
    Returns:
        float: Total energy per unit mass (km^2/s^2)
    """
    r = state[:3]
    v = state[3:]
    
    r_norm = np.linalg.norm(r)
    v_norm_sq = np.dot(v, v)
    
    kinetic = 0.5 * v_norm_sq
    
    # Handle zero radius case to avoid division by zero
    if r_norm > 0:
        potential = -mu / r_norm
    else:
        potential = -np.inf
    
    return kinetic + potential