import numpy as np
from scipy.optimize import root

# Constants
EPS = 1e-12
MAX_ITER = 100

def lambert_solver(r1, r2, tof, mu, prograde=True):
    """
    Solve Lambert's problem
    
    Args:
        r1: Initial position vector (km)
        r2: Final position vector (km)
        tof: Time of flight (s)
        mu: Gravitational parameter (km^3/s^2)
        prograde: True for prograde orbit, False for retrograde
        
    Returns:
        tuple: (v1, v2) - Initial and final velocity vectors
    """
    r1 = np.array(r1)
    r2 = np.array(r2)
    
    r1_norm = np.linalg.norm(r1)
    r2_norm = np.linalg.norm(r2)
    
    # Calculate transfer angle
    cos_dnu = np.dot(r1, r2) / (r1_norm * r2_norm)
    sin_dnu = np.linalg.norm(np.cross(r1, r2)) / (r1_norm * r2_norm)
    dnu = np.arctan2(sin_dnu, cos_dnu)
    
    if not prograde and dnu > 0:
        dnu = 2 * np.pi - dnu
    elif prograde and dnu < 0:
        dnu = 2 * np.pi + dnu
    
    # Calculate chord length
    c = np.linalg.norm(r2 - r1)
    
    # Calculate semi-perimeter
    s = (r1_norm + r2_norm + c) / 2
    
    # Calculate normalized time of flight
    T = np.sqrt(2 * mu / s**3) * tof
    
    # Solve for x using Newton-Raphson
    def f(x):
        if x < 1:
            y = np.sqrt(1 - x**2)
            psi = 2 * np.arcsin(y)
            St = (psi - np.sin(psi)) / y**3
        else:
            y = np.sqrt(x**2 - 1)
            psi = 2 * np.arcsinh(y)
            St = (np.sinh(psi) - psi) / y**3
        
        alpha = 2 * np.arcsin(np.sqrt((s - c) / (2 * s * x**2)))
        if dnu > np.pi:
            alpha = np.pi - alpha
        
        return (s**1.5 / np.sqrt(2 * mu)) * (St - alpha) - tof
    
    # Initial guess
    if dnu < np.pi:
        x0 = 1.0  # Elliptical orbit
    else:
        x0 = 0.1  # Hyperbolic orbit
    
    # Solve
    result = root(f, x0)
    x = result.x[0]
    
    # Calculate intermediate variables
    if x < 1:
        y = np.sqrt(1 - x**2)
        psi = 2 * np.arcsin(y)
        f_val = 1 - (s - r2_norm) * (1 - np.cos(psi)) / (s * x**2)
        g_val = tof - np.sqrt(s**3 / (2 * mu)) * (psi - np.sin(psi)) / y**3
        f_dot = np.sqrt(mu / (2 * s**3)) * (np.sin(psi) - psi) / y**3
        g_dot = 1 - (s - r1_norm) * (1 - np.cos(psi)) / (s * x**2)
    else:
        y = np.sqrt(x**2 - 1)
        psi = 2 * np.arcsinh(y)
        f_val = 1 - (s - r2_norm) * (np.cosh(psi) - 1) / (s * x**2)
        g_val = tof - np.sqrt(s**3 / (2 * mu)) * (np.sinh(psi) - psi) / y**3
        f_dot = np.sqrt(mu / (2 * s**3)) * (psi - np.sinh(psi)) / y**3
        g_dot = 1 - (s - r1_norm) * (np.cosh(psi) - 1) / (s * x**2)
    
    # Calculate velocities
    v1 = (r2 - f_val * r1) / g_val
    v2 = g_dot * v1 - f_dot * r1
    
    return v1, v2