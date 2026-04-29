"""Force model plugin system for orbital mechanics simulator"""
import importlib
import os
from typing import Callable, Dict, List, Union, Optional
import numpy as np
from src.core.exceptions import ForceModelError


class ForceModel:
    """Base class for force models"""
    
    def __init__(self, name: str):
        """
        Initialize force model
        
        Args:
            name: Name of the force model
        """
        self.name = name
    
    def __call__(self, t: float, y: Union[List[float], np.ndarray]) -> np.ndarray:
        """
        Calculate acceleration due to this force
        
        Args:
            t: Current time (s)
            y: State vector [x, y, z, vx, vy, vz]
            
        Returns:
            Acceleration vector [ax, ay, az]
        """
        raise NotImplementedError("Subclasses must implement __call__ method")


class ForceModelManager:
    """Manager for force models"""
    
    def __init__(self):
        """Initialize force model manager"""
        self.force_models: Dict[str, ForceModel] = {}
        self._load_builtin_models()
    
    def _load_builtin_models(self) -> None:
        """Load built-in force models"""
        # This will be implemented in the actual code
        pass
    
    def register_model(self, model: ForceModel) -> None:
        """
        Register a force model
        
        Args:
            model: Force model to register
        """
        self.force_models[model.name] = model
    
    def load_model(self, name: str) -> ForceModel:
        """
        Load a force model by name
        
        Args:
            name: Name of the force model
            
        Returns:
            Force model instance
        """
        if name in self.force_models:
            return self.force_models[name]
        raise ForceModelError(f"Force model '{name}' not found")
    
    def create_combined_model(self, model_names: List[str]) -> Callable[[float, Union[List[float], np.ndarray]], np.ndarray]:
        """
        Create a combined force model from multiple models
        
        Args:
            model_names: List of force model names
            
        Returns:
            Combined force model function
        """
        models = [self.load_model(name) for name in model_names]
        
        def combined_force(t: float, y: Union[List[float], np.ndarray]) -> np.ndarray:
            """Combined force model"""
            r = y[:3]
            v = y[3:]
            
            # Calculate total acceleration
            total_acc = np.zeros(3)
            for model in models:
                total_acc += model(t, y)
            
            return np.concatenate([v, total_acc])
        
        return combined_force


# Global force model manager
force_model_manager = ForceModelManager()
