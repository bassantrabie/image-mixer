import numpy as np

class ScenarioParameters:
    def __init__(self):
        self.frequency = None
        self.phase = None
        self.curvature_angle = None
        self.position_between_transmitters = None
        self.num_transmitters = 2
        self.array_geometry = None

    def set_5g_parameters(self):
        self.frequency = 1800000000 
        self.phase = 0 
        self.curvature_angle = 30 
        self.position_between_transmitters = 1  
        self.num_transmitters = 32  
        self.array_geometry = "linear"

    def set_tumor_ablation_parameters(self):
        self.frequency = 900000000 
        self.phase = 0 
        self.curvature_angle = 5  
        self.position_between_transmitters = 2 
        self.num_transmitters = 4  
        self.array_geometry = "curved"
        
    def set_ultrasound_parameters(self):
        self.frequency = 5000000
        self.phase = 0
        self.curvature_angle = 30
        self.position_between_transmitters = 3
        self.num_transmitters = 16
        self.array_geometry = "linear"

    def reset_parameters(self):
        self.frequency = 1000000000
        self.phase = 0
        self.curvature_angle = 30
        self.position_between_transmitters = 5
        self.num_transmitters = 2  
        self.array_geometry = "curved" 
       



    def update_parameters(self, scenario):
        if scenario == "5G":
            self.set_5g_parameters()
        elif scenario == "Tumor Ablation":
            self.set_tumor_ablation_parameters()
        elif scenario == "Ultrasound":
            self.set_ultrasound_parameters()
        else:
            self.reset_parameters()

    def display_parameters(self):
        """Displays the current parameters in a readable format."""
        print(f"Frequency: {self.frequency}")
        print(f"Phase: {self.phase}")
        print(f"Curvature Angle: {self.curvature_angle}")
        print(f"Number of Transmitters: {self.num_transmitters}")

