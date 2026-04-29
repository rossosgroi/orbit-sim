import numpy as np
from scipy.optimize import minimize, root
from .lambert import lambert_solver as lambert_problem
from ..core.bodies import CelestialBody
from ..dynamics.two_body import two_body_energy


def hohmann_transfer(r1: float, r2: float, mu: float) -> tuple:
    """
    Calculate Hohmann transfer orbit parameters
    
    Args:
        r1: Initial orbit radius (km)
        r2: Final orbit radius (km)
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        tuple: (delta_v1, delta_v2, transfer_time)
            delta_v1: Velocity change at periapsis (km/s)
            delta_v2: Velocity change at apoapsis (km/s)
            transfer_time: Time of flight (s)
    """
    # Semi-major axis of transfer orbit
    a_transfer = (r1 + r2) / 2
    
    # Velocities in circular orbits
    v1_circular = np.sqrt(mu / r1)
    v2_circular = np.sqrt(mu / r2)
    
    # Velocities at transfer orbit periapsis and apoapsis
    v_transfer_periapsis = np.sqrt(mu * (2/r1 - 1/a_transfer))
    v_transfer_apoapsis = np.sqrt(mu * (2/r2 - 1/a_transfer))
    
    # Delta-v requirements
    delta_v1 = v_transfer_periapsis - v1_circular
    delta_v2 = v2_circular - v_transfer_apoapsis
    
    # Transfer time (half of transfer orbit period)
    transfer_time = np.pi * np.sqrt(a_transfer**3 / mu)
    
    return delta_v1, delta_v2, transfer_time


def bielliptic_transfer(r1: float, r2: float, r3: float, mu: float) -> tuple:
    """
    Calculate bi-elliptic transfer orbit parameters
    
    Args:
        r1: Initial orbit radius (km)
        r2: Intermediate orbit radius (km)
        r3: Final orbit radius (km)
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        tuple: (delta_v1, delta_v2, delta_v3, transfer_time)
            delta_v1: Velocity change at first periapsis (km/s)
            delta_v2: Velocity change at apoapsis (km/s)
            delta_v3: Velocity change at second periapsis (km/s)
            transfer_time: Total time of flight (s)
    """
    # First transfer orbit (r1 to r2)
    a1 = (r1 + r2) / 2
    v1_circular = np.sqrt(mu / r1)
    v_transfer1_periapsis = np.sqrt(mu * (2/r1 - 1/a1))
    v_transfer1_apoapsis = np.sqrt(mu * (2/r2 - 1/a1))
    delta_v1 = v_transfer1_periapsis - v1_circular
    
    # Second transfer orbit (r2 to r3)
    a2 = (r2 + r3) / 2
    v3_circular = np.sqrt(mu / r3)
    v_transfer2_apoapsis = np.sqrt(mu * (2/r2 - 1/a2))
    v_transfer2_periapsis = np.sqrt(mu * (2/r3 - 1/a2))
    delta_v2 = v_transfer2_apoapsis - v_transfer1_apoapsis
    delta_v3 = v3_circular - v_transfer2_periapsis
    
    # Total transfer time (half of each transfer orbit period)
    transfer_time1 = np.pi * np.sqrt(a1**3 / mu)
    transfer_time2 = np.pi * np.sqrt(a2**3 / mu)
    transfer_time = transfer_time1 + transfer_time2
    
    return delta_v1, delta_v2, delta_v3, transfer_time


def calculate_delta_v(initial_state: np.ndarray, final_state: np.ndarray, mu: float) -> float:
    """
    Calculate delta-v required for impulsive orbit change
    
    Args:
        initial_state: Initial state vector [x, y, z, vx, vy, vz]
        final_state: Final state vector [x, y, z, vx, vy, vz]
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        float: Delta-v required (km/s)
    """
    # Calculate velocities
    v_initial = initial_state[3:]
    v_final = final_state[3:]
    
    # Calculate delta-v
    delta_v = np.linalg.norm(v_final - v_initial)
    
    return delta_v


def optimize_hohmann_transfer(r1: float, r2: float, mu: float) -> tuple:
    """
    Optimize Hohmann transfer for minimum delta-v
    
    Args:
        r1: Initial orbit radius (km)
        r2: Final orbit radius (km)
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        tuple: (delta_v_total, delta_v1, delta_v2, transfer_time)
            delta_v_total: Total delta-v required (km/s)
            delta_v1: Velocity change at periapsis (km/s)
            delta_v2: Velocity change at apoapsis (km/s)
            transfer_time: Time of flight (s)
    """
    delta_v1, delta_v2, transfer_time = hohmann_transfer(r1, r2, mu)
    delta_v_total = abs(delta_v1) + abs(delta_v2)
    
    return delta_v_total, delta_v1, delta_v2, transfer_time


