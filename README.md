# Beamforming Simulator

## Overview
This Beamforming Simulator is a 2D visualization tool designed to help users understand and experiment with beamforming concepts, widely used in modern technologies such as wireless communications, 5G, radar, sonar, and biomedical applications (e.g., ultrasound and tumor ablations). The core concepts implemented in this simulator are delays/phase shifts and constructive/destructive interference.

## Features
- **Real-Time Beam Steering Customization:**
  - Adjust the number of transmitters/receivers.
  - Apply variable delays and phase shifts.
  - Configure multiple operating frequencies and their values.
- **Phased Array Geometry:**
  - Customize the geometry of the phased array (linear or curved with adjustable curvature parameters).
- **Visualization Tools:**
  - Display constructive/destructive interference maps.
  - Beam profile shown in synchronized viewers.
- **Multiple Phased Array Units:**
  - Add multiple phased array units.
  - Customize location and parameters for each unit.
- **Predefined Scenarios:**
  - Three parameter settings files included for direct loading, visualization, and fine-tuning.
  - Scenarios inspired by 5G, Ultrasound, and Tumor Ablation.

## Code Design Principles
### Object-Oriented Programming (OOP)
- Proper encapsulation with minimal code in the main function.
- Separate classes for:
  - **PhasedArray:** Manages array configurations and calculations.
  - **ImageVisualizer:** Handles image display and visualization.
- Avoid code repetition with reusable class structures.

### Logging
- Python's `logging` library is integrated for:
  - Tracking user interactions.
  - Logging major simulation steps.
  - Debugging issues effectively.

## Requirements
- Python 3.x
- Required libraries: `matplotlib`, `numpy`, `logging`

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/MuhamedSalah10/image-mixer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd image-mixer
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the simulator:
   ```bash
   python program.py
   ```

## Usage
- Customize the parameters via the GUI.
- Select predefined scenarios for visualization.
- Fine-tune settings for personalized experimentation.

## File Structure
- `BeamFormingSimulator.py`: Main simulator logic.
- `program.py`: Manages program flow.
- `visulizer.py`: Handles data visualization.
- `beamPlot.py`: Plots beamforming results.
- `scenarios.py`: Contains predefined parameter settings files.
- `task4.ui`: UI definition file.
- `logs/`: Contains log files for debugging purposes.

## Contributing
Contributions are welcome! Please follow the standard GitHub workflow:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Create a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments
Inspired by Matlab's beamforming toolboxes and modern beamforming applications in communications and biomedical technologies.

