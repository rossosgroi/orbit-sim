import numpy as np

# Physical constants
G = 6.67430e-20  # km^3/(kg·s^2)
C = 299792.458  # Speed of light in km/s

# US Standard Atmosphere 1976 model constants
ATMOSPHERIC_LAYERS = [
    # (altitude_km, temperature_K, pressure_Pa, density_kg_m3, scale_height_km)
    (0.0, 288.15, 101325.0, 1.225, 7.31),
    (11.0, 216.65, 22632.1, 0.36391, 6.42),
    (20.0, 216.65, 5474.89, 0.08803, 6.59),
    (32.0, 228.65, 868.02, 0.01322, 8.94),
    (47.0, 270.65, 110.91, 0.00143, 12.65),
    (51.0, 270.65, 66.94, 0.00086, 12.65),
    (71.0, 214.65, 3.96, 0.000064, 16.14),
    (84.852, 186.87, 0.3734, 0.0000072, 22.52),
    (100.0, 210.0, 0.032, 0.0000005, 30.0),
    (150.0, 600.0, 0.0002, 3.5e-9, 50.0),
    (200.0, 800.0, 2.6e-5, 4.3e-10, 70.0),
    (300.0, 1000.0, 1.6e-6, 3.2e-11, 100.0),
    (400.0, 1200.0, 1.6e-7, 3.7e-12, 130.0),
    (500.0, 1400.0, 2.2e-8, 5.6e-13, 160.0),
    (600.0, 1600.0, 3.6e-9, 1.0e-13, 190.0),
    (700.0, 1800.0, 6.9e-10, 2.1e-14, 220.0),
    (800.0, 2000.0, 1.5e-10, 4.6e-15, 250.0),
    (900.0, 2200.0, 3.6e-11, 1.2e-15, 280.0),
    (1000.0, 2400.0, 9.7e-12, 3.4e-16, 310.0)
]

def j2_derivative(mu, r_body, j2):
    """
    Create derivative function with J2 perturbation
    
    Args:
        mu: Gravitational parameter (km^3/s^2)
        r_body: Equatorial radius of the body (km)
        j2: J2 coefficient
        
    Returns:
        function: Derivative function f(t, y)
    """
    def derivative(t, y):
        """
        Calculate derivative with J2 perturbation
        
        Args:
            t: Current time (s)
            y: State vector [x, y, z, vx, vy, vz]
            
        Returns:
            numpy array: Derivative [vx, vy, vz, ax, ay, az]
        """
        r = y[:3]
        v = y[3:]
        
        r_norm = np.linalg.norm(r)
        if r_norm == 0:
            raise ValueError("Position vector cannot be zero")
        
        # Two-body acceleration
        a_two_body = -mu * r / r_norm**3
        
        # J2 perturbation acceleration
        z2 = r[2]**2
        r2 = r_norm**2
        factor = (3/2) * j2 * mu * r_body**2 / r_norm**5
        
        ax = factor * r[0] * (5 * z2 / r2 - 1)
        ay = factor * r[1] * (5 * z2 / r2 - 1)
        az = factor * r[2] * (5 * z2 / r2 - 3)
        
        a_j2 = np.array([ax, ay, az])
        
        # Total acceleration
        a_total = a_two_body + a_j2
        
        return np.concatenate([v, a_total])
    
    return derivative

