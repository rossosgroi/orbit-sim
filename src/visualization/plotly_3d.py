import plotly.graph_objects as go
import numpy as np
from core.bodies import CelestialBody


def plotly_3d_orbit(states, body: CelestialBody, title: str = "Orbit Visualization"):
    """
    Create an interactive 3D orbit visualization using Plotly
    
    Args:
        states: Array of state vectors
        body: Celestial body around which the orbit is plotted
        title: Title of the plot
        
    Returns:
        plotly.graph_objects.Figure: Interactive 3D plot
    """
    # Extract positions from states
    positions = states[:, :3]
    
    # Create figure
    fig = go.Figure()
    
    # Add celestial body
    fig.add_trace(
        go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode='markers',
            marker=dict(
                size=body.radius / 1000,  # Scale down for better visualization
                color='blue',
                opacity=0.8
            ),
            name=body.name
        )
    )
    
    # Add orbit trajectory
    fig.add_trace(
        go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2],
            mode='lines',
            line=dict(
                color='red',
                width=2
            ),
            name='Orbit'
        )
    )
    
    # Add spacecraft position
    fig.add_trace(
        go.Scatter3d(
            x=[positions[-1, 0]],
            y=[positions[-1, 1]],
            z=[positions[-1, 2]],
            mode='markers',
            marker=dict(
                size=5,
                color='green'
            ),
            name='Spacecraft'
        )
    )
    
    # Set layout
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (km)',
            yaxis_title='Y (km)',
            zaxis_title='Z (km)',
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    return fig


def animate_orbit(states, body: CelestialBody, title: str = "Orbit Animation"):
    """
    Create an animated 3D orbit visualization using Plotly
    
    Args:
        states: Array of state vectors
        body: Celestial body around which the orbit is plotted
        title: Title of the animation
        
    Returns:
        plotly.graph_objects.Figure: Animated 3D plot
    """
    # Extract positions from states
    positions = states[:, :3]
    n_frames = len(positions)
    
    # Create figure
    fig = go.Figure()
    
    # Add celestial body
    fig.add_trace(
        go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode='markers',
            marker=dict(
                size=body.radius / 1000,  # Scale down for better visualization
                color='blue',
                opacity=0.8
            ),
            name=body.name
        )
    )
    
    # Add orbit trajectory
    fig.add_trace(
        go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2],
            mode='lines',
            line=dict(
                color='red',
                width=2
            ),
            name='Orbit'
        )
    )
    
    # Add spacecraft position (will be animated)
    fig.add_trace(
        go.Scatter3d(
            x=[positions[0, 0]],
            y=[positions[0, 1]],
            z=[positions[0, 2]],
            mode='markers',
            marker=dict(
                size=5,
                color='green'
            ),
            name='Spacecraft'
        )
    )
    
    # Create frames for animation
    frames = []
    for i in range(n_frames):
        frames.append(
            go.Frame(
                data=[
                    go.Scatter3d(
                        x=[0],
                        y=[0],
                        z=[0],
                        mode='markers',
                        marker=dict(
                            size=body.radius / 1000,
                            color='blue',
                            opacity=0.8
                        ),
                        name=body.name
                    ),
                    go.Scatter3d(
                        x=positions[:, 0],
                        y=positions[:, 1],
                        z=positions[:, 2],
                        mode='lines',
                        line=dict(
                            color='red',
                            width=2
                        ),
                        name='Orbit'
                    ),
                    go.Scatter3d(
                        x=[positions[i, 0]],
                        y=[positions[i, 1]],
                        z=[positions[i, 2]],
                        mode='markers',
                        marker=dict(
                            size=5,
                            color='green'
                        ),
                        name='Spacecraft'
                    )
                ],
                name=str(i)
            )
        )
    
    # Set layout with animation
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (km)',
            yaxis_title='Y (km)',
            zaxis_title='Z (km)',
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[
                            None,
                            dict(
                                frame=dict(duration=50, redraw=True),
                                fromcurrent=True,
                                transition=dict(duration=0)
                            )
                        ]
                    ),
                    dict(
                        label='Pause',
                        method='animate',
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=False),
                                mode='immediate',
                                transition=dict(duration=0)
                            )
                        ]
                    )
                ]
            )
        ]
    )
    
    # Add frames to figure
    fig.frames = frames
    
    return fig
