import numpy as np

class KeplerianElements:
    """Keplerian orbital elements"""
    
    def __init__(self, a, e, i, raan, argp, nu):
        """
        Initialize Keplerian elements
        
        Args:
            a: Semi-major axis (km)
            e: Eccentricity
            i: Inclination (radians)
            raan: Right ascension of ascending node (radians)
            argp: Argument of perigee (radians)
            nu: True anomaly (radians)
        """
        self.a = a
        self.e = e
        self.i = i
        self.raan = raan
        self.argp = argp
        self.nu = nu
    
    def __repr__(self):
        return f"KeplerianElements(a={self.a}, e={self.e}, i={self.i}, raan={self.raan}, argp={self.argp}, nu={self.nu})"
    
    def __str__(self):
        return (
            f"Semi-major axis: {self.a} km\n" +
            f"Eccentricity: {self.e}\n" +
            f"Inclination: {self.i} rad\n" +
            f"RAAN: {self.raan} rad\n" +
            f"Argument of perigee: {self.argp} rad\n" +
            f"True anomaly: {self.nu} rad"
        )