def atmospheric_drag_derivative(mu, r_body, Cd=2.2, A=1.0, m=1.0):
    """
    Create derivative function with high-fidelity atmospheric drag
    
    Args:
        mu: Gravitational parameter (km^3/s^2)
        r_body: Equatorial radius of the body (km)
        Cd: Drag coefficient
        A: Cross-sectional area (m^2)
        m: Mass of the spacecraft (kg)
        
    Returns:
        function: Derivative function f(t, y)
    """
    def get_atmospheric_properties(altitude_km):
        """
        Get atmospheric properties at a given altitude using US Standard Atmosphere 1976
        
        Args:
            altitude_km: Altitude in kilometers
            
        Returns:
            tuple: (temperature_K, pressure_Pa, density_kg_m3)
        """
        if altitude_km < 0:
            return ATMOSPHERIC_LAYERS[0][1], ATMOSPHERIC_LAYERS[0][2], ATMOSPHERIC_LAYERS[0][3]
        
        if altitude_km >= ATMOSPHERIC_LAYERS[-1][0]:
            return ATMOSPHERIC_LAYERS[-1][1], ATMOSPHERIC_LAYERS[-1][2], ATMOSPHERIC_LAYERS[-1][3]
        
        # Find the appropriate layer
        for i in range(len(ATMOSPHERIC_LAYERS) - 1):
            if ATMOSPHERIC_LAYERS[i][0] <= altitude_km < ATMOSPHERIC_LAYERS[i+1][0]:
                # Interpolate between layers
                h0, T0, P0, rho0, H = ATMOSPHERIC_LAYERS[i]
                h1, T1, P1, rho1, _ = ATMOSPHERIC_LAYERS[i+1]
                
                # Linear interpolation for temperature
                T = T0 + (T1 - T0) * (altitude_km - h0) / (h1 - h0)
                
                # Exponential interpolation for pressure and density
                if T0 != T1:
                    # Temperature varies, use hydrostatic equation
                    g = 9.80665  # m/s^2
                    R = 287.05  # J/(kg·K)
                    P = P0 * (T0 / T) ** (g / (R * (T1 - T0) / (h1 - h0) * 1000))
                    rho = rho0 * (T0 / T) ** (g / (R * (T1 - T0) / (h1 - h0) * 1000) - 1)
                else:
                    # Isothermal layer
                    P = P0 * np.exp(-(altitude_km - h0) / H)
                    rho = rho0 * np.exp(-(altitude_km - h0) / H)
                
                return T, P, rho
        
        return ATMOSPHERIC_LAYERS[-1][1], ATMOSPHERIC_LAYERS[-1][2], ATMOSPHERIC_LAYERS[-1][3]
    
    def derivative(t, y):
        """
        Calculate derivative with atmospheric drag
        
        Args:
            t: Current time (s)
            y: State vector [x, y, z, vx, vy, vz]
            
        Returns:
            numpy array: Derivative [vx, vy, vz, ax, ay, az]
        """
        r = y[:3]  # Position in km
        v = y[3:]  # Velocity in km/s
        
        r_norm = np.linalg.norm(r)
        if r_norm == 0:
            raise ValueError("Position vector cannot be zero")
        
        # Two-body acceleration
        a_two_body = -mu * r / r_norm**3
        
        # Atmospheric drag acceleration
        # Altitude above the body
        altitude_km = r_norm - r_body
        
        # Only apply drag if above the body
        if altitude_km > 0:
            # Get atmospheric properties
            T, P, rho = get_atmospheric_properties(altitude_km)
            
            # Convert units: km to m, km/s to m/s
            r_m = r * 1000.0  # Convert to meters
            v_m = v * 1000.0  # Convert to meters/s
            
            # Calculate relative velocity (assuming atmosphere rotates with the Earth)
            # Earth rotation rate: 7.292115e-5 rad/s
            omega_earth = 7.292115e-5
            v_rot = np.array([-omega_earth * r_m[1], omega_earth * r_m[0], 0])
            v_rel = v_m - v_rot
            
            # Velocity magnitude
            v_norm = np.linalg.norm(v_rel)
            
            if v_norm > 0:
                # Drag force direction (opposite to relative velocity)
                drag_dir = -v_rel / v_norm
                
                # Drag acceleration
                a_drag_m = -0.5 * rho * v_norm**2 * Cd * A / m * drag_dir
                
                # Convert back to km/s^2
                a_drag = a_drag_m / 1000.0
            else:
                a_drag = np.zeros(3)
        else:
            a_drag = np.zeros(3)
        
        # Total acceleration
        a_total = a_two_body + a_drag
        
        return np.concatenate([v, a_total])
    
    return derivative

def third_body_derivative(mu_primary, mu_third, third_body_position_func):
    """
    Create derivative function with third-body perturbation
    
    Args:
        mu_primary: Gravitational parameter of the primary body (km^3/s^2)
        mu_third: Gravitational parameter of the third body (km^3/s^2)
        third_body_position_func: Function that returns the position of the third body at time t
        
    Returns:
        function: Derivative function f(t, y)
    """
    def derivative(t, y):
        """
        Calculate derivative with third-body perturbation
        
        Args:
            t: Current time (s)
            y: State vector [x, y, z, vx, vy, vz]
            
        Returns:
            numpy array: Derivative [vx, vy, vz, ax, ay, az]
        """
        r = y[:3]  # Position of the spacecraft relative to primary body
        v = y[3:]  # Velocity of the spacecraft relative to primary body
        
        r_norm = np.linalg.norm(r)
        if r_norm == 0:
            raise ValueError("Position vector cannot be zero")
        
        # Two-body acceleration
        a_two_body = -mu_primary * r / r_norm**3
        
        # Third-body position at current time
        r_third = third_body_position_func(t)
        
        # Spacecraft position relative to third body
        r_sc_third = r - r_third
        r_sc_third_norm = np.linalg.norm(r_sc_third)
        
        # Third-body position norm
        r_third_norm = np.linalg.norm(r_third)
        
        if r_sc_third_norm == 0 or r_third_norm == 0:
            # Avoid division by zero
            a_third_body = np.zeros(3)
        else:
            # Third-body perturbation acceleration
            a_third_body = -mu_third * (r_sc_third / r_sc_third_norm**3 + r_third / r_third_norm**3)
        
        # Total acceleration
        a_total = a_two_body + a_third_body
        
        return np.concatenate([v, a_total])
    
    return derivative

