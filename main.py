import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QRadioButton, QButtonGroup
from PyQt5 import uic 
from Imag_Widget import ImageWidget
from PyQt5.QtWidgets import QWidget, QFileDialog
from FTViewPort import CompWidget
from PIL import Image, ImageQt, ImageEnhance
from numpy.fft import ifft2, ifftshift
import numpy as np
from scipy.fft import fft2, fftshift
import logging
from OutputPorts import Output_Widget
from PyQt5.QtWidgets import QMainWindow, QTabWidget


from second_window_finalll import *
# Configure logging to capture all log levels
logging.basicConfig(filemode="a", filename="our_log.log",
                    format="(%(asctime)s) | %(name)s| %(levelname)s | => %(message)s", level=logging.INFO)


# Load the UI file
Ui_MainWindow, QtBaseClass = uic.loadUiType("OLD.ui")

# Main Window
class MainWindow(QMainWindow , Ui_MainWindow ):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        # make groups for  radio buttons (inside , outside) 
        button_group = QButtonGroup(self)
        button_group.addButton(self.RadioButton_Inside)
        button_group.addButton(self.RadioButton_Outside)
        self.RadioButton_Inside.setChecked(True)
         # make groups for  radio buttons (Mag&phase , real&img) 
        button_group = QButtonGroup(self)
        button_group.addButton(self.RadioButton_Magandphase)
        button_group.addButton(self.RadioButton_RealandImg)


        # connect the second window to its button
        # self.PushButton_BeamFormaing.clicked.connect(self.show_Second_Window)


        # Connect radio buttons
        radio_connections = {
            'RadioButton_Magandphase': lambda: self.Select_mode('Magandphase'),
            'RadioButton_RealandImg': lambda: self.Select_mode('RealandImg'),
            # make any change replot the output
            'RadioButton_Inside': self.display_output,
            'RadioButton_Outside': self.display_output,
            'RadioButton_Select_out1': self.display_output,
            'RadioButton_Select_out2': self.display_output
        }

        for button_name, handler in radio_connections.items():
            getattr(self, button_name).clicked.connect(handler)
        
        



        for i in range(1, 5): 
            slider=getattr(self, f"horizontalSlider_{i}")
            # connect  any change of sliders replot the output
            slider.valueChanged.connect(self.display_output)
            combo = getattr(self, f"ComboBox_FTComp_{i}")
            combo.currentIndexChanged.connect(lambda checked, i=i: self.change_comp(getattr(self, f"ComboBox_FTComp_{i}"), i))

        
        # to make objects form the image_widget need to path the widget in the ui
        self.widget_images = [self.Widget_Img_1, self.Widget_Img_2, self.Widget_Img_3, self.Widget_Img_4]
        self.widget_Ftcomp = [self.Widget_Comp_1 , self.Widget_Comp_2 , self.Widget_Comp_3 , self.Widget_Comp_4]
        self.image_widgets = []
        self.comp_widget=[]

        # Loop through the widget names and create ImageWidget and the component_widgets 
        for i  in  range(len(self.widget_images)):            
            widget_comp=CompWidget(None ,self. widget_Ftcomp[i] , {'combox':getattr(self, f"ComboBox_FTComp_{i+1}")
                                                                   , 'slider':getattr(self, f"horizontalSlider_{i+1}")},self.display_output)
            widget_comp.setGeometry(self.widget_Ftcomp[i].geometry())
            widget_comp.setParent(self)
            self.comp_widget.append(widget_comp)

            image_widget = ImageWidget(None, self.widget_images[i] , widget_comp )
            image_widget.setGeometry(self.widget_images[i].geometry())
            image_widget.setParent(self)
            self.image_widgets.append(image_widget)

       
        # createee output widgetttts
        for i in range(1, 3):  # Adjust range as needed for more widgets
            output_attr = getattr(self, f"Output_{i}")
            widget = Output_Widget(output_attr)
            widget.setGeometry(output_attr.geometry())
            widget.setParent(self)
            setattr(self, f"output_widget_{i}", widget)


        # set default is output_1
        self.RadioButton_Select_out1.setChecked(True)
        # intializee mode with the Magnitude 
        self.Select_mode('Magandphase')
     

    
    def change_comp(self,current_comboBox,index):
        '''
        inputs :  current_comboBox as object , index of the its related image widget(one_index)
        '''
        text=current_comboBox.currentText()
        curr_choice=current_comboBox.currentIndex()

        if curr_choice>=0:
            # set in this the related image_widget , related Component Widget
            current_data= [self.image_widgets[index-1],self.comp_widget[index-1]]
            if current_data[0].is_uploaded_img() :
                # call the omponent_widget function to redisplay the component
                current_data[1].set_component(current_data[0].get_fft_components()[text] , text)

        # update the output when change the choose from the compobox
        self.display_output()
        
        
    



    def display_output(self ):
        mode='InsideRegion'  if self.RadioButton_Inside.isChecked() else 'OutsideRegion'
        CompWidget.extract_data_inside_rectangle(mode)    
        # all_data=CompWidget.Get_CroppedData()
        Mode = 'Magandphase' if self.RadioButton_Magandphase.isChecked() else 'RealandImg'
        output=self.output_widget_1  if  self.RadioButton_Select_out1.isChecked() else self.output_widget_2
        
        # trace logging
        output_name=f"output_widget_1"  if  self.RadioButton_Select_out1.isChecked() else f"output_widget_2" 
        logging.info(f"The Selected Mode is {mode} and selected widget is {output_name}")
     
        
    #    set the new cropped_data to the output widget
        output.Calculate_Cropped_Data(Mode)



    def Select_mode(self,mode):              
        # the radiobutton change in combobox and also redisplay the new selected mode
        if mode=='Magandphase':
            logging.info("The Selected Mode is Magnitude and Phase")
            for i in range(1,5):
                combox=getattr(self, f"ComboBox_FTComp_{i}")
                for _ in range(4):
                    combox.removeItem(0)
                combox.addItem('FT Magnitude')
                combox.addItem('FT Phase')
                self.change_comp(combox ,i)
        else :
            logging.info("The Selected Mode is Real and Imaginary")
            for i in range(1,5):
                combox=getattr(self, f"ComboBox_FTComp_{i}")
                for _ in range(4):
                    combox.removeItem(0)
                combox.addItem('FT Real')
                combox.addItem('FT Imaginary')
                self.change_comp(combox ,i)
        self.display_output()




    # def show_Second_Window(self):
    #         self.second_window = SecondWindow()
    #         self.second_window.show() 
    #         self.close()
            

if __name__ == "__main__":
    logging.info(
        "----------------------the user open the app-------------------------------------")
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
