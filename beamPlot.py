import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    def __init__(self):
        self.graph = None
        self.map1 = None
        self.plot1 = None
    
    def plot_beam_pattern(self):
        """Generate the beamforming heatmap plot."""
        self.maps = self.map1
        x = np.linspace(-50, 50, 500)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))  # Example beamforming pattern

        fig, ax = plt.subplots(figsize=(self.maps.width(), self.maps.height()))
        heatmap = ax.imshow(Z, aspect= 'auto', extent=[-100, 100, -100, 100], cmap='viridis')
        ax.set_title("Beamforming Heatmap")
        plt.colorbar(heatmap, ax=ax)
        return fig

    def plot_phase_magnitude(self):
        """Generate the phase-magnitude plot."""
        self.plots = self.plot1
        x = np.linspace(0, 10, 500)
        phase = np.sin(x)
        magnitude = np.cos(x)

        fig, ax = plt.subplots(figsize=(self.plots.width(), self.plots.height()))
        ax.plot(x, phase, label='Phase')
        ax.plot(x, magnitude, label='Magnitude')
        ax.set_title("Phase-Magnitude Plot")
        ax.legend()
        return fig
