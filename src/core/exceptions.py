"""Custom exception classes for the orbital mechanics simulator"""


class OrbitSimError(Exception):
    """Base exception class for all orbit simulation errors"""
    pass


class StateError(OrbitSimError):
    """Exception raised for state-related errors"""
    pass


class StateVectorError(StateError):
    """Exception raised for invalid state vectors"""
    pass


class OrbitError(OrbitSimError):
    """Exception raised for orbit-related errors"""
    pass


class PropagatorError(OrbitSimError):
    """Exception raised for propagator-related errors"""
    pass


class IntegratorError(PropagatorError):
    """Exception raised for integrator-related errors"""
    pass


class ForceModelError(PropagatorError):
    """Exception raised for force model-related errors"""
    pass


class ConfigurationError(OrbitSimError):
    """Exception raised for configuration-related errors"""
    pass


class VisualizationError(OrbitSimError):
    """Exception raised for visualization-related errors"""
    pass


class ConversionError(OrbitSimError):
    """Exception raised for coordinate conversion errors"""
    pass
