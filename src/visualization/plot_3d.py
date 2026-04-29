import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ..core.bodies import EARTH

def plot_3d_orbit(states, body=EARTH, title="Orbit Visualization"):
    """
    Plot 3D orbit
    
    Args:
        states: Array of state vectors
        body: Celestial body (default: Earth)
        title: Plot title
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Extract positions
    positions = states[:, :3]
    
    # Plot orbit
    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', label='Orbit')
    
    # Plot start and end points
    ax.plot([positions[0, 0]], [positions[0, 1]], [positions[0, 2]], 'go', markersize=8, label='Start')
    ax.plot([positions[-1, 0]], [positions[-1, 1]], [positions[-1, 2]], 'ro', markersize=8, label='End')
    
    # Plot celestial body
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    x = body.radius * np.cos(u) * np.sin(v)
    y = body.radius * np.sin(u) * np.sin(v)
    z = body.radius * np.cos(v)
    ax.plot_surface(x, y, z, color='blue', alpha=0.3)
    
    # Set labels and title
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.set_title(title)
    
    # Set equal aspect ratio
    max_range = np.max(np.abs(positions))
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    # Add legend
    ax.legend()
    
    plt.tight_layout()
    return fig, ax

def plot_energy(times, energies, title="Energy Conservation"):
    """
    Plot energy vs time
    
    Args:
        times: Array of time points (s)
        energies: Array of energy values (km^2/s^2)
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Convert times to days for better readability
    times_days = np.array(times) / 86400
    
    # Plot energy
    ax.plot(times_days, energies, 'g-')
    
    # Set labels and title
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Energy (km²/s²)')
    ax.set_title(title)
    
    # Calculate and display energy error
    energy_error = abs((energies[-1] - energies[0]) / energies[0]) * 100
    ax.text(0.05, 0.95, f"Energy error: {energy_error:.6f}%", 
            transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    return fig, ax

def plot_orbital_elements(times, elements, title="Orbital Elements Evolution"):
    """
    Plot orbital elements vs time
    
    Args:
        times: Array of time points (s)
        elements: Array of Keplerian elements
        title: Plot title
    """
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    
    # Convert times to days
    times_days = np.array(times) / 86400
    
    # Extract elements
    a = [el.a for el in elements]
    e = [el.e for el in elements]
    i = [el.i for el in elements]
    raan = [el.raan for el in elements]
    argp = [el.argp for el in elements]
    nu = [el.nu for el in elements]
    
    # Plot semi-major axis
    axs[0, 0].plot(times_days, a, 'b-')
    axs[0, 0].set_ylabel('Semi-major axis (km)')
    axs[0, 0].grid(True)
    
    # Plot eccentricity
    axs[0, 1].plot(times_days, e, 'g-')
    axs[0, 1].set_ylabel('Eccentricity')
    axs[0, 1].grid(True)
    
    # Plot inclination
    axs[1, 0].plot(times_days, np.array(i) * 57.2958, 'r-')
    axs[1, 0].set_ylabel('Inclination (deg)')
    axs[1, 0].grid(True)
    
    # Plot RAAN
    axs[1, 1].plot(times_days, np.array(raan) * 57.2958, 'c-')
    axs[1, 1].set_ylabel('RAAN (deg)')
    axs[1, 1].grid(True)
    
    # Plot argument of perigee
    axs[2, 0].plot(times_days, np.array(argp) * 57.2958, 'm-')
    axs[2, 0].set_ylabel('Arg. of perigee (deg)')
    axs[2, 0].set_xlabel('Time (days)')
    axs[2, 0].grid(True)
    
    # Plot true anomaly
    axs[2, 1].plot(times_days, np.array(nu) * 57.2958, 'y-')
    axs[2, 1].set_ylabel('True anomaly (deg)')
    axs[2, 1].set_xlabel('Time (days)')
    axs[2, 1].grid(True)
    
    plt.suptitle(title)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig, axs