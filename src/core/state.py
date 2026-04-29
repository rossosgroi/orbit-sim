import numpy as np
from typing import List, Union, Optional
from .exceptions import StateVectorError

class State:
    """State vector representation for orbital objects"""
    
    def __init__(self, position: Union[List[float], np.ndarray], velocity: Union[List[float], np.ndarray]):
        """
        Initialize state vector
        
        Args:
            position: 3-element list or numpy array [x, y, z] in km
            velocity: 3-element list or numpy array [vx, vy, vz] in km/s
        """
        self.position: np.ndarray = np.array(position, dtype=np.float64)
        self.velocity: np.ndarray = np.array(velocity, dtype=np.float64)
        
        if self.position.shape != (3,):
            raise StateVectorError("Position must be a 3-element vector")
        if self.velocity.shape != (3,):
            raise StateVectorError("Velocity must be a 3-element vector")
    
    def to_vector(self) -> np.ndarray:
        """
        Convert state to 6-element vector [x, y, z, vx, vy, vz]
        
        Returns:
            numpy array: State vector
        """
        return np.concatenate([self.position, self.velocity])
    
    @classmethod
    def from_vector(cls, vector: Union[List[float], np.ndarray]) -> 'State':
        """
        Create State from 6-element vector
        
        Args:
            vector: 6-element list or numpy array [x, y, z, vx, vy, vz]
            
        Returns:
            State: State object
        """
        vector = np.array(vector, dtype=np.float64)
        if vector.shape != (6,):
            raise StateVectorError("Vector must be 6-element")
        return cls(vector[:3], vector[3:])
    
    def __repr__(self) -> str:
        return f"State(position={self.position}, velocity={self.velocity})"
    
    def __str__(self) -> str:
        return f"Position: {self.position} km\nVelocity: {self.velocity} km/s"