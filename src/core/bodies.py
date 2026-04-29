from .constants import MU_EARTH, R_EARTH, J2_EARTH, MU_SUN, R_SUN, MU_MOON, R_MOON, MU_JUPITER, R_JUPITER, J2_JUPITER

class CelestialBody:
    """Base class for celestial bodies"""
    
    def __init__(self, name, mu, radius, j2=0.0):
        """
        Initialize celestial body
        
        Args:
            name: Name of the body
            mu: Gravitational parameter (km^3/s^2)
            radius: Equatorial radius (km)
            j2: J2 coefficient for non-spherical gravity
        """
        self.name = name
        self.mu = mu
        self.radius = radius
        self.j2 = j2

# Pre-defined celestial bodies
EARTH = CelestialBody("Earth", MU_EARTH, R_EARTH, J2_EARTH)
SUN = CelestialBody("Sun", MU_SUN, R_SUN)
MOON = CelestialBody("Moon", MU_MOON, R_MOON)
JUPITER = CelestialBody("Jupiter", MU_JUPITER, R_JUPITER, J2_JUPITER)

# Dictionary for easy access
BODIES = {
    "earth": EARTH,
    "sun": SUN,
    "moon": MOON,
    "jupiter": JUPITER
}