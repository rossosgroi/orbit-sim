import numpy as np
from ..core.constants import DEG2RAD, RAD2DEG
from .elements import KeplerianElements

def cartesian_to_keplerian(state, mu):
    """
    Convert Cartesian state to Keplerian elements
    
    Args:
        state: State vector [x, y, z, vx, vy, vz]
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        KeplerianElements: Keplerian orbital elements
    """
    r = state[:3]
    v = state[3:]
    
    # Calculate vectors
    r_norm = np.linalg.norm(r)
    v_norm = np.linalg.norm(v)
    
    # Specific angular momentum
    h = np.cross(r, v)
    h_norm = np.linalg.norm(h)
    
    # Inclination
    i = np.arccos(h[2] / h_norm)
    
    # Eccentricity vector
    e_vec = (1/mu) * ((v_norm**2 - mu/r_norm) * r - np.dot(r, v) * v)
    e = np.linalg.norm(e_vec)
    
    # Right ascension of ascending node
    if h[0] == 0 and h[1] == 0:
        raan = 0.0  # Equatorial orbit
    else:
        raan = np.arctan2(h[0], -h[1])
        if raan < 0:
            raan += 2 * np.pi
    
    # Argument of perigee
    if e == 0:
        argp = 0.0  # Circular orbit
    else:
        # Node vector
        n = np.cross(np.array([0, 0, 1]), h)
        n_norm = np.linalg.norm(n)
        
        if n_norm == 0:
            argp = 0.0  # Polar orbit
        else:
            argp = np.arccos(np.dot(n, e_vec) / (n_norm * e))
            if e_vec[2] < 0:
                argp = 2 * np.pi - argp
    
    # True anomaly
    if e == 0:
        nu = 0.0  # Circular orbit
    else:
        nu = np.arccos(np.dot(e_vec, r) / (e * r_norm))
        if np.dot(r, v) < 0:
            nu = 2 * np.pi - nu
    
    # Semi-major axis
    if e == 1:
        a = float('inf')  # Parabolic orbit
    else:
        a = 1 / (2/r_norm - v_norm**2/mu)
    
    return KeplerianElements(a, e, i, raan, argp, nu)

def keplerian_to_cartesian(elements, mu):
    """
    Convert Keplerian elements to Cartesian state
    
    Args:
        elements: KeplerianElements object
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        numpy array: Cartesian state vector [x, y, z, vx, vy, vz]
    """
    a = elements.a
    e = elements.e
    i = elements.i
    raan = elements.raan
    argp = elements.argp
    nu = elements.nu
    
    # Calculate periapsis distance
    p = a * (1 - e**2)
    
    # True anomaly to eccentric anomaly
    if e < 1:
        E = 2 * np.arctan2(np.sqrt(1 - e) * np.tan(nu/2), np.sqrt(1 + e))
    else:
        E = 2 * np.arctanh(np.sqrt(e - 1) * np.tan(nu/2))
    
    # Distance from primary
    r = p / (1 + e * np.cos(nu))
    
    # Position in perifocal frame
    r_perifocal = np.array([r * np.cos(nu), r * np.sin(nu), 0])
    
    # Velocity in perifocal frame
    v_perifocal = np.sqrt(mu / p) * np.array([-np.sin(nu), e + np.cos(nu), 0])
    
    # Rotation matrices
    # 1. Rotate by argument of perigee
    cos_argp = np.cos(argp)
    sin_argp = np.sin(argp)
    R_argp = np.array([
        [cos_argp, -sin_argp, 0],
        [sin_argp, cos_argp, 0],
        [0, 0, 1]
    ])
    
    # 2. Rotate by inclination
    cos_i = np.cos(i)
    sin_i = np.sin(i)
    R_i = np.array([
        [1, 0, 0],
        [0, cos_i, -sin_i],
        [0, sin_i, cos_i]
    ])
    
    # 3. Rotate by RAAN
    cos_raan = np.cos(raan)
    sin_raan = np.sin(raan)
    R_raan = np.array([
        [cos_raan, -sin_raan, 0],
        [sin_raan, cos_raan, 0],
        [0, 0, 1]
    ])
    
    # Combined rotation matrix
    R = R_raan @ R_i @ R_argp
    
    # Transform to ECI frame
    r_eci = R @ r_perifocal
    v_eci = R @ v_perifocal
    
    return np.concatenate([r_eci, v_eci])