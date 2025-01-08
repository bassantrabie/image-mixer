from PyQt5 import QtWidgets, QtGui, QtCore, uic   # Added uic import
import sys
from PyQt5.QtGui import *
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtGui import QImage, QPixmap
import scenarios
from visualizer import Visualizer
from PIL import Image
# from regionSelector import ResizableRectangle


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task4.ui', self)

        # self.switch_button.clicked.connect(self.hide_image_frame_and_label)

        # self.return_button.clicked.connect(self.show_image_frame_and_label)
       

        


        ################# PART B #########################
        #  Find and initialize UI elements
        self.linear_radio_button = self.findChild(QtWidgets.QRadioButton, "linear_radio_button_3")
        self.frequency_slider = self.findChild(QtWidgets.QSlider, "beam_frequency_slider")
        self.phase_slider = self.findChild(QtWidgets.QSlider, "beam_phase_slider")
        self.curvature_slider = self.findChild(QtWidgets.QSlider, "beam_curvature_slider")
        self.no_transmitters_spinbox = self.findChild(QtWidgets.QSpinBox, "spinBox_No_transmitters_3")
        # self.frequency_lcd = self.findChild(QtWidgets.QLCDNumber, "frequency_lcd")
        # self.phase_lcd = self.findChild(QtWidgets.QLCDNumber, "phase_lcd")
        # self.curvature_lcd = self.findChild(QtWidgets.QLCDNumber, "curvature_lcd")
        self.curvature_angle_label = self.findChild(QtWidgets.QLabel, "curvature_angle_label")
        self.beam_position_slider = self.findChild(QtWidgets.QSlider, "beam_position_slider")
        # self.position_lcd = self.findChild(QtWidgets.QLCDNumber, "position_lcd")
        self.beam_position_y_slider = self.findChild(QtWidgets.QSlider, "position_y_slider")
        # self.position_y_lcd = self.findChild(QtWidgets.QLCDNumber, "position_y_lcd")
        self.curvature_unit_label = self.findChild(QtWidgets.QLabel, "label_12")
        self.spacing_slider = self.findChild(QtWidgets.QSlider, "spacing_slider")
        # self.spacing_lcd = self.findChild(QtWidgets.QLCDNumber, "spacing_lcd")


        self.beam_map_view = self.findChild(QtWidgets.QWidget, "beam_map")
        self.beam_plot_view = self.findChild(QtWidgets.QWidget, "beam_plot")
        self.scenario_combobox = self.findChild(QtWidgets.QComboBox, "comboBox_Open_scenario")

        # Initialize parameters
        self.num_transmitters = 2
        self.frequencies = [1000000000] * self.num_transmitters  # Default frequency for each transmitter
        self.phases = [0] * self.num_transmitters  # Default phase for each transmitter
        self.array_type = "curved"  # Default to curved
        self.curvature_angle = 30  # Default curvature angle
        self.element_spacing = 0.5  # Default element spacing
        self.array_position = [0, 0]  # Default position of the array

        # Set the initial state of radio button
        self.linear_radio_button.setChecked(False)
        # self.update_radio_button_text(self.linear_radio_button.isChecked())
        self.linear_radio_button.toggled.connect(self.update_radio_button_text)
        self.scenario_combobox.currentText() == "Open Scenario"
        self.update_scenario_parameters()

        # Connect UI elements to methods
        self.frequency_slider.setMinimum(1000000)
        self.frequency_slider.setMaximum(2000000000)
        self.frequency_slider.setSingleStep(10000000)  # Step size
        self.frequency_slider.valueChanged.connect(self.update_frequency)
        self.phase_slider.setMinimum(-180)
        self.phase_slider.setMaximum(180)
        self.phase_slider.setValue(0)
        self.phase_slider.valueChanged.connect(self.update_phase)
        self.curvature_slider.setMinimum(1)
        self.curvature_slider.setMaximum(180)
        self.curvature_slider.valueChanged.connect(self.update_curvature_angle)
        self.no_transmitters_spinbox.setMinimum(2)
        self.no_transmitters_spinbox.setMaximum(100)
        self.no_transmitters_spinbox.valueChanged.connect(self.update_transmitter_count)
        self.beam_position_slider.setMinimum(-10)
        self.beam_position_slider.setMaximum(10)
        self.beam_position_slider.setSingleStep(1)
        self.beam_position_slider.valueChanged.connect(self.update_array_Xposition)
        self.beam_position_y_slider.setMinimum(0)
        self.beam_position_y_slider.setMaximum(10)
        self.beam_position_y_slider.setSingleStep(1)
        self.beam_position_y_slider.valueChanged.connect(self.update_array_Yposition)

        self.spacing_slider.setMinimum(1)
        self.spacing_slider.setMaximum(200)
        self.spacing_slider.setSingleStep(1)
        self.spacing_slider.setValue(50)
        self.spacing_lcd.setText(str(50/100))
        
        
        self.spacing_slider.valueChanged.connect(self.update_spacing)

        self.scenario_combobox.currentIndexChanged.connect(self.update_scenario_parameters)
        # self.hide_image_frame_and_label()
        # self.frame_5.hide()
        # Initialize the plots
        self.beam_forming()

    
    def hide_image_frame_and_label(self):
        # Hides imageFrame, frame_3, and label; shows everything else
        self.imageFrame.hide()
        self.frame_3.hide()
        for widget in self.findChildren(QtWidgets.QWidget):
            if widget.objectName() not in ['imageFrame', 'frame_3']:
                widget.show()

    def show_image_frame_and_label(self):
        # Shows imageFrame, frame_3, and label; hides everything else
        self.frame_5.hide()
        self.imageFrame.show()
        self.frame_3.show()
    
    
    ############### PART B ###################

    def update_radio_button_text(self, checked):
        if checked:
            self.array_type = "linear"
            self.curvature_angle_previous = self.curvature_angle
            self.curvature_angle = 0
            self.linear_radio_button.setText("Linear")
            self.curvature_slider.hide()
            self.curvature_lcd.hide()
            self.curvature_angle_label.hide()
            self.curvature_unit_label.hide()
        else:
            self.array_type = "curved"
            self.curvature_angle = getattr(self, 'curvature_angle_previous', 30)
            self.linear_radio_button.setText("Curved")
            self.curvature_slider.show()
            self.curvature_lcd.show()
            self.curvature_angle_label.show()
            # self.curvature_unit_label.show()
        self.beam_forming()

    def update_transmitter_count(self, count):
        print(f"no transmitters updated: {count}")
        self.num_transmitters = count
        self.frequencies = [self.frequencies[0]] * count
        self.phases = [self.phases[0]] * count
        self.beam_forming()

    def update_frequency(self, value):
        print(f"Frequency updated: {value}")
        self.frequencies = [value] * self.num_transmitters
        self.frequency_lcd.setText(f"{value//1000000}")
        self.beam_forming()

    def update_phase(self, value):
        print(f"Phase updated: {value}")
        self.phases = [value] * self.num_transmitters
        self.phase_lcd.setText(str(value))
        self.beam_forming()

    def update_curvature_angle(self, value):
        print(f"curved angle updated: {value}")
        self.curvature_angle = value
        self.curvature_lcd.setText(str(value))
        self.beam_forming()

    def update_array_Xposition(self, value):
        print(f"Array position x updated: {value}")
        self.array_position[0] = [value]
        self.position_lcd.setText(str(value))
        self.beam_forming()

    def update_array_Yposition(self,value):
        print(f"Array position y updated: {value}")
        self.array_position[1] = [value]
        self.position_y_lcd.setText(str(value))
        self.beam_forming()

    def update_spacing(self, value):
        spacing = value / 100.0
        self.element_spacing = spacing
        print(f"Element spacing updated: {spacing:.2f}")
        # self.spacing_lcd.setDigitCount(4)  # Ensure enough space for decimal display
        self.spacing_lcd.setText(str(spacing))  # Show decimal value
        self.beam_forming()

    def beam_forming(self):
        visualizer = Visualizer()
        visualizer.set_frequencies(self.frequencies)
        visualizer.set_phases(self.phases)
        visualizer.set_array_type(self.array_type, self.curvature_angle)
        visualizer.set_position_offset(self.array_position[0], self.array_position[1])
        visualizer.set_element_spacing(self.element_spacing)
        
        # Generate and display the plots
        field_map_fig = visualizer.plot_field_map(
            num_transmitters=self.num_transmitters,
            element_spacing=self.element_spacing,
            frequency=self.frequencies[0],
            phases=self.phases,
            curvature_angle=self.curvature_angle,
        )

        beam_pattern_fig = visualizer.plot_beam_pattern_polar(
            num_transmitters=self.num_transmitters,
            element_spacing=self.element_spacing,
            frequency=self.frequencies[0],
            phases=self.phases,
            curvature_angle=self.curvature_angle,
        )
        
        self.display_plot(self.beam_map_view, field_map_fig)
        self.display_plot(self.beam_plot_view, beam_pattern_fig) 

    def display_plot(self, widget, figure):
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from PyQt5.QtWidgets import QVBoxLayout

        if widget.layout() is None:
            widget.setLayout(QVBoxLayout())

        layout = widget.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)
        layout.setAlignment(QtCore.Qt.AlignCenter)

    def update_scenario_parameters(self):
        scenario = self.scenario_combobox.currentText()
        parameters = scenarios.ScenarioParameters()
        if scenario == "5G":
            parameters.update_parameters("5G")
            parameters.display_parameters()
        elif scenario == "Tumor Ablation":
            parameters.update_parameters("Tumor Ablation")
            parameters.display_parameters()
        elif scenario == "Ultrasound":
            parameters.update_parameters("Ultrasound")
            parameters.display_parameters()
        else:
            parameters.update_parameters("Custom")
            parameters.display_parameters()
        
        self.array_type = parameters.array_geometry
        if self.array_type == "linear":
            self.linear_radio_button.setChecked(True)
        else:
            self.linear_radio_button.setChecked(False)  
        self.update_radio_button_text(self.linear_radio_button.isChecked())
        self.frequency_slider.setValue(parameters.frequency)
        self.frequency_lcd.setText(str(parameters.frequency//1000000))
        self.phase_slider.setValue(parameters.phase)
        self.phase_lcd.setText(str(parameters.phase))
        self.curvature_slider.setValue(parameters.curvature_angle)
        self.curvature_lcd.setText(str(parameters.curvature_angle))
        self.no_transmitters_spinbox.setValue(parameters.num_transmitters)
        self.spacing_slider.setValue(int(parameters.position_between_transmitters * 10))
        self.spacing_lcd.setText(str(parameters.position_between_transmitters /10))
        self.beam_position_slider.setValue(0)
        self.position_lcd.setText(str(0))
        self.beam_position_y_slider.setValue(0)
        self.position_y_lcd.setText(str(0))
        
       

        print(f"Scenario updated: {scenario}")
        print(f"self.frequencies updated: {self.frequencies}")
        print(f"self.phases updated: {self.phases}")
        print(f"self.array_type updated: {self.array_type}")
        print(f"self.curvature_angle updated: {self.curvature_angle}")

        self.beam_forming()

# Entry point of the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())