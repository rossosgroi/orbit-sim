import numpy as np
from typing import List, Tuple


def calculate_minimum_distance(state1: np.ndarray, state2: np.ndarray, mu: float) -> Tuple[float, float]:
    """
    Calculate minimum distance between two orbiting objects
    
    Args:
        state1: State vector of first object [x, y, z, vx, vy, vz]
        state2: State vector of second object [x, y, z, vx, vy, vz]
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        tuple: (minimum_distance, time_of_minimum_distance)
            minimum_distance: Minimum distance between objects (km)
            time_of_minimum_distance: Time at which minimum distance occurs (s)
    """
    # Relative position and velocity
    r_rel = state1[:3] - state2[:3]
    v_rel = state1[3:] - state2[3:]
    
    # Calculate time of closest approach
    r_rel_mag = np.linalg.norm(r_rel)
    v_rel_mag = np.linalg.norm(v_rel)
    
    if v_rel_mag == 0:
        # Objects are not moving relative to each other
        return r_rel_mag, 0.0
    
    # Time to closest approach
    t_closest = -np.dot(r_rel, v_rel) / v_rel_mag**2
    
    # Calculate minimum distance
    if t_closest < 0:
        # Closest approach already occurred
        return r_rel_mag, 0.0
    else:
        # Calculate position at closest approach
        r_closest = r_rel + v_rel * t_closest
        min_distance = np.linalg.norm(r_closest)
        return min_distance, t_closest


def detect_conjunctions(objects: List[np.ndarray], mu: float, threshold: float = 1.0) -> List[Tuple[int, int, float, float]]:
    """
    Detect potential conjunctions between multiple objects
    
    Args:
        objects: List of state vectors for each object
        mu: Gravitational parameter (km^3/s^2)
        threshold: Distance threshold for conjunction detection (km)
        
    Returns:
        list: List of potential conjunctions
            Each conjunction is a tuple (object1_index, object2_index, min_distance, time_of_conjunction)
    """
    conjunctions = []
    n_objects = len(objects)
    
    # Check all pairs of objects
    for i in range(n_objects):
        for j in range(i+1, n_objects):
            min_distance, t_conj = calculate_minimum_distance(objects[i], objects[j], mu)
            if min_distance < threshold:
                conjunctions.append((i, j, min_distance, t_conj))
    
    return conjunctions


def calculate_probability_of_collision(min_distance: float, position_error: float, object_radius: float = 0.1) -> float:
    """
    Calculate probability of collision
    
    Args:
        min_distance: Minimum distance between objects (km)
        position_error: Position error covariance (km)
        object_radius: Radius of each object (km)
        
    Returns:
        float: Probability of collision
    """
    # Combined radius
    combined_radius = 2 * object_radius
    
    # Sigma (standard deviation) from position error
    sigma = np.sqrt(position_error)
    
    if sigma == 0:
        # No position error, collision if min_distance < combined_radius
        return 1.0 if min_distance < combined_radius else 0.0
    
    # Probability of collision using Gaussian distribution
    # This is a simplified model
    from scipy.stats import norm
    probability = norm.cdf((combined_radius - min_distance) / sigma)
    
    return probability


def conjunction_analysis(objects: List[np.ndarray], mu: float, threshold: float = 1.0, position_error: float = 0.1) -> List[dict]:
    """
    Perform comprehensive conjunction analysis
    
    Args:
        objects: List of state vectors for each object
        mu: Gravitational parameter (km^3/s^2)
        threshold: Distance threshold for conjunction detection (km)
        position_error: Position error covariance (km)
        
    Returns:
        list: List of conjunction events with detailed information
    """
    conjunctions = detect_conjunctions(objects, mu, threshold)
    
    # Add probability of collision to each conjunction
    conjunction_events = []
    for i, j, min_distance, t_conj in conjunctions:
        p_collision = calculate_probability_of_collision(min_distance, position_error)
        conjunction_events.append({
            'object1': i,
            'object2': j,
            'min_distance': min_distance,
            'time_of_conjunction': t_conj,
            'probability_of_collision': p_collision
        })
    
    # Sort by probability of collision (highest first)
    conjunction_events.sort(key=lambda x: x['probability_of_collision'], reverse=True)
    
    return conjunction_events
