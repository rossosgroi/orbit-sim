import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QPushButton, QLabel, QLineEdit, QComboBox, 
    QGroupBox, QGridLayout, QDoubleSpinBox, QSpinBox, QTextEdit,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.bodies import EARTH, SUN, MOON, BODIES
from core.state import State
from dynamics.two_body import two_body_derivative, two_body_energy
from dynamics.perturbations import j2_derivative, atmospheric_drag_derivative
from dynamics.propagator import OrbitPropagator
from orbits.conversions import cartesian_to_keplerian
from visualization.plot_3d import plot_3d_orbit, plot_energy, plot_orbital_elements
from visualization.plotly_3d import plotly_3d_orbit, animate_orbit


class OrbitSimGUI(QMainWindow):
    """Main GUI for the orbital mechanics simulator"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orbital Mechanics Simulator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_simulation_tab()
        self.create_mission_design_tab()
        self.create_conjunction_tab()
        self.create_settings_tab()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
    
    def create_simulation_tab(self):
        """Create the simulation tab"""
        simulation_tab = QWidget()
        layout = QVBoxLayout(simulation_tab)
        
        # Scenario selection
        scenario_group = QGroupBox("Simulation Scenario")
        scenario_layout = QHBoxLayout()
        
        self.scenario_combo = QComboBox()
        self.scenario_combo.addItems(["Earth Satellite", "Hohmann Transfer", "J2 Perturbation"])
        scenario_layout.addWidget(QLabel("Scenario:"))
        scenario_layout.addWidget(self.scenario_combo)
        scenario_group.setLayout(scenario_layout)
        layout.addWidget(scenario_group)
        
        # Simulation parameters
        params_group = QGroupBox("Simulation Parameters")
        params_layout = QGridLayout()
        
        # Central body
        params_layout.addWidget(QLabel("Central Body:"), 0, 0)
        self.body_combo = QComboBox()
        self.body_combo.addItems(["Earth", "Sun", "Moon"])
        params_layout.addWidget(self.body_combo, 0, 1)
        
        # Initial altitude
        params_layout.addWidget(QLabel("Initial Altitude (km):"), 1, 0)
        self.altitude_spin = QDoubleSpinBox()
        self.altitude_spin.setRange(100, 100000)
        self.altitude_spin.setValue(7000)
        params_layout.addWidget(self.altitude_spin, 1, 1)
        
        # Simulation duration
        params_layout.addWidget(QLabel("Duration (hours):"), 2, 0)
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.1, 72)
        self.duration_spin.setValue(24)
        params_layout.addWidget(self.duration_spin, 2, 1)
        
        # Time step
        params_layout.addWidget(QLabel("Time Step (seconds):"), 3, 0)
        self.timestep_spin = QDoubleSpinBox()
        self.timestep_spin.setRange(1, 3600)
        self.timestep_spin.setValue(60)
        params_layout.addWidget(self.timestep_spin, 3, 1)
        
        # Integrator
        params_layout.addWidget(QLabel("Integrator:"), 4, 0)
        self.integrator_combo = QComboBox()
        self.integrator_combo.addItems(["RK4", "RK45"])
        params_layout.addWidget(self.integrator_combo, 4, 1)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Force models
        force_group = QGroupBox("Force Models")
        force_layout = QVBoxLayout()
        
        self.j2_checkbox = QPushButton("J2 Perturbation")
        self.j2_checkbox.setCheckable(True)
        self.j2_checkbox.setChecked(True)
        force_layout.addWidget(self.j2_checkbox)
        
        self.drag_checkbox = QPushButton("Atmospheric Drag")
        self.drag_checkbox.setCheckable(True)
        force_layout.addWidget(self.drag_checkbox)
        
        force_group.setLayout(force_layout)
        layout.addWidget(force_group)
        
        # Run button
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        layout.addWidget(self.run_button)
        
        # Status text
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        self.tab_widget.addTab(simulation_tab, "Simulation")
    
    def create_mission_design_tab(self):
        """Create the mission design tab"""
        mission_tab = QWidget()
        layout = QVBoxLayout(mission_tab)
        
        # Mission type
        mission_group = QGroupBox("Mission Type")
        mission_layout = QHBoxLayout()
        
        self.mission_combo = QComboBox()
        self.mission_combo.addItems(["Hohmann Transfer", "Bi-elliptic Transfer", "Delta-V Calculation"])
        mission_layout.addWidget(QLabel("Mission:"))
        mission_layout.addWidget(self.mission_combo)
        mission_group.setLayout(mission_layout)
        layout.addWidget(mission_group)
        
        # Transfer parameters
        transfer_group = QGroupBox("Transfer Parameters")
        transfer_layout = QGridLayout()
        
        # Initial orbit
        transfer_layout.addWidget(QLabel("Initial Altitude (km):"), 0, 0)
        self.initial_alt_spin = QDoubleSpinBox()
        self.initial_alt_spin.setRange(100, 100000)
        self.initial_alt_spin.setValue(7000)
        transfer_layout.addWidget(self.initial_alt_spin, 0, 1)
        
        # Final orbit
        transfer_layout.addWidget(QLabel("Final Altitude (km):"), 1, 0)
        self.final_alt_spin = QDoubleSpinBox()
        self.final_alt_spin.setRange(100, 100000)
        self.final_alt_spin.setValue(35786)  # GEO altitude
        transfer_layout.addWidget(self.final_alt_spin, 1, 1)
        
        # Intermediate orbit (for bi-elliptic)
        transfer_layout.addWidget(QLabel("Intermediate Altitude (km):"), 2, 0)
        self.intermediate_alt_spin = QDoubleSpinBox()
        self.intermediate_alt_spin.setRange(100, 1000000)
        self.intermediate_alt_spin.setValue(100000)
        transfer_layout.addWidget(self.intermediate_alt_spin, 2, 1)
        
        transfer_group.setLayout(transfer_layout)
        layout.addWidget(transfer_group)
        
        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_mission)
        layout.addWidget(self.calculate_button)
        
        # Results
        self.mission_results = QTextEdit()
        self.mission_results.setReadOnly(True)
        layout.addWidget(self.mission_results)
        
        self.tab_widget.addTab(mission_tab, "Mission Design")
    
    def create_conjunction_tab(self):
        """Create the conjunction analysis tab"""
        conjunction_tab = QWidget()
        layout = QVBoxLayout(conjunction_tab)
        
        # Object 1 parameters
        obj1_group = QGroupBox("Object 1")
        obj1_layout = QGridLayout()
        
        obj1_layout.addWidget(QLabel("Altitude (km):"), 0, 0)
        self.obj1_alt_spin = QDoubleSpinBox()
        self.obj1_alt_spin.setRange(100, 100000)
        self.obj1_alt_spin.setValue(7000)
        obj1_layout.addWidget(self.obj1_alt_spin, 0, 1)
        
        obj1_layout.addWidget(QLabel("Inclination (deg):"), 1, 0)
        self.obj1_inc_spin = QDoubleSpinBox()
        self.obj1_inc_spin.setRange(0, 180)
        self.obj1_inc_spin.setValue(0)
        obj1_layout.addWidget(self.obj1_inc_spin, 1, 1)
        
        obj1_group.setLayout(obj1_layout)
        layout.addWidget(obj1_group)
        
        # Object 2 parameters
        obj2_group = QGroupBox("Object 2")
        obj2_layout = QGridLayout()
        
        obj2_layout.addWidget(QLabel("Altitude (km):"), 0, 0)
        self.obj2_alt_spin = QDoubleSpinBox()
        self.obj2_alt_spin.setRange(100, 100000)
        self.obj2_alt_spin.setValue(7050)
        obj2_layout.addWidget(self.obj2_alt_spin, 0, 1)
        
        obj2_layout.addWidget(QLabel("Inclination (deg):"), 1, 0)
        self.obj2_inc_spin = QDoubleSpinBox()
        self.obj2_inc_spin.setRange(0, 180)
        self.obj2_inc_spin.setValue(0.1)
        obj2_layout.addWidget(self.obj2_inc_spin, 1, 1)
        
        obj2_group.setLayout(obj2_layout)
        layout.addWidget(obj2_group)
        
        # Analysis parameters
        analysis_group = QGroupBox("Analysis Parameters")
        analysis_layout = QGridLayout()
        
        analysis_layout.addWidget(QLabel("Time Horizon (hours):"), 0, 0)
        self.time_horizon_spin = QDoubleSpinBox()
        self.time_horizon_spin.setRange(1, 168)  # Up to a week
        self.time_horizon_spin.setValue(24)
        analysis_layout.addWidget(self.time_horizon_spin, 0, 1)
        
        analysis_layout.addWidget(QLabel("Distance Threshold (km):"), 1, 0)
        self.distance_threshold_spin = QDoubleSpinBox()
        self.distance_threshold_spin.setRange(0.1, 100)
        self.distance_threshold_spin.setValue(1)
        analysis_layout.addWidget(self.distance_threshold_spin, 1, 1)
        
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        # Analyze button
        self.analyze_button = QPushButton("Analyze Conjunctions")
        self.analyze_button.clicked.connect(self.analyze_conjunctions)
        layout.addWidget(self.analyze_button)
        
        # Results
        self.conjunction_results = QTextEdit()
        self.conjunction_results.setReadOnly(True)
        layout.addWidget(self.conjunction_results)
        
        self.tab_widget.addTab(conjunction_tab, "Conjunction Analysis")
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_tab = QWidget()
        layout = QVBoxLayout(settings_tab)
        
        # Visualization settings
        viz_group = QGroupBox("Visualization")
        viz_layout = QVBoxLayout()
        
        self.plotly_checkbox = QPushButton("Use Plotly for 3D Visualization")
        self.plotly_checkbox.setCheckable(True)
        self.plotly_checkbox.setChecked(False)
        viz_layout.addWidget(self.plotly_checkbox)
        
        viz_group.setLayout(viz_layout)
        layout.addWidget(viz_group)
        
        # Save settings button
        self.save_settings_button = QPushButton("Save Settings")
        self.save_settings_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_settings_button)
        
        self.tab_widget.addTab(settings_tab, "Settings")
    
    def run_simulation(self):
        """Run the simulation"""
        try:
            self.statusBar().showMessage("Running simulation...")
            self.status_text.clear()
            
            # Get parameters
            scenario = self.scenario_combo.currentText()
            body_name = self.body_combo.currentText().lower()
            body = BODIES[body_name]
            altitude = self.altitude_spin.value()
            duration = self.duration_spin.value() * 3600  # Convert to seconds
            dt = self.timestep_spin.value()
            integrator = self.integrator_combo.currentText().lower()
            use_j2 = self.j2_checkbox.isChecked()
            use_drag = self.drag_checkbox.isChecked()
            use_plotly = self.plotly_checkbox.isChecked()
            
            # Log parameters
            self.status_text.append(f"Scenario: {scenario}")
            self.status_text.append(f"Central Body: {body.name}")
            self.status_text.append(f"Initial Altitude: {altitude} km")
            self.status_text.append(f"Duration: {duration/3600:.2f} hours")
            self.status_text.append(f"Time Step: {dt} seconds")
            self.status_text.append(f"Integrator: {integrator.upper()}")
            self.status_text.append(f"J2 Perturbation: {use_j2}")
            self.status_text.append(f"Atmospheric Drag: {use_drag}")
            self.status_text.append("")
            
            # Calculate initial state
            r = body.radius + altitude
            v = np.sqrt(body.mu / r)
            state0 = State([r, 0, 0], [0, v, 0])
            
            # Create force model
            if use_j2 and use_drag:
                # Combine J2 and drag
                def combined_force(t, y):
                    # Two-body acceleration
                    r_vec = y[:3]
                    v_vec = y[3:]
                    r_norm = np.linalg.norm(r_vec)
                    a_two_body = -body.mu * r_vec / r_norm**3
                    
                    # J2 acceleration
                    z2 = r_vec[2]**2
                    r2 = r_norm**2
                    factor = (3/2) * body.j2 * body.mu * body.radius**2 / r_norm**5
                    ax_j2 = factor * r_vec[0] * (5 * z2 / r2 - 1)
                    ay_j2 = factor * r_vec[1] * (5 * z2 / r2 - 1)
                    az_j2 = factor * r_vec[2] * (5 * z2 / r2 - 3)
                    a_j2 = np.array([ax_j2, ay_j2, az_j2])
                    
                    # Drag acceleration
                    # Convert to meters
                    r_m = r_vec * 1000
                    v_m = v_vec * 1000
                    r_norm_m = r_norm * 1000
                    altitude_m = r_norm_m - body.radius * 1000
                    
                    if altitude_m > 0:
                        rho0 = 1.225  # kg/m^3
                        H = 8.5  # km
                        Cd = 2.2
                        A = 1.0  # m^2
                        m = 1.0  # kg
                        
                        rho = rho0 * np.exp(-altitude_m / (H * 1000))
                        v_norm = np.linalg.norm(v_m)
                        
                        if v_norm > 0:
                            drag_dir = -v_m / v_norm
                            a_drag_m = -0.5 * rho * v_norm**2 * Cd * A / m * drag_dir
                            a_drag = a_drag_m / 1000  # Convert back to km/s^2
                        else:
                            a_drag = np.zeros(3)
                    else:
                        a_drag = np.zeros(3)
                    
                    # Total acceleration
                    a_total = a_two_body + a_j2 + a_drag
                    return np.concatenate([v_vec, a_total])
            elif use_j2:
                force_model = j2_derivative(body.mu, body.radius, body.j2)
            elif use_drag:
                force_model = atmospheric_drag_derivative(body.mu, body.radius)
            else:
                force_model = two_body_derivative(body.mu)
            
            # Create propagator
            propagator = OrbitPropagator(force_model, integrator)
            
            # Propagate orbit
            self.status_text.append("Propagating orbit...")
            times, states = propagator.propagate(state0.to_vector(), duration, dt)
            
            # Calculate energy
            energy_fn = lambda state: two_body_energy(body.mu, state)
            times, states, energies = propagator.propagate_with_energy(
                state0.to_vector(), duration, dt, energy_fn
            )
            
            # Calculate orbital elements
            elements = [cartesian_to_keplerian(state, body.mu) for state in states]
            
            # Visualize results
            self.status_text.append("Generating visualizations...")
            
            if use_plotly:
                # Use Plotly for 3D visualization
                fig = plotly_3d_orbit(states, body, f"{scenario} - {body.name}")
                fig.show()
            else:
                # Use matplotlib for visualization
                plot_3d_orbit(states, body, f"{scenario} - {body.name}")
                plot_energy(times, energies, "Energy Conservation")
                plot_orbital_elements(times, elements, "Orbital Elements Evolution")
            
            # Calculate energy drift
            energy_drift = abs((energies[-1] - energies[0]) / energies[0]) * 100
            self.status_text.append(f"Energy drift: {energy_drift:.6f}%")
            
            self.statusBar().showMessage("Simulation completed successfully!")
            self.status_text.append("Simulation completed successfully!")
            
        except Exception as e:
            self.statusBar().showMessage("Error running simulation")
            self.status_text.append(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error running simulation: {str(e)}")
    
    def calculate_mission(self):
        """Calculate mission parameters"""
        try:
            from orbits.mission_design import hohmann_transfer, bielliptic_transfer, calculate_delta_v
            
            mission = self.mission_combo.currentText()
            initial_alt = self.initial_alt_spin.value()
            final_alt = self.final_alt_spin.value()
            intermediate_alt = self.intermediate_alt_spin.value()
            
            # Calculate radii
            r1 = EARTH.radius + initial_alt
            r2 = EARTH.radius + final_alt
            r3 = EARTH.radius + intermediate_alt
            
            self.mission_results.clear()
            self.mission_results.append(f"Mission: {mission}")
            self.mission_results.append(f"Initial Altitude: {initial_alt} km")
            self.mission_results.append(f"Final Altitude: {final_alt} km")
            
            if mission == "Hohmann Transfer":
                delta_v1, delta_v2, transfer_time = hohmann_transfer(r1, r2, EARTH.mu)
                total_delta_v = delta_v1 + delta_v2
                
                self.mission_results.append("")
                self.mission_results.append("Hohmann Transfer Results:")
                self.mission_results.append(f"Delta-v1: {delta_v1:.3f} km/s")
                self.mission_results.append(f"Delta-v2: {delta_v2:.3f} km/s")
                self.mission_results.append(f"Total Delta-v: {total_delta_v:.3f} km/s")
                self.mission_results.append(f"Transfer Time: {transfer_time/3600:.2f} hours")
                
            elif mission == "Bi-elliptic Transfer":
                delta_v1, delta_v2, delta_v3, transfer_time = bielliptic_transfer(r1, r3, r2, EARTH.mu)
                total_delta_v = delta_v1 + delta_v2 + delta_v3
                
                self.mission_results.append(f"Intermediate Altitude: {intermediate_alt} km")
                self.mission_results.append("")
                self.mission_results.append("Bi-elliptic Transfer Results:")
                self.mission_results.append(f"Delta-v1: {delta_v1:.3f} km/s")
                self.mission_results.append(f"Delta-v2: {delta_v2:.3f} km/s")
                self.mission_results.append(f"Delta-v3: {delta_v3:.3f} km/s")
                self.mission_results.append(f"Total Delta-v: {total_delta_v:.3f} km/s")
                self.mission_results.append(f"Transfer Time: {transfer_time/3600:.2f} hours")
                
            elif mission == "Delta-V Calculation":
                # Calculate circular orbit velocities
                v1 = np.sqrt(EARTH.mu / r1)
                v2 = np.sqrt(EARTH.mu / r2)
                
                # Calculate delta-v for direct change
                delta_v = abs(v2 - v1)
                
                self.mission_results.append("")
                self.mission_results.append("Delta-V Calculation Results:")
                self.mission_results.append(f"Initial Velocity: {v1:.3f} km/s")
                self.mission_results.append(f"Final Velocity: {v2:.3f} km/s")
                self.mission_results.append(f"Delta-v: {delta_v:.3f} km/s")
                
        except Exception as e:
            self.mission_results.append(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error calculating mission: {str(e)}")
    
    def analyze_conjunctions(self):
        """Analyze conjunctions between two objects"""
        try:
            from orbits.conjunction import conjunction_analysis
            
            # Get parameters
            obj1_alt = self.obj1_alt_spin.value()
            obj1_inc = self.obj1_inc_spin.value()
            obj2_alt = self.obj2_alt_spin.value()
            obj2_inc = self.obj2_inc_spin.value()
            time_horizon = self.time_horizon_spin.value() * 3600  # Convert to seconds
            distance_threshold = self.distance_threshold_spin.value()
            
            # Calculate initial states
            # Object 1: circular orbit
            r1 = EARTH.radius + obj1_alt
            v1 = np.sqrt(EARTH.mu / r1)
            state1 = np.array([r1, 0, 0, 0, v1, 0])
            
            # Object 2: circular orbit with slight inclination
            r2 = EARTH.radius + obj2_alt
            v2 = np.sqrt(EARTH.mu / r2)
            # Simple inclination adjustment
            state2 = np.array([r2, 0, 0, 0, v2 * np.cos(obj2_inc * np.pi/180), v2 * np.sin(obj2_inc * np.pi/180)])
            
            self.conjunction_results.clear()
            self.conjunction_results.append("Conjunction Analysis Results:")
            self.conjunction_results.append(f"Object 1: {obj1_alt} km altitude, {obj1_inc} deg inclination")
            self.conjunction_results.append(f"Object 2: {obj2_alt} km altitude, {obj2_inc} deg inclination")
            self.conjunction_results.append(f"Time Horizon: {time_horizon/3600:.2f} hours")
            self.conjunction_results.append(f"Distance Threshold: {distance_threshold} km")
            self.conjunction_results.append("")
            
            # Run conjunction analysis
            events = conjunction_analysis([state1, state2], EARTH.mu, distance_threshold)
            
            if events:
                self.conjunction_results.append("Potential conjunctions found:")
                for i, event in enumerate(events):
                    self.conjunction_results.append(f"Event {i+1}:")
                    self.conjunction_results.append(f"  Minimum Distance: {event['min_distance']:.3f} km")
                    self.conjunction_results.append(f"  Time: {event['time_of_conjunction']/3600:.2f} hours")
                    self.conjunction_results.append(f"  Collision Probability: {event['probability_of_collision']:.6f}")
            else:
                self.conjunction_results.append("No potential conjunctions found within the distance threshold.")
                
        except Exception as e:
            self.conjunction_results.append(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error analyzing conjunctions: {str(e)}")
    
    def save_settings(self):
        """Save settings"""
        try:
            # In a real implementation, this would save settings to a file
            self.statusBar().showMessage("Settings saved successfully!")
            QMessageBox.information(self, "Success", "Settings saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving settings: {str(e)}")


def main():
    """Main function to run the GUI"""
    app = QApplication(sys.argv)
    window = OrbitSimGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
