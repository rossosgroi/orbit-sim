"""Configuration system for orbital mechanics simulator"""
import os
import json
from typing import Dict, Any, Optional
from .exceptions import ConfigurationError


class Config:
    """Configuration manager for simulation parameters"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file: Path to configuration file
        """
        self.config: Dict[str, Any] = self._load_default_config()
        
        if config_file and os.path.exists(config_file):
            self._load_config_file(config_file)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """
        Load default configuration
        
        Returns:
            Default configuration dictionary
        """
        return {
            "simulation": {
                "default_integrator": "rk4",
                "default_time_step": 60.0,  # seconds
                "max_time_step": 3600.0,  # seconds
                "min_time_step": 0.1,  # seconds
                "error_tolerance": 1e-6
            },
            "visualization": {
                "show_plots": True,
                "save_plots": False,
                "plot_directory": "plots",
                "animation_fps": 30
            },
            "logging": {
                "level": "INFO",
                "log_directory": "logs",
                "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    
    def _load_config_file(self, config_file: str) -> None:
        """
        Load configuration from file
        
        Args:
            config_file: Path to configuration file
        """
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
            
            # Update config with file values
            self._update_config(self.config, file_config)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {e}")
    
    def _update_config(self, current: Dict[str, Any], update: Dict[str, Any]) -> None:
        """
        Recursively update configuration dictionary
        
        Args:
            current: Current configuration
            update: Updated configuration values
        """
        for key, value in update.items():
            if key in current and isinstance(current[key], dict) and isinstance(value, dict):
                self._update_config(current[key], value)
            else:
                current[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key (e.g., "simulation.default_integrator")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Configuration key (e.g., "simulation.default_integrator")
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, config_file: str) -> None:
        """
        Save configuration to file
        
        Args:
            config_file: Path to save configuration
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            raise ConfigurationError(f"Error saving configuration: {e}")


# Global configuration instance
config = Config()