def interplanetary_transfer(primary_body: CelestialBody, departure_body: CelestialBody, arrival_body: CelestialBody, 
                          departure_time: float, time_of_flight: float) -> tuple:
    """
    Calculate interplanetary transfer orbit
    
    Args:
        primary_body: Primary celestial body (e.g., Sun)
        departure_body: Departure celestial body (e.g., Earth)
        arrival_body: Arrival celestial body (e.g., Mars)
        departure_time: Departure time (s since epoch)
        time_of_flight: Time of flight (s)
        
    Returns:
        tuple: (departure_state, arrival_state, delta_v)
            departure_state: Departure state vector [x, y, z, vx, vy, vz]
            arrival_state: Arrival state vector [x, y, z, vx, vy, vz]
            delta_v: Delta-v required for transfer (km/s)
    """
    # This is a placeholder implementation
    # In a real implementation, you would:
    # 1. Calculate positions of departure and arrival bodies at departure and arrival times
    # 2. Solve Lambert's problem to find transfer orbit
    # 3. Calculate delta-v required
    
    # For now, return dummy values
    departure_state = np.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])
    arrival_state = np.array([2.0, 0.0, 0.0, 0.0, 0.707, 0.0])
    delta_v = 1.0
    
    return departure_state, arrival_state, delta_v

def gravity_assist(v_inf: np.ndarray, body_velocity: np.ndarray, body_mu: float, closest_approach: float) -> np.ndarray:
    """
    Calculate gravity assist delta-v
    
    Args:
        v_inf: Velocity of spacecraft relative to planet at infinity (km/s)
        body_velocity: Velocity of planet (km/s)
        body_mu: Gravitational parameter of planet (km^3/s^2)
        closest_approach: Closest approach distance (km)
        
    Returns:
        np.ndarray: Velocity after gravity assist (km/s)
    """
    # Convert to planet-centered frame
    v_planet_frame = v_inf - body_velocity
    
    # Calculate hyperbolic excess velocity
    v_inf_mag = np.linalg.norm(v_planet_frame)
    
    # Calculate turning angle
    turning_angle = 2 * np.arcsin(body_mu / (closest_approach * v_inf_mag**2 + body_mu))
    
    # Calculate velocity after gravity assist in planet frame
    # Rotate velocity vector by turning angle
    theta = turning_angle
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])
    
    # Assume velocity is in xy-plane for simplicity
    v_planet_frame_2d = v_planet_frame[:2]
    v_planet_frame_2d_rotated = rotation_matrix @ v_planet_frame_2d
    
    # Convert back to 3D
    v_planet_frame_rotated = np.array([v_planet_frame_2d_rotated[0], v_planet_frame_2d_rotated[1], 0])
    
    # Convert back to heliocentric frame
    v_out = v_planet_frame_rotated + body_velocity
    
    return v_out

def multi_burn_transfer(initial_state: np.ndarray, final_state: np.ndarray, mu: float, n_burns: int = 2) -> tuple:
    """
    Calculate multi-burn transfer orbit
    
    Args:
        initial_state: Initial state vector [x, y, z, vx, vy, vz]
        final_state: Final state vector [x, y, z, vx, vy, vz]
        mu: Gravitational parameter (km^3/s^2)
        n_burns: Number of burns (default: 2)
        
    Returns:
        tuple: (delta_vs, burn_times, burn_states)
            delta_vs: List of delta-v vectors
            burn_times: List of burn times
            burn_states: List of states at burn times
    """
    # For simplicity, implement a two-burn transfer
    if n_burns == 2:
        # Calculate transfer orbit using Lambert's problem
        r1 = initial_state[:3]
        r2 = final_state[:3]
        
        # Estimate time of flight
        v1_mag = np.linalg.norm(initial_state[3:])
        v2_mag = np.linalg.norm(final_state[3:])
        r1_mag = np.linalg.norm(r1)
        r2_mag = np.linalg.norm(r2)
        
        # Estimate TOF based on average orbital period
        a_avg = (r1_mag + r2_mag) / 2
        tof_estimate = np.pi * np.sqrt(a_avg**3 / mu)
        
        # Solve Lambert's problem
        v1_transfer, v2_transfer = lambert_problem(r1, r2, tof_estimate, mu)
        
        # Calculate delta-vs
        delta_v1 = v1_transfer - initial_state[3:]
        delta_v2 = final_state[3:] - v2_transfer
        
        delta_vs = [delta_v1, delta_v2]
        burn_times = [0, tof_estimate]
        burn_states = [initial_state, final_state]
        
        return delta_vs, burn_times, burn_states
    else:
        # For more than 2 burns, implement a more complex optimization
        # This is a placeholder
        delta_vs = [np.zeros(3) for _ in range(n_burns)]
        burn_times = [i * 1000 for i in range(n_burns)]
        burn_states = [initial_state for _ in range(n_burns)]
        
        return delta_vs, burn_times, burn_states

