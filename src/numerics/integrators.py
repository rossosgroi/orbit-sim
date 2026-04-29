import numpy as np
from typing import Callable, Union, List, Tuple

# Try to import Numba for JIT compilation
try:
    from numba import jit, njit
except ImportError:
    # Numba not installed, use regular functions
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    njit = jit


def rk4_step(f: Callable[[float, np.ndarray], np.ndarray], t: float, y: np.ndarray, dt: float) -> np.ndarray:
    """
    Fourth-order Runge-Kutta integration step
    
    Args:
        f: Function returning derivative dy/dt
        t: Current time
        y: Current state vector
        dt: Time step
        
    Returns:
        numpy array: New state vector after time step
    """
    k1 = f(t, y)
    k2 = f(t + dt/2, y + dt*k1/2)
    k3 = f(t + dt/2, y + dt*k2/2)
    k4 = f(t + dt, y + dt*k3)
    return y + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)


def rk45_step(f: Callable[[float, np.ndarray], np.ndarray], t: float, y: np.ndarray, dt: float) -> Tuple[np.ndarray, float]:
    """
    Fifth-order Runge-Kutta integration step (Cash-Karp)
    
    Args:
        f: Function returning derivative dy/dt
        t: Current time
        y: Current state vector
        dt: Time step
        
    Returns:
        tuple: (new_state, error_estimate)
    """
    # Cash-Karp coefficients
    a = np.array([0, 1/5, 3/10, 3/5, 1, 7/8])
    b = np.array([
        [0, 0, 0, 0, 0],
        [1/5, 0, 0, 0, 0],
        [3/40, 9/40, 0, 0, 0],
        [3/10, -9/10, 6/5, 0, 0],
        [-11/54, 5/2, -70/27, 35/27, 0],
        [1631/55296, 175/512, 575/13824, 44275/110592, 253/4096]
    ])
    c4 = np.array([37/378, 0, 250/621, 125/594, 0, 512/1771])
    c5 = np.array([2825/27648, 0, 18575/48384, 13525/55296, 277/14336, 1/4])
    
    # Calculate k vectors
    n = len(y)
    k = np.zeros((6, n))
    k[0] = f(t, y)
    
    for i in range(1, 6):
        y_temp = y.copy()
        for j in range(i):
            y_temp += dt * b[i][j] * k[j]
        k[i] = f(t + a[i] * dt, y_temp)
    
    # Calculate fourth and fifth order solutions using vectorized operations
    y4 = y + dt * np.dot(c4, k)
    y5 = y + dt * np.dot(c5, k)
    
    # Error estimate
    error = np.linalg.norm(y5 - y4)
    
    return y5, error


def adaptive_rk45(f: Callable[[float, Union[List[float], np.ndarray]], np.ndarray], t: float, y: Union[List[float], np.ndarray], dt: float, tol: float = 1e-6) -> Tuple[np.ndarray, float, float]:
    """
    Adaptive step size Runge-Kutta 4/5
    
    Args:
        f: Function returning derivative dy/dt
        t: Current time
        y: Current state vector
        dt: Initial time step
        tol: Error tolerance
        
    Returns:
        tuple: (new_state, new_time, new_dt)
    """
    # Safety factor
    SAFETY = 0.9
    MIN_FACTOR = 0.1
    MAX_FACTOR = 4.0
    
    # Convert to numpy array for consistency
    y = np.asarray(y)
    
    while True:
        y_new, error = rk45_step(f, t, y, dt)
        
        if error < 1e-12:
            # No error, take a big step
            new_dt = min(MAX_FACTOR * dt, 10.0)
            break
        
        # Calculate step size scaling factor
        scale = (tol / error) ** 0.2
        new_dt = SAFETY * dt * scale
        
        # Limit step size changes
        new_dt = min(new_dt, MAX_FACTOR * dt)
        new_dt = max(new_dt, MIN_FACTOR * dt)
        
        if error < tol:
            break
        
        dt = new_dt
    
    return y_new, t + dt, new_dt