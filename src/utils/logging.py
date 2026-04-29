import logging
import time
from datetime import datetime

def setup_logger(name='orbit-sim', level=logging.INFO):
    """
    Setup logger for the simulation
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create file handler
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(f'logs/simulation_{timestamp}.log')
    file_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Set formatters
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

def log_simulation_parameters(logger, params):
    """
    Log simulation parameters
    
    Args:
        logger: Logger instance
        params: Dictionary of parameters
    """
    logger.info("Simulation Parameters:")
    for key, value in params.items():
        logger.info(f"  {key}: {value}")

def log_energy_drift(logger, initial_energy, final_energy):
    """
    Log energy drift
    
    Args:
        logger: Logger instance
        initial_energy: Initial energy
        final_energy: Final energy
    """
    energy_error = abs((final_energy - initial_energy) / initial_energy) * 100
    logger.info(f"Energy drift: {energy_error:.6f}%")
    
    if energy_error > 1.0:
        logger.warning("High energy drift detected!")

def log_step_size(logger, step_size):
    """
    Log step size
    
    Args:
        logger: Logger instance
        step_size: Current step size
    """
    logger.debug(f"Current step size: {step_size}s")