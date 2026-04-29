# Orbital Mechanics Simulator

A professional-grade orbital mechanics simulation framework designed for aerospace engineering applications.

This project aims to provide a robust simulation environment for orbital mechanics, including:

- Newtonian mechanics applied in 3D space
- Numerical integration of differential equations
- Physical modeling of orbital dynamics
- Clean software architecture
- Extensible simulation system

## Physics Model

### Core Equation of Motion

Two-body gravity:

```
dd r = -μ * r / |r|³
```

Where:

- μ = GM (gravitational parameter)
- r = position vector

### Advanced Force Models

- **J2 perturbation** for Earth's non-spherical gravity
- **High-fidelity atmospheric drag** using US Standard Atmosphere 1976
- **Third-body perturbations** (Moon, Sun)
- **Solar radiation pressure**
- **Relativistic effects** (Einstein's general relativity)
- **Multi-body dynamics**

## Numerical Methods

The simulator uses numerical integration methods such as:

1. **RK4** (Fourth-order Runge-Kutta):
   - Stable and widely used
   - Good balance of accuracy and computational efficiency
2. **Adaptive RK45** (Cash-Karp method):
   - Automatically adjusts step size for improved accuracy
   - Ideal for precision-critical applications
3. **Numba JIT optimization**:
   - Accelerated numerical calculations
   - Significantly improved performance

## Features

### Core Features

- ✅ Circular orbit propagation
- ✅ Elliptical orbit propagation
- ✅ Energy conservation check
- ✅ Hohmann transfer simulation
- ✅ Bi-elliptic transfer simulation
- ✅ Orbital elements conversion (Cartesian ↔ Keplerian)
- ✅ 3D orbit visualization (Matplotlib)
- ✅ Interactive 3D visualization (Plotly)
- ✅ Lambert problem solver
- ✅ J2 perturbation modeling
- ✅ Sun-synchronous orbit simulation
- ✅ Atmospheric drag modeling
- ✅ Solar radiation pressure
- ✅ Third-body perturbations
- ✅ Relativistic effects
- ✅ Multi-body dynamics
- ✅ Conjunction analysis
- ✅ Gravity assist calculations
- ✅ Multi-burn transfer optimization
- ✅ Optimal transfer orbit calculation
- ✅ Graphical user interface (GUI)

## Results

### Example Outputs

1. **3D Orbit Visualization**:
   - Earth at origin
   - Satellite trajectory
   - Rotation animation
   - Interactive Plotly visualization
2. **Energy Conservation**:
   - Total energy vs time plot
   - Minimal energy drift (< 0.1%)
3. **Orbital Elements Evolution**:
   - Semi-major axis stability
   - Eccentricity drift (with J2)
   - RAAN and argument of perigee evolution
4. **Mission Design Results**:
   - Delta-v requirements
   - Transfer time calculations
   - Gravity assist trajectories

## How to Run

### Installation

```bash
pip install -r requirements.txt
```

### Run Simulations

```bash
# Basic Earth satellite orbit
python main.py --scenario earth_satellite

# Hohmann transfer simulation
python main.py --scenario hohmann_transfer

# J2 perturbation study
python main.py --scenario j2_perturbation

# Run tests
python main.py --scenario test
```

### Run GUI

```bash
# Run the graphical user interface
python run_gui.py
```

## Usage Examples

### Basic Orbit Simulation

```python
from src.core.bodies import EARTH
from src.core.state import State
from src.dynamics.two_body import two_body_derivative
from src.dynamics.propagator import OrbitPropagator
from src.visualization.plot_3d import plot_3d_orbit

# Create initial state (7000 km altitude circular orbit)
r = 7000 + EARTH.radius
v = (EARTH.mu / r) ** 0.5
state0 = State([r, 0, 0], [0, v, 0])

# Create force model and propagator
force_model = two_body_derivative(EARTH.mu)
propagator = OrbitPropagator(force_model, integrator='rk45')

# Propagate for 24 hours
duration = 24 * 3600
dt = 60

times, states = propagator.propagate(state0.to_vector(), duration, dt)

# Visualize the orbit
plot_3d_orbit(states, EARTH, 'Earth Satellite Orbit')
```

### Gravity Assist

```python
from src.orbits.mission_design import gravity_assist
from src.core.bodies import EARTH, JUPITER
import numpy as np

# Define spacecraft velocity relative to Jupiter at infinity
v_inf = np.array([10, 0, 0])  # km/s

# Jupiter's velocity (simplified)
body_velocity = np.array([13.07, 0, 0])  # km/s

# Calculate gravity assist
v_out = gravity_assist(v_inf, body_velocity, JUPITER.mu, 50000)  # 50,000 km closest approach

print(f"Velocity before gravity assist: {np.linalg.norm(v_inf):.3f} km/s")
print(f"Velocity after gravity assist: {np.linalg.norm(v_out):.3f} km/s")
print(f"Delta-v from gravity assist: {np.linalg.norm(v_out - v_inf):.3f} km/s")
```

### Multi-burn Transfer

```python
from src.orbits.mission_design import multi_burn_transfer
from src.core.bodies import EARTH
import numpy as np

# Define initial and final states
r1 = 7000 + EARTH.radius
v1 = (EARTH.mu / r1) ** 0.5
initial_state = np.array([r1, 0, 0, 0, v1, 0])

r2 = 35786 + EARTH.radius
v2 = (EARTH.mu / r2) ** 0.5
final_state = np.array([0, r2, 0, -v2, 0, 0])

# Calculate multi-burn transfer
delta_vs, burn_times, burn_states = multi_burn_transfer(initial_state, final_state, EARTH.mu, n_burns=2)

print(f"Number of burns: {len(delta_vs)}")
for i, (delta_v, burn_time) in enumerate(zip(delta_vs, burn_times)):
    print(f"Burn {i+1}: delta-v = {np.linalg.norm(delta_v):.3f} km/s at {burn_time/3600:.2f} hours")
print(f"Total delta-v: {sum(np.linalg.norm(dv) for dv in delta_vs):.3f} km/s")
```

## Project Structure

```
orbit-sim/
├── src/
│   ├── core/            # Core modules (bodies, constants, state, exceptions, config)
│   ├── dynamics/        # Force models and propagator
│   ├── numerics/        # Numerical integration methods
│   ├── orbits/          # Orbital mechanics utilities
│   ├── visualization/   # Plotting and animation
│   ├── gui/             # Graphical user interface
│   └── utils/           # Utility functions
├── simulations/         # Simulation scripts
├── tests/               # Test cases
├── docs/                # Sphinx documentation
├── logs/                # Log files
├── .github/             # GitHub Actions CI/CD
├── README.md            # This file
├── requirements.txt     # Dependencies
├── setup.py             # Package configuration
├── pytest.ini           # Pytest configuration
├── main.py              # Entry point
└── run_gui.py           # GUI entry point
```

## Error Analysis

- **Energy Conservation**: < 0.1% error over one orbit
- **Orbit Period**: < 100 km position error after one period
- **Numerical Stability**: RK4 method provides stable results for typical orbit scenarios
- **Step Size**: Adaptive RK45 automatically adjusts for optimal accuracy
- **Performance**: Numba JIT compilation provides significant speedup

## Technical Details

- **Language**: Python 3.8+
- **Dependencies**: NumPy, SciPy, Matplotlib, pytest, tqdm, Plotly, Numba, PyQt5
- **Numerical Methods**: RK4, Adaptive RK45 (Cash-Karp)
- **Force Models**: Two-body gravity, J2 perturbation, high-fidelity atmospheric drag, third-body perturbations, solar radiation pressure, relativistic effects, multi-body dynamics
- **Visualization**: Matplotlib 3D, Animation, Plotly interactive 3D
- **Mission Design**: Hohmann transfer, bi-elliptic transfer, gravity assist, multi-burn transfer, optimal transfer
- **Conjunction Analysis**: Minimum distance calculation, collision probability estimation
- **GUI**: PyQt5-based graphical user interface
- **Testing**: Pytest framework
- **Documentation**: Sphinx
- **CI/CD**: GitHub Actions

## License

MIT License

## Author

Rosso Sgroi
