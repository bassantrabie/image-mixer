import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QGraphicsView, QGraphicsScene,
                             QGraphicsPixmapItem)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QIcon
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5 import uic
from matplotlib import cm
from matplotlib.colors import Normalize
from PyQt5.QtWidgets import QMainWindow, QTabWidget
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QPushButton, QWidget, QHBoxLayout , QDesktopWidget, QLabel, QSlider, QSizePolicy
from pprint import pprint
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import math
from pyqtgraph import ROI, LinearRegionItem

import sys
import numpy as np
from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QGraphicsView, QGraphicsScene,QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage, QPainter, QIcon
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5 import uic
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from matplotlib import cm
from matplotlib.colors import Normalize
from PyQt5.QtWidgets import  QTabWidget
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QPushButton, QWidget, QHBoxLayout , QDesktopWidget, QLabel
from pprint import pprint
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt


# Emitter class
class Emitter:
    def __init__(self, x, y, c, frequency, phi, spacing):
        self.r = np.array([x, y])
        self.c = c
        self.frequency = frequency
        self.phi = phi
        self.spacing = spacing


# EmitterArray class
class EmitterArray:
    def __init__(self):
        self.emitters = []

    def AddEmitter(self, emitter):
        self.emitters.append(emitter)


# Main Window
class SecondWindow(QTabWidget):
    def __init__(self):

        super(SecondWindow, self).__init__()
        
        uic.loadUi("Final_Middle.ui", self)

        self.spinBox_Frequency.setValue(1)
        # self.spinBox_nTransmiter.setValue(3)
        self.spinBox_Frequency.setDecimals(5)
        self.spinBox_nTransmiter.setRange(0, 200)
        self.spinBox_Frequency.setRange(1e-3, 100)  # Range in GHz (0.001 GHz to 50 GHz)


        self.graphicsView = QGraphicsView()
        self.layout_map = QVBoxLayout(self.widget_map)
        self.layout_map.addWidget(self.graphicsView)
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QPainter.Antialiasing, True)

        self.widget_2_layout = QVBoxLayout(self.widget_2)      
        self.fig_2 = plt.figure()
        self.canvas_2 = FigureCanvas(self.fig_2)
        self.widget_2_layout.addWidget(self.canvas_2)

        # Create an object of class
        self.emitter_array = EmitterArray()
        
        # Connect the signal of the spinBox to the update function

        self.stop_values = [0, 45, 90, 135, 180, 225, 270, 315, 360]
        self.slider_Phase.setRange(0, 8)  # 8 stops: 0, 1, ..., 7
        self.slider_Phase.setTickPosition(QSlider.TicksBelow)
        self.slider_Phase.setTickInterval(1)  # Interval matches the stops
        self.slider_Phase.setSingleStep(1)  # Prevent in-between values
        
        self.spinBox_nTransmiter.valueChanged.connect(self.update_info)  
        self.spinBox_Frequency.valueChanged.connect(self.update_info) 
        self.spinBox_Radius.valueChanged.connect(self.update_info)     
        self.lineEdit_xPosition.returnPressed.connect(self.update_info)  
        self.lineEdit_yPosition.returnPressed.connect(self.update_info)   
        self.slider_Phase.valueChanged.connect(self.update_info)       
        self.pushButton_Reset.clicked.connect(self.on_reset_clicked)
        self.comboBox_Distance.currentIndexChanged.connect(self.update_info)
        self.comboBox_Geometry.currentIndexChanged.connect(self.update_info)
        # self.slider_Phase.valueChanged.connect(self.update_value_label)
        if self.comboBox_Geometry.currentText() == "Curved" :
            self.spinBox_Radius.valueChanged.connect(self.update_info) 
        else: 
            self.spinBox_Radius.setValue(0)
            self.update_info()
        
        self.draw_scenarios()
        self.comboBox.currentIndexChanged.connect(self.draw_scenarios)
        
    def update_info(self):
        self.emitter_array.emitters.clear()
        print("Parameter changed, updating plot...")
        param = self.get_parameters()  
        self.assign_emitters(param)    
        self.plot_interference_map()   
        print("Information updated and plot refreshed.")
        self.plot_second_graph(param)

    def draw_scenarios(self):
        scenario = self.comboBox.currentText()
        
        # Temporarily disconnect signals to prevent unwanted updates
        self.disconnect_ui_signals()
        
        # Reset ranges for "Scenarios" (free mode)
        if scenario == "Scenarios":
            # Set wide ranges for all inputs
            self.spinBox_nTransmiter.setMinimum(1)
            self.spinBox_nTransmiter.setMaximum(1000)
            self.spinBox_Frequency.setMinimum(1e-6)  # 1 kHz
            self.spinBox_Frequency.setMaximum(1e3)   # 1000 GHz
            self.spinBox_Radius.setMinimum(0)
            self.spinBox_Radius.setMaximum(100)
            
            # Get current parameters without validation
            param = self.get_parameters()
            
            # Update UI with current parameters
            self.show_scenarios_prameters(param)
            
            # Reconnect signals
            self.connect_ui_signals()
            
            # Plot with current parameters
            self.emitter_array.emitters.clear()
            self.assign_emitters(param)
            self.plot_interference_map()
            self.plot_second_graph(param)
            return
        
        # Handle specific scenarios
        scenario_ranges = {

            # Higher Frequency
            # ---------------------
            # 5G:
            # Pros: Higher data rates and capacity for communication.
            # Cons: Increased signal attenuation, leading to reduced range and penetration (e.g., through walls).
            # Lower Frequency
            # ----------------------
            # 5G:
            # Pros: Better range and penetration, even through obstacles.
            # Cons: Reduced data capacity and slower transmission speeds.
            # Increasing Emitters
            #------------------------
            # 5G:
            # Pros: Enhanced beamforming capabilities, allowing better directional control and efficiency.
            # Cons: Increased system complexity and potential cost.
            # Decreasing Emitters
            #-------------------------
            # 5G:
            # Pros: Simpler, cheaper systems.
            # Cons: Reduced beamforming efficiency and lower overall performance.
            "5G": {
                "frequency": (24e9, 40e9),
                "n_transmitters": (16, 128),
                "radius": (0, 10)
            },
            # Higher Frequency
            # ---------------------
            # Tumor Ablation:
            # Pros: Improved precision and focus for targeting small areas.
            # Cons: Reduced penetration depth in tissues.
            # Lower Frequency
            # ----------------------
            # Tumor Ablation:
            # Pros: Increased penetration depth for reaching deeper tissues.
            # Cons: Less precise focus, potentially affecting surrounding tissues.
            # Increasing Emitters
            #------------------------
            # Tumor Ablation:
            # Pros: Higher precision in focusing energy on the tumor while sparing healthy tissues.
            # Cons: More complex hardware setup and energy management.
            # Decreasing Emitters
            #-------------------------
            # Tumor Ablation:
            # Pros: Simpler equipment with lower energy requirements.
            # Cons: Reduced precision, possibly affecting non-target areas.
            "Tumer Albation": {
                "frequency": (0.5e6, 3e6),
                "n_transmitters": (32, 128),
                "radius": (0, 5)
            },
            # Higher Frequency
            # ---------------------
            # Ultrasound:
            # Pros: Higher resolution in imaging.
            # Cons: Lower penetration depth, making it harder to reach deeper tissues.
            # Lower Frequency
            # ----------------------
            # Ultrasound:
            # Pros: Better penetration depth for imaging or treatment of deeper regions.
            # Cons: Lower image resolution
            # Increasing Emitters
            #------------------------
            # Ultrasound:
            # Pros: Improved image resolution and coverage for larger or complex areas.
            # Cons: Higher power requirements and system complexity.
            # Decreasing Emitters
            #-------------------------
            # Ultrasound:
            # Pros: Lower power usage and simpler setups.
            # Cons: Reduced image quality and smaller coverage.
            "Ultrasound": {
                "frequency": (1e6, 10e6),
                "n_transmitters": (64, 256),
                "radius": (0, 8)
            }
        }
        
        # Get scenario ranges
        ranges = scenario_ranges.get(scenario, scenario_ranges["Ultrasound"])
        
        # Set default parameters for each scenario
        if scenario == "5G":
            param = [0, 0, 29e9, 0.5, 64, "Linear", 0, 2, 3e8]
        elif scenario == "Tumer Albation":
            param = [0, 0, 1e6, 0.2, 64, "Linear", 0, 2, 1540]
        elif scenario == "Ultrasound":
            param = [0, 0, 5e6, 0.1, 128, "Linear", 0, 5, 1540]
        else:
            param = self.get_parameters()
        
        # Set the ranges for the spinboxes
        self.spinBox_nTransmiter.setMinimum(ranges["n_transmitters"][0])
        self.spinBox_nTransmiter.setMaximum(ranges["n_transmitters"][1])
        
        # Convert frequency range to GHz for spinbox
        min_freq_ghz = ranges["frequency"][0] / 1e9
        max_freq_ghz = ranges["frequency"][1] / 1e9
        self.spinBox_Frequency.setMinimum(min_freq_ghz)
        self.spinBox_Frequency.setMaximum(max_freq_ghz)
        
        self.spinBox_Radius.setMinimum(ranges["radius"][0])
        self.spinBox_Radius.setMaximum(ranges["radius"][1])
        
        # Validate and adjust parameters if needed
        current_transmitters = self.spinBox_nTransmiter.value()
        if not ranges["n_transmitters"][0] <= current_transmitters <= ranges["n_transmitters"][1]:
            self.spinBox_nTransmiter.setValue(param[4])
            
        current_freq = self.spinBox_Frequency.value() * 1e9
        if not ranges["frequency"][0] <= current_freq <= ranges["frequency"][1]:
            self.spinBox_Frequency.setValue(param[2] / 1e9)
            
        current_radius = self.spinBox_Radius.value()
        if not ranges["radius"][0] <= current_radius <= ranges["radius"][1]:
            self.spinBox_Radius.setValue(param[6])

        # Update UI with validated parameters
        self.show_scenarios_prameters(param)
        
        # Reconnect signals
        self.connect_ui_signals()

        # Plot with validated parameters
        if (ranges["n_transmitters"][0] <= param[4] <= ranges["n_transmitters"][1] and
            ranges["frequency"][0] <= param[2] <= ranges["frequency"][1] and
            ranges["radius"][0] <= param[6] <= ranges["radius"][1]):
            
            self.emitter_array.emitters.clear()
            self.assign_emitters(param)
            self.plot_interference_map()
            self.plot_second_graph(param)
        else:
            print("Error: Parameters out of range. Please adjust values within the allowed ranges.")
            self.scene.clear()
            

    def show_scenarios_prameters(self, param):
                self.lineEdit_xPosition.setText(str(param[0]))
                self.lineEdit_yPosition.setText(str(param[1]))
                self.spinBox_Frequency.setValue(param[2]/1e9)
                
                self.spinBox_nTransmiter.setValue(param[4])
                self.comboBox_Geometry.setCurrentText(str(param[5]))
                self.spinBox_Radius.setValue(int(param[6]))
                self.lineEdit_Speed.setText(str(param[8]))
                if param[3] == 0.5 :
                    self.slider_Phase.setValue(3)
                elif param[3] == 0.2 :
                    self.slider_Phase.setValue(0)
                else :
                    self.slider_Phase.setValue(1)
                if param[7] == 1:
                    self.comboBox_Distance.setCurrentText("λ")
                elif param[7] == 2:
                    self.comboBox_Distance.setCurrentText("λ/2")
                elif param[7] == 5:
                    self.comboBox_Distance.setCurrentText("λ/5")

    def disconnect_ui_signals(self):
        self.spinBox_nTransmiter.valueChanged.disconnect(self.update_info)
        self.spinBox_Frequency.valueChanged.disconnect(self.update_info)
        self.spinBox_Radius.valueChanged.disconnect(self.update_info)
        self.lineEdit_xPosition.returnPressed.disconnect(self.update_info)
        self.lineEdit_yPosition.returnPressed.disconnect(self.update_info)
        self.slider_Phase.valueChanged.disconnect(self.update_info)
        self.comboBox_Distance.currentIndexChanged.disconnect(self.update_info)
        self.comboBox_Geometry.currentIndexChanged.disconnect(self.update_info)

    def connect_ui_signals(self):
        self.spinBox_nTransmiter.valueChanged.connect(self.update_info)
        self.spinBox_Frequency.valueChanged.connect(self.update_info)
        self.spinBox_Radius.valueChanged.connect(self.update_info)
        self.lineEdit_xPosition.returnPressed.connect(self.update_info)
        self.lineEdit_yPosition.returnPressed.connect(self.update_info)
        self.slider_Phase.valueChanged.connect(self.update_info)
        self.comboBox_Distance.currentIndexChanged.connect(self.update_info)
        self.comboBox_Geometry.currentIndexChanged.connect(self.update_info)


    def on_reset_clicked(self):
        self.emitter_array.emitters.clear()
        self.scene.clear()
        

    def get_parameters(self):
            x = -float(self.lineEdit_xPosition.text())
            y = -float(self.lineEdit_yPosition.text())
            frequency = self.spinBox_Frequency.value() * 1e9
            phase = float(self.slider_Phase.value() * 45) * np.pi / 180  
            emitterNUmber = self.spinBox_nTransmiter.value()
            geometry = self.comboBox_Geometry.currentText()
            curvature = self.spinBox_Radius.value()
            c = self.lineEdit_Speed.text()

            if self.comboBox_Distance.currentText() == "λ":
                spacing = 1
            elif self.comboBox_Distance.currentText() == "5λ/8":
                spacing = 8/5
            elif self.comboBox_Distance.currentText() == "λ/2":
                spacing = 2
            elif self.comboBox_Distance.currentText() == "3λ/8":
                spacing = 8/3
            elif self.comboBox_Distance.currentText() == "λ/4":
                spacing = 4
            elif self.comboBox_Distance.currentText() == "λ/5":
                spacing = 5
            else:
                spacing = 8
            return [x, y, frequency, phase, emitterNUmber, geometry, curvature, spacing, c]
            ##      0  1     2         3          4           5          6         7     8

    def assign_emitters(self, param):
            lambda0 = float(param[8])/param[2]
            distance = lambda0/param[7]
    
            if (param[4]-1) == 0:
                phaseIncrement = param[3]/(2-1)
            else: phaseIncrement = param[3]/(param[4]-1)

            xc = []
            yc = []
            xs = []
            ys = []

            m = (param[4] - 1) / 2
            for i in range (param[4]):
                xc.append(param[0] + (i - m) * distance)
            yc = np.full(param[4],param[1])
            
            if param[5] == "Linear":
                xs = xc
                ys = yc
            else:  
                r = param[6]  
                if r == 0:
                    r = 0.001
                num_emitters = param[4]

                delta_theta = distance / r  
                mid_angle = 0  
                start_angle = mid_angle - delta_theta * (num_emitters - 1) / 2

                for i in range(num_emitters):
                    theta = start_angle + i * delta_theta
                    # Compute x and y positions based on the angle
                    x = param[0] + r * np.sin(theta)  
                    y = param[1] - r * (1 - np.cos(theta))  

                    xs.append(x)
                    ys.append(y)

                # DEBBUG
                print("Emitter positions:")
                for idx, (x, y) in enumerate(zip(xs, ys)):
                    print(f"Emitter {idx + 1}: x = {x:.3f}, y = {y:.3f}")


            for i in range (param[4]):
                emitter = Emitter(xs[i], ys[i], param[8], param[2], phaseIncrement*i, param[7])
                self.emitter_array.AddEmitter(emitter)
                print(f"Added emitter at ({xs[i]}, {ys[i]}) with frequency {param[2]} Hz and phase {phaseIncrement*i} rad")
            
    

    def array_factor(self, param, theta):
        d = 1 / param[7]  # Element spacing (normalized by wavelength)
        N = param[4]      # Number of elements
        phi = param[3]    # Phase shift in radians
        # Add rotation scaling based on number of elements
        scaling_factor = 1 / np.sqrt(N)  # Square root scaling provides a more balanced effect
        # Initialize complex array factor
        AF = np.zeros_like(theta, dtype=complex)
        # Calculate array center position
        array_center = (N-1)/2
        # Calculate array factor with progressive phase shift and scaled rotation
        for n in range(N):
            # Position of each element relative to array center
            element_pos = (n - array_center) * d
            # Scale the progressive phase based on number of elements
            scaled_phi = phi * scaling_factor
            # Progressive phase term with scaling
            progressive_phase = n * scaled_phi
            # Add contribution from each element
            AF += np.exp(1j * (2 * np.pi * element_pos * np.cos(theta) + progressive_phase))
        
        # Return magnitude of array factor
        return np.abs(AF)






    def calculate_interference_map(self, grid_size):
        if not self.emitter_array.emitters:
            print("No emitters to calculate interference map.")
            return np.zeros((grid_size, grid_size))

        wavelength = float(self.emitter_array.emitters[0].c)  / self.emitter_array.emitters[0].frequency 
        print(f"wavelength ({self.emitter_array.emitters[0].c} and frequency is ({self.emitter_array.emitters[0].frequency })")
        print(f" {wavelength} ")
        k = 2 * np.pi / wavelength

        x = np.linspace(-15, 15, grid_size)
        y = np.linspace(-15, 0, grid_size//2)
        X, Y = np.meshgrid(x, y)
        total_signal = np.zeros_like(X, dtype=np.complex128)

        for emitter in self.emitter_array.emitters:
            distance = np.sqrt((X - emitter.r[0]) ** 2 + (Y - emitter.r[1]) ** 2)
            total_signal += np.exp(1j * (k * distance + emitter.phi))

        print(f"signal {total_signal} ")
        return np.abs(total_signal)
    
    def plot_interference_map(self):

        if not self.emitter_array.emitters:
            print("No emitters to plot.")
            return

        frequency = self.emitter_array.emitters[0].frequency
        wavelength = 3e8 / frequency 

        grid_size = 800  
        interference_map = self.calculate_interference_map(grid_size)
        mirrored_map = np.flip(interference_map, axis=1)
        pixmap = self.np_to_pixmap(mirrored_map)
        pixmap = self.apply_circular_clip(pixmap)

        self.scene.clear()
        self.scene.addPixmap(pixmap)

        # Draw concentric circles
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = painter.pen()
        pen.setColor(Qt.gray)
        pen.setWidth(1)
        painter.setPen(pen)

        # # Draw circles with a distance of wavelength between them
        width, height = pixmap.width(), pixmap.height()
        center = QPointF(width/2 , height )

        max_radius = min(width, height) 
        radius = wavelength * grid_size / 30  

        # Add the color bar with the value range
        min_value, max_value = 0, interference_map.max()
        self.add_color_bar(min_value, max_value)


        while radius <= max_radius:
            painter.drawEllipse(center, radius, radius)
            radius += 10 * wavelength * grid_size / 30

        # Draw dividing lines and angle labels

        for angle in range(0, 181, 45):
            radian = np.radians(angle)

            # Set the pen for drawing lines
            pen.setColor(Qt.gray)
            pen.setWidth(1)
            painter.setPen(pen)

            # Calculate line endpoints
            end_x = center.x() + max_radius * np.cos(radian)
            end_y = center.y() - max_radius * np.sin(radian)
            painter.drawLine(center, QPointF(end_x, end_y))

            # Calculate label positions slightly inside the edge of the circle
            label_offset = 15  # Adjust this to bring the text slightly inward
            label_x = center.x() + (max_radius - label_offset) * np.cos(radian)
            label_y = center.y() - (max_radius - label_offset) * np.sin(radian)

            # Set font for the text
            font = painter.font()
            font.setPointSize(10)  
            painter.setFont(font)


        painter.end()
        self.scene.clear()
        self.scene.addPixmap(pixmap)


    def np_to_pixmap(self, np_array):
        """
        Convert a numpy array to a QPixmap using a colormap.
        """
        norm = Normalize(vmin=0, vmax=np_array.max())
        colormap = cm.get_cmap('viridis_r')

        # Apply the colormap to the normalized array
        colored_array = colormap(norm(np_array))

        # Convert to 8-bit RGB
        colored_array = (colored_array[:, :, :3] * 255).astype(np.uint8)

        # Convert to QImage
        height, width, _ = colored_array.shape
        q_image = QImage(colored_array.data, width, height, width * 3, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)
    
    def apply_circular_clip(self, pixmap):
        """
        Apply semicircular clipping to the pixmap.
        """
        # Create a mask for the semicircle
        width, height = pixmap.width(), pixmap.height()
        mask = QPixmap(width, height)
        mask.fill(Qt.transparent)

        # Use QPainter to draw a semicircle mask
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.setPen(Qt.black)
        painter.drawPie(0, 0, width, height * 2, 0, 180 * 16)  # Draw a semicircle
        painter.end()

        # Set the mask to the pixmap
        pixmap.setMask(mask.mask())
        return pixmap

    def plot_second_graph(self, param):
            # Second plot: Adjust for emitter geometry
            self.fig_2.clf() 

            if param[5] == "Linear":
                theta = np.linspace(0, 2 * np.pi, 2000)  
            else:  # Curved geometry
                theta = np.linspace(-np.pi * param[6], np.pi * param[6], 2000) 


            AF = self.array_factor(param, theta)

            # Normalize the array factor
            AF_normalized = 20 * np.log10(AF / np.max(AF))

            # Clear previous plot and create a new one
            ax2 = self.fig_2.add_subplot(111, polar=True)
        
            ax2.plot(theta, AF_normalized, label="Pattern superposition", color="orange")

            # Adjust radial limits for better visualization
            ax2.set_thetamin(-180)  
            ax2.set_thetamax(0)  
            ax2.set_ylim(-40, 0)

            # Rotate 0° to the right and maintain counterclockwise orientation
            ax2.set_theta_zero_location("E")  # 0° now at the right (East)
            ax2.set_theta_direction(-1)  # Counterclockwise direction

            # Highlight the active range for curved geometry
            if param[5] == "Curved":
                ax2.fill_between(theta, AF_normalized, -40, where=(AF_normalized > -40), alpha=0.3)

            self.fig_2.tight_layout()
            # Update canvas and ensure it expands
            self.canvas_2.draw()
            self.canvas_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.canvas_2.updateGeometry()

            ax2.legend(loc="upper center")
            self.canvas_2.draw()

    def add_color_bar(self, min_value, max_value):
        norm = Normalize(vmin=min_value, vmax=max_value)
        colormap = cm.get_cmap('viridis')

        # Create a vertical gradient for the color bar
        gradient_height = 200
        gradient_width = 20
        gradient = np.linspace(min_value, max_value, gradient_height).reshape(-1, 1)
        gradient = np.tile(gradient, (1, gradient_width))
        colored_array = colormap(norm(gradient))[:, :, :3] * 255
        colored_array = colored_array.astype(np.uint8)

        # Convert to QImage and QPixmap
        q_image = QImage(
            colored_array.data,
            gradient_width,
            gradient_height,
            gradient_width * 3,
            QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_image)

        color_bar_label = QLabel()
        color_bar_label.setPixmap(pixmap)

        min_label = QLabel(f"{min_value:.2f}")
        max_label = QLabel(f"{max_value:.2f}")
        min_label.setAlignment(Qt.AlignCenter)
        max_label.setAlignment(Qt.AlignCenter)

        bar_layout = QVBoxLayout()
        bar_layout.addWidget(max_label)
        bar_layout.addWidget(color_bar_label)
        bar_layout.addWidget(min_label)

        if not hasattr(self, 'map_layout'):
            self.map_layout = QHBoxLayout()  
            self.layout_map.addLayout(self.map_layout)

        while self.map_layout.count() > 1:  
            item = self.map_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        self.map_layout.addWidget(self.graphicsView)  
        self.map_layout.addLayout(bar_layout)  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = SecondWindow()
    mainWindow.show()
    sys.exit(app.exec_())