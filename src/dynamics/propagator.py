import numpy as np
from typing import Callable, Union, List, Tuple
from ..numerics.integrators import rk4_step, adaptive_rk45
from src.core.exceptions import PropagatorError

class OrbitPropagator:
    """Orbit propagator with configurable force model and integrator"""
    
    def __init__(self, force_model: Callable[[float, Union[List[float], np.ndarray]], np.ndarray], integrator: str = 'rk4'):
        """
        Initialize orbit propagator
        
        Args:
            force_model: Function returning derivative dy/dt
            integrator: Integration method ('rk4' or 'rk45')
        """
        self.force_model: Callable[[float, Union[List[float], np.ndarray]], np.ndarray] = force_model
        self.integrator: str = integrator
    
    def propagate(self, state0: Union[List[float], np.ndarray], t_span: float, dt: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Propagate orbit forward in time
        
        Args:
            state0: Initial state vector [x, y, z, vx, vy, vz]
            t_span: Time span to propagate (s)
            dt: Time step (s)
            
        Returns:
            tuple: (times, states)
                times: Array of time points
                states: Array of state vectors at each time point
        """
        # Initialize arrays
        n_steps = int(np.ceil(t_span / dt))
        times = np.zeros(n_steps + 1)
        states = np.zeros((n_steps + 1, 6))
        
        # Set initial conditions
        states[0] = state0
        
        if self.integrator == 'rk4':
            # Use fixed-step RK4
            for i in range(n_steps):
                states[i+1] = rk4_step(self.force_model, times[i], states[i], dt)
                times[i+1] = times[i] + dt
        
        elif self.integrator == 'rk45':
            # Use adaptive RK45
            current_time = 0.0
            current_state = state0.copy()
            
            i = 0
            while current_time < t_span and i < n_steps:
                states[i] = current_state
                times[i] = current_time
                
                current_state, current_time, dt = adaptive_rk45(
                    self.force_model, current_time, current_state, dt
                )
                
                i += 1
            
            # Handle final step
            if i <= n_steps:
                states[i] = current_state
                times[i] = current_time
        
        else:
            raise PropagatorError(f"Unknown integrator: {self.integrator}")
        
        return times, states
    
    def propagate_with_energy(self, state0: Union[List[float], np.ndarray], t_span: float, dt: float, energy_fn: Callable[[Union[List[float], np.ndarray]], float]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Propagate orbit and calculate energy at each step
        
        Args:
            state0: Initial state vector [x, y, z, vx, vy, vz]
            t_span: Time span to propagate (s)
            dt: Time step (s)
            energy_fn: Function to calculate energy
            
        Returns:
            tuple: (times, states, energies)
        """
        times, states = self.propagate(state0, t_span, dt)
        energies = np.array([energy_fn(state) for state in states])
        return times, states, energies