def solar_radiation_pressure_derivative(mu, r_body, P0=4.56e-6, A=1.0, m=1.0, CR=1.0, sun_position_func=None):
    """
    Create derivative function with solar radiation pressure
    
    Args:
        mu: Gravitational parameter of the primary body (km^3/s^2)
        r_body: Equatorial radius of the primary body (km)
        P0: Solar radiation pressure at 1 AU (N/m^2)
        A: Cross-sectional area of the spacecraft (m^2)
        m: Mass of the spacecraft (kg)
        CR: Radiation pressure coefficient (1.0 for perfect absorption, 2.0 for perfect reflection)
        sun_position_func: Function that returns the position of the Sun at time t
        
    Returns:
        function: Derivative function f(t, y)
    """
    def derivative(t, y):
        """
        Calculate derivative with solar radiation pressure
        
        Args:
            t: Current time (s)
            y: State vector [x, y, z, vx, vy, vz]
            
        Returns:
            numpy array: Derivative [vx, vy, vz, ax, ay, az]
        """
        r = y[:3]  # Position in km
        v = y[3:]  # Velocity in km/s
        
        r_norm = np.linalg.norm(r)
        if r_norm == 0:
            raise ValueError("Position vector cannot be zero")
        
        # Two-body acceleration
        a_two_body = -mu * r / r_norm**3
        
        # Solar radiation pressure acceleration
        if sun_position_func is not None:
            # Sun position at current time
            r_sun = sun_position_func(t)
            
            # Spacecraft position relative to Sun
            r_sc_sun = r - r_sun
            r_sc_sun_norm = np.linalg.norm(r_sc_sun)
            
            if r_sc_sun_norm > 0:
                # Unit vector from spacecraft to Sun
                sun_dir = r_sc_sun / r_sc_sun_norm
                
                # Distance from Sun in AU (1 AU = 149597870.7 km)
                r_au = r_sc_sun_norm / 149597870.7
                
                # Solar radiation pressure at spacecraft position
                P = P0 / r_au**2
                
                # Acceleration due to solar radiation pressure
                # Convert to km/s^2: 1 N/kg = 1 m/s^2 = 0.001 km/s^2
                a_srp = -P * A * CR / m * sun_dir * 0.001
            else:
                a_srp = np.zeros(3)
        else:
            a_srp = np.zeros(3)
        
        # Total acceleration
        a_total = a_two_body + a_srp
        
        return np.concatenate([v, a_total])
    
    return derivative

def relativistic_derivative(mu):
    """
    Create derivative function with relativistic effects
    
    Args:
        mu: Gravitational parameter of the primary body (km^3/s^2)
        
    Returns:
        function: Derivative function f(t, y)
    """
    def derivative(t, y):
        """
        Calculate derivative with relativistic effects
        
        Args:
            t: Current time (s)
            y: State vector [x, y, z, vx, vy, vz]
            
        Returns:
            numpy array: Derivative [vx, vy, vz, ax, ay, az]
        """
        r = y[:3]  # Position in km
        v = y[3:]  # Velocity in km/s
        
        r_norm = np.linalg.norm(r)
        if r_norm == 0:
            raise ValueError("Position vector cannot be zero")
        
        # Two-body acceleration
        a_two_body = -mu * r / r_norm**3
        
        # Relativistic correction (Einstein's general relativity)
        v_norm = np.linalg.norm(v)
        
        # Calculate relativistic correction term
        # First term: 3*mu*v^2/(c^2*r)
        # Second term: -4*mu^2/(c^2*r^2)
        term1 = 3 * mu * v_norm**2 / (C**2 * r_norm)
        term2 = -4 * mu**2 / (C**2 * r_norm**2)
        
        # Relativistic acceleration
        a_relativistic = a_two_body * (1 + term1 + term2)
        
        # Total acceleration
        a_total = a_relativistic
        
        return np.concatenate([v, a_total])
    
    return derivative