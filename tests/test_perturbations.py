import numpy as np
import pytest
from src.core.bodies import EARTH
from src.dynamics.perturbations import relativistic_derivative, atmospheric_drag_derivative


def test_relativistic_derivative():
    """
    Test relativistic derivative calculation
    """
    # Create relativistic derivative function
    rel_derivative = relativistic_derivative(EARTH.mu)
    
    # Test case: Earth satellite in circular orbit
    r = EARTH.radius + 7000  # km
    v = np.sqrt(EARTH.mu / r)  # km/s
    state = np.array([r, 0, 0, 0, v, 0])
    
    # Calculate derivative
    deriv = rel_derivative(0, state)
    
    # Check that derivative has correct shape
    assert deriv.shape == (6,)
    
    # Check that velocity derivatives are correct (should be equal to current velocity)
    assert np.allclose(deriv[:3], state[3:])
    
    # Check that acceleration is non-zero
    assert not np.allclose(deriv[3:], np.zeros(3))


def test_atmospheric_drag_derivative():
    """
    Test atmospheric drag derivative calculation
    """
    # Create atmospheric drag derivative function
    drag_derivative = atmospheric_drag_derivative(EARTH.mu, EARTH.radius)
    
    # Test case 1: Satellite in low Earth orbit (should experience drag)
    r = EARTH.radius + 200  # km (low Earth orbit)
    v = np.sqrt(EARTH.mu / r)  # km/s
    state = np.array([r, 0, 0, 0, v, 0])
    
    # Calculate derivative
    deriv = drag_derivative(0, state)
    
    # Check that derivative has correct shape
    assert deriv.shape == (6,)
    
    # Check that velocity derivatives are correct
    assert np.allclose(deriv[:3], state[3:])
    
    # Check that acceleration is non-zero (drag should be present)
    assert not np.allclose(deriv[3:], np.zeros(3))
    
    # Test case 2: Satellite in geostationary orbit (should experience minimal drag)
    r = EARTH.radius + 35786  # km (geostationary orbit)
    v = np.sqrt(EARTH.mu / r)  # km/s
    state = np.array([r, 0, 0, 0, v, 0])
    
    # Calculate derivative
    deriv = drag_derivative(0, state)
    
    # Check that derivative has correct shape
    assert deriv.shape == (6,)
    
    # Check that velocity derivatives are correct
    assert np.allclose(deriv[:3], state[3:])


if __name__ == "__main__":
    test_relativistic_derivative()
    test_atmospheric_drag_derivative()
    print("All perturbations tests passed!")