def optimal_transfer(initial_state: np.ndarray, final_state: np.ndarray, mu: float) -> tuple:
    """
    Calculate optimal transfer orbit using direct optimization
    
    Args:
        initial_state: Initial state vector [x, y, z, vx, vy, vz]
        final_state: Final state vector [x, y, z, vx, vy, vz]
        mu: Gravitational parameter (km^3/s^2)
        
    Returns:
        tuple: (delta_v_total, delta_vs, burn_times, burn_states)
            delta_v_total: Total delta-v required (km/s)
            delta_vs: List of delta-v vectors
            burn_times: List of burn times
            burn_states: List of states at burn times
    """
    # Define objective function to minimize total delta-v
    def objective(x):
        # x contains burn times and delta-vs
        # For simplicity, assume two burns
        tof = x[0]
        delta_v1 = x[1:4]
        delta_v2 = x[4:7]
        
        # Calculate transfer orbit
        r1 = initial_state[:3]
        v1 = initial_state[3:] + delta_v1
        r2 = final_state[:3]
        
        try:
            # Solve Lambert's problem
            v1_transfer, v2_transfer = lambert_problem(r1, r2, tof, mu)
            
            # Calculate required delta-v2
            delta_v2_required = final_state[3:] - v2_transfer
            
            # Total delta-v
            total_delta_v = np.linalg.norm(delta_v1) + np.linalg.norm(delta_v2_required)
            
            return total_delta_v
        except:
            return np.inf
    
    # Initial guess
    r1_mag = np.linalg.norm(initial_state[:3])
    r2_mag = np.linalg.norm(final_state[:3])
    a_avg = (r1_mag + r2_mag) / 2
    tof_guess = np.pi * np.sqrt(a_avg**3 / mu)
    
    x0 = [tof_guess, 0, 0, 0, 0, 0, 0]
    
    # Minimize
    result = minimize(objective, x0, method='Nelder-Mead')
    
    if result.success:
        tof = result.x[0]
        delta_v1 = result.x[1:4]
        
        # Calculate actual delta_v2
        r1 = initial_state[:3]
        v1 = initial_state[3:] + delta_v1
        r2 = final_state[:3]
        v1_transfer, v2_transfer = lambert_problem(r1, r2, tof, mu)
        delta_v2 = final_state[3:] - v2_transfer
        
        delta_vs = [delta_v1, delta_v2]
        burn_times = [0, tof]
        burn_states = [initial_state, final_state]
        delta_v_total = np.linalg.norm(delta_v1) + np.linalg.norm(delta_v2)
        
        return delta_v_total, delta_vs, burn_times, burn_states
    else:
        # If optimization fails, return Hohmann transfer as fallback
        r1 = np.linalg.norm(initial_state[:3])
        r2 = np.linalg.norm(final_state[:3])
        delta_v1, delta_v2, transfer_time = hohmann_transfer(r1, r2, mu)
        
        # Convert to vectors
        v1_initial = initial_state[3:]
        v1_circular = v1_initial / np.linalg.norm(v1_initial)
        delta_v1_vec = delta_v1 * v1_circular
        
        v2_final = final_state[3:]
        v2_circular = v2_final / np.linalg.norm(v2_final)
        delta_v2_vec = delta_v2 * v2_circular
        
        delta_vs = [delta_v1_vec, delta_v2_vec]
        burn_times = [0, transfer_time]
        burn_states = [initial_state, final_state]
        delta_v_total = abs(delta_v1) + abs(delta_v2)
        
        return delta_v_total, delta_vs, burn_times, burn_states
