import numpy as np
import pytest
from src.core.bodies import EARTH
from src.orbits.conjunction import calculate_minimum_distance, detect_conjunctions, calculate_probability_of_collision, conjunction_analysis


def test_calculate_minimum_distance():
    """
    Test minimum distance calculation
    """
    # Test case: two objects in the same orbit
    state1 = np.array([7000, 0, 0, 0, 7.5, 0])
    state2 = np.array([7000, 10, 0, 0, 7.5, 0])  # 10 km behind
    
    min_distance, t_min = calculate_minimum_distance(state1, state2, EARTH.mu)
    
    # Check that minimum distance is positive
    assert min_distance > 0
    
    # Check that time of minimum distance is positive
    assert t_min >= 0


def test_detect_conjunctions():
    """
    Test conjunction detection
    """
    # Test case: two objects close to each other
    state1 = np.array([7000, 0, 0, 0, 7.5, 0])
    state2 = np.array([7000, 0.5, 0, 0, 7.5, 0])  # 0.5 km apart
    state3 = np.array([7000, 100, 0, 0, 7.5, 0])  # 100 km apart
    
    objects = [state1, state2, state3]
    conjunctions = detect_conjunctions(objects, EARTH.mu, threshold=1.0)
    
    # Check that only one conjunction is detected
    assert len(conjunctions) == 1
    
    # Check that the conjunction is between object 0 and 1
    assert conjunctions[0][0] == 0
    assert conjunctions[0][1] == 1


def test_calculate_probability_of_collision():
    """
    Test collision probability calculation
    """
    # Test case: very close objects
    min_distance = 0.01  # 10 meters
    position_error = 0.1  # 100 meters
    
    prob = calculate_probability_of_collision(min_distance, position_error)
    
    # Check that probability is between 0 and 1
    assert 0 <= prob <= 1


def test_conjunction_analysis():
    """
    Test comprehensive conjunction analysis
    """
    # Test case: two objects close to each other
    state1 = np.array([7000, 0, 0, 0, 7.5, 0])
    state2 = np.array([7000, 0.5, 0, 0, 7.5, 0])  # 0.5 km apart
    
    objects = [state1, state2]
    events = conjunction_analysis(objects, EARTH.mu, threshold=1.0)
    
    # Check that one event is returned
    assert len(events) == 1
    
    # Check that the event has all required fields
    assert 'object1' in events[0]
    assert 'object2' in events[0]
    assert 'min_distance' in events[0]
    assert 'time_of_conjunction' in events[0]
    assert 'probability_of_collision' in events[0]


if __name__ == "__main__":
    test_calculate_minimum_distance()
    test_detect_conjunctions()
    test_calculate_probability_of_collision()
    test_conjunction_analysis()
    print("All conjunction analysis tests passed!")
