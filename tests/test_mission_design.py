import numpy as np
import pytest
from src.core.bodies import EARTH, JUPITER
from src.orbits.mission_design import hohmann_transfer, bielliptic_transfer, calculate_delta_v, optimize_hohmann_transfer, gravity_assist, multi_burn_transfer, optimal_transfer


def test_hohmann_transfer():
    """
    Test Hohmann transfer calculation
    """
    # Test case: transfer from 7000 km altitude to 35786 km altitude (geostationary)
    r1 = EARTH.radius + 7000  # km
    r2 = EARTH.radius + 35786  # km
    
    delta_v1, delta_v2, transfer_time = hohmann_transfer(r1, r2, EARTH.mu)
    
    # Check that delta_v values are positive
    assert delta_v1 > 0
    assert delta_v2 > 0
    
    # Check that transfer time is positive
    assert transfer_time > 0
    
    # Check that total delta_v is reasonable (should be around 2.5 km/s for GEO transfer)
    total_delta_v = delta_v1 + delta_v2
    assert 2.0 < total_delta_v < 3.0


def test_bielliptic_transfer():
    """
    Test bi-elliptic transfer calculation
    """
    # Test case: transfer from 7000 km altitude to 35786 km altitude with intermediate 100000 km altitude
    r1 = EARTH.radius + 7000  # km
    r2 = 100000  # km
    r3 = EARTH.radius + 35786  # km
    
    delta_v1, delta_v2, delta_v3, transfer_time = bielliptic_transfer(r1, r2, r3, EARTH.mu)
    
    # Check that delta_v1 and delta_v2 are positive (accelerations)
    assert delta_v1 > 0
    assert delta_v2 > 0
    # delta_v3 can be negative (deceleration)
    assert transfer_time > 0


def test_calculate_delta_v():
    """
    Test delta-v calculation
    """
    # Test case: simple velocity change
    initial_state = np.array([7000, 0, 0, 0, 7.5, 0])
    final_state = np.array([7000, 0, 0, 0, 8.0, 0])
    
    delta_v = calculate_delta_v(initial_state, final_state, EARTH.mu)
    
    # Check that delta-v is correct
    assert np.isclose(delta_v, 0.5)


def test_optimize_hohmann_transfer():
    """
    Test Hohmann transfer optimization
    """
    # Test case: transfer from 7000 km altitude to 35786 km altitude
    r1 = EARTH.radius + 7000  # km
    r2 = EARTH.radius + 35786  # km
    
    delta_v_total, delta_v1, delta_v2, transfer_time = optimize_hohmann_transfer(r1, r2, EARTH.mu)
    
    # Check that delta_v values are positive
    assert delta_v_total > 0
    assert delta_v1 > 0
    assert delta_v2 > 0
    
    # Check that transfer time is positive
    assert transfer_time > 0


def test_gravity_assist():
    """
    Test gravity assist calculation
    """
    # Test case: Jupiter gravity assist
    v_inf = np.array([10, 0, 0])  # km/s
    body_velocity = np.array([13.07, 0, 0])  # km/s (Jupiter's orbital velocity)
    closest_approach = 50000  # km
    
    v_out = gravity_assist(v_inf, body_velocity, JUPITER.mu, closest_approach)
    
    # Check that velocity after gravity assist is different from input
    assert not np.array_equal(v_out, v_inf)
    
    # Check that velocity magnitude is reasonable
    assert np.linalg.norm(v_out) > 0


def test_multi_burn_transfer():
    """
    Test multi-burn transfer calculation
    """
    # Test case: transfer from 7000 km altitude to 35786 km altitude (180-degree transfer)
    r1 = EARTH.radius + 7000
    v1 = np.sqrt(EARTH.mu / r1)
    initial_state = np.array([r1, 0, 0, 0, v1, 0])

    r2 = EARTH.radius + 35786
    v2 = np.sqrt(EARTH.mu / r2)
    final_state = np.array([-r2, 0, 0, 0, -v2, 0])  # 180-degree transfer

    delta_vs, burn_times, burn_states = multi_burn_transfer(initial_state, final_state, EARTH.mu, n_burns=2)

    # Check that we get the correct number of burns
    assert len(delta_vs) == 2
    assert len(burn_times) == 2
    assert len(burn_states) == 2

    # Check that delta-v values are reasonable
    for delta_v in delta_vs:
        assert np.linalg.norm(delta_v) > 0
    
    # Check that burn times are positive and increasing
    assert burn_times[0] >= 0
    assert burn_times[1] > burn_times[0]


def test_optimal_transfer():
    """
    Test optimal transfer calculation
    """
    # Test case: transfer from 7000 km altitude to 35786 km altitude
    r1 = EARTH.radius + 7000
    v1 = np.sqrt(EARTH.mu / r1)
    initial_state = np.array([r1, 0, 0, 0, v1, 0])
    
    r2 = EARTH.radius + 35786
    v2 = np.sqrt(EARTH.mu / r2)
    final_state = np.array([0, r2, 0, -v2, 0, 0])
    
    delta_v_total, delta_vs, burn_times, burn_states = optimal_transfer(initial_state, final_state, EARTH.mu)
    
    # Check that delta-v total is positive
    assert delta_v_total > 0
    
    # Check that we get reasonable delta-vs
    for delta_v in delta_vs:
        assert np.linalg.norm(delta_v) > 0
    
    # Check that burn times are positive and increasing
    assert len(burn_times) >= 2
    assert burn_times[0] >= 0
    for i in range(1, len(burn_times)):
        assert burn_times[i] > burn_times[i-1]


if __name__ == "__main__":
    test_hohmann_transfer()
    test_bielliptic_transfer()
    test_calculate_delta_v()
    test_optimize_hohmann_transfer()
    test_gravity_assist()
    test_multi_burn_transfer()
    test_optimal_transfer()
    print("All mission design tests passed!")
