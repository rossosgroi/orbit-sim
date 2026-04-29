import numpy as np

def calculate_energy_error(initial_energy, final_energy):
    """
    Calculate relative energy error
    
    Args:
        initial_energy: Initial total energy
        final_energy: Final total energy
        
    Returns:
        float: Relative energy error
    """
    if initial_energy == 0:
        return float('inf')
    return abs((final_energy - initial_energy) / initial_energy)

def calculate_position_error(actual, expected):
    """
    Calculate position error
    
    Args:
        actual: Actual position vector
        expected: Expected position vector
        
    Returns:
        float: Euclidean distance between actual and expected
    """
    return np.linalg.norm(np.array(actual) - np.array(expected))

def calculate_velocity_error(actual, expected):
    """
    Calculate velocity error
    
    Args:
        actual: Actual velocity vector
        expected: Expected velocity vector
        
    Returns:
        float: Euclidean distance between actual and expected
    """
    return np.linalg.norm(np.array(actual) - np.array(expected))