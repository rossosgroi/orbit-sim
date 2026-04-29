import numpy as np

def norm(vec):
    """
    Calculate the norm of a vector
    
    Args:
        vec: Vector as list or numpy array
        
    Returns:
        float: Norm of the vector
    """
    return np.linalg.norm(np.array(vec))

def unit_vector(vec):
    """
    Calculate the unit vector
    
    Args:
        vec: Vector as list or numpy array
        
    Returns:
        numpy array: Unit vector
    """
    vec = np.array(vec)
    return vec / np.linalg.norm(vec)

def cross(a, b):
    """
    Calculate cross product of two vectors
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        numpy array: Cross product
    """
    return np.cross(np.array(a), np.array(b))

def dot(a, b):
    """
    Calculate dot product of two vectors
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        float: Dot product
    """
    return np.dot(np.array(a), np.array(b))

def angle_between(a, b):
    """
    Calculate angle between two vectors
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        float: Angle in radians
    """
    a = np.array(a)
    b = np.array(b)
    return np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def rotate_vector(vec, axis, angle):
    """
    Rotate a vector around an axis by a given angle
    
    Args:
        vec: Vector to rotate
        axis: Rotation axis
        angle: Rotation angle in radians
        
    Returns:
        numpy array: Rotated vector
    """
    vec = np.array(vec)
    axis = unit_vector(axis)
    
    # Rodrigues' rotation formula
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    
    return (vec * cos_theta +
            np.cross(axis, vec) * sin_theta +
            axis * np.dot(axis, vec) * (1 - cos_theta))