import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from ..core.bodies import EARTH

def animate_orbit(states, body=EARTH, title="Orbit Animation", interval=50):
    """
    Animate orbit
    
    Args:
        states: Array of state vectors
        body: Celestial body (default: Earth)
        title: Animation title
        interval: Time between frames (ms)
        
    Returns:
        FuncAnimation: Animation object
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Extract positions
    positions = states[:, :3]
    
    # Plot orbit path
    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', label='Orbit')
    
    # Plot celestial body
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    x = body.radius * np.cos(u) * np.sin(v)
    y = body.radius * np.sin(u) * np.sin(v)
    z = body.radius * np.cos(v)
    ax.plot_surface(x, y, z, color='blue', alpha=0.3)
    
    # Initialize satellite marker
    satellite, = ax.plot([], [], [], 'ro', markersize=8, label='Satellite')
    
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
    
    def update(frame):
        """Update function for animation"""
        # Update satellite position
        satellite.set_data(positions[frame, 0], positions[frame, 1])
        satellite.set_3d_properties(positions[frame, 2])
        return satellite,
    
    # Create animation
    anim = FuncAnimation(
        fig, update, frames=len(positions), interval=interval, blit=True
    )
    
    plt.tight_layout()
    return anim