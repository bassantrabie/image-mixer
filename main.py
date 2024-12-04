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

from OutputPorts import Output_Widget

# Load the UI file
Ui_MainWindow, QtBaseClass = uic.loadUiType("mixed_images.ui")

# Main Window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        

        button_group = QButtonGroup(self)
        button_group.addButton(self.RadioButton_Inside)
        button_group.addButton(self.RadioButton_Outside)
        self.RadioButton_Inside.setChecked(True)

        button_group = QButtonGroup(self)
        button_group.addButton(self.RadioButton_Magandphase)
        button_group.addButton(self.RadioButton_RealandImg)


        self.PushButton_Mix.clicked.connect(self.display_output)
        self.RadioButton_Magandphase.clicked.connect(lambda: self.Select_mode('Magandphase'))
        self.RadioButton_RealandImg.clicked.connect (lambda: self.Select_mode('RealandImg'))


        # for i in range(1, 5): 
        #    getattr(self, f"ComboBox_FTComp_{i}").currentIndexChanged.connect(lambda : self.change_comp( f"ComboBox_FTComp_{i}",i))
         
        self.ComboBox_FTComp_1.currentIndexChanged.connect(lambda : self.change_comp(self.ComboBox_FTComp_1,1))  
        self.ComboBox_FTComp_2.currentIndexChanged.connect(lambda : self.change_comp(self.ComboBox_FTComp_2,2))  
        self.ComboBox_FTComp_3.currentIndexChanged.connect(lambda : self.change_comp(self.ComboBox_FTComp_3,3))  
        self.ComboBox_FTComp_4.currentIndexChanged.connect(lambda : self.change_comp(self.ComboBox_FTComp_4,4))


        self.widget_images = [self.Widget_Img_1, self.Widget_Img_2, self.Widget_Img_3, self.Widget_Img_4]
        self.widget_Ftcomp = [self.Widget_Comp_1 , self.Widget_Comp_2 , self.Widget_Comp_3 , self.Widget_Comp_4]
        # List to store the ImageWidget instances
        self.image_widgets = []
        self.comp_widget=[]

        # Loop through the widget names and create ImageWidget instances dynamically
        for i  in  range(len(self.widget_images)):            
            widget_comp=CompWidget(None ,self. widget_Ftcomp[i] , {'combox':getattr(self, f"ComboBox_FTComp_{i+1}")
                                                                   , 'slider':getattr(self, f"horizontalSlider_{i+1}")})
            widget_comp.setGeometry(self.widget_Ftcomp[i].geometry())
            widget_comp.setParent(self)
            self.comp_widget.append(widget_comp)

            image_widget = ImageWidget(None, self.widget_images[i] , widget_comp )
            image_widget.setGeometry(self.widget_images[i].geometry())
            image_widget.setParent(self)
            self.image_widgets.append(image_widget)

       
        # createee output widgetttts
          
        self.output_widget_1=Output_Widget(self.Output_1 )
        self.output_widget_1.setGeometry(self.Output_1.geometry())
        self.output_widget_1.setParent(self)


        self.output_widget_2=Output_Widget(self.Output_2 )
        self.output_widget_2.setGeometry(self.Output_2.geometry())
        self.output_widget_2.setParent(self)
        # set default is output_1
        self.RadioButton_Select_out1.setChecked(True)


        # intializee mode with the Magnitude 
        self.Select_mode('Magandphase')
     
    def change_comp(self,current_comboBox,index):
        text=current_comboBox.currentText()
        curr_choice=current_comboBox.currentIndex()
        # print(f"text is now :{text}and curr index :{curr_choice} " )
        if curr_choice>=0:
            # print("in")
            current_data= [self.image_widgets[index-1],self.comp_widget[index-1]]
            if current_data[0].ft_components :
                current_data[1].display_component(current_data[0].ft_components[text] , curr_choice)
        
    



    def display_output(self):
        mode='InsideRegion'  if self.RadioButton_Inside.isChecked() else 'OutsideRegion'
        CompWidget.extract_data_inside_rectangle(mode)


        all_data=CompWidget.Get_CroppedData()
        Mode = 'Magandphase' if self.RadioButton_Magandphase.isChecked() else 'RealandImg'
        output=self.output_widget_1  if  self.RadioButton_Select_out1.isChecked() else self.output_widget_2
        output.Set_Cropped_Data(all_data,Mode)







    def Select_mode(self,mode):
        
        if mode=='Magandphase':
            for i in range(1,5):
                combox=getattr(self, f"ComboBox_FTComp_{i}")
                for i in range(4):
                    combox.removeItem(0)
                combox.addItem('FT Magnitude')
                combox.addItem('FT Phase')
                self.change_comp(combox ,i)
        else :
            for i in range(1,5):
                combox=getattr(self, f"ComboBox_FTComp_{i}")
                for num in range(4):
                    combox.removeItem(0)
                combox.addItem('FT Real')
                combox.addItem('FT Imaginary')
                self.change_comp(combox ,i)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
