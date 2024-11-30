import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic
from Imag_Widget import ImageWidget
from PyQt5.QtWidgets import QWidget, QFileDialog
from FTViewPort import CompWidget
# Load the UI file
Ui_MainWindow, QtBaseClass = uic.loadUiType("mixed_images.ui")

# Main Window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # for i in range(1, 5): 
        #    getattr(self, f"ComboBox_FTComp_{i}").currentIndexChanged.connect(lambda : self.change_comp( f"ComboBox_FTComp_{i}",i))
         
        self.ComboBox_FTComp_1.currentIndexChanged.connect(lambda : self.change_comp(self.ComboBox_FTComp_1,1))  
        self.ComboBox_FTComp_2.currentIndexChanged.connect(lambda : self.change_comp(self.ComboBox_FTComp_2,2))  
        self.ComboBox_FTComp_3.currentIndexChanged.connect(lambda : self.change_comp(self.ComboBox_FTComp_3,3))  
        self.ComboBox_FTComp_4.currentIndexChanged.connect(lambda : self.change_comp(self.ComboBox_FTComp_4,4))


        self.widget_images = [self.Widget_Img_1, self.Widget_Img_2, self.Widget_Img_3, self.Widget_Img_4]
        self.widget_Ftcomp=[self.Widget_Comp_1 , self.Widget_Comp_2 , self.Widget_Comp_3 , self.Widget_Comp_4]
        # List to store the ImageWidget instances
        self.image_widgets = []
        self.comp_widget=[]

        # Loop through the widget names and create ImageWidget instances dynamically
        for i  in  range(len(self.widget_images)):            
            widget_comp=CompWidget(None ,self. widget_Ftcomp[i])
            widget_comp.setGeometry(self.widget_Ftcomp[i].geometry())
            widget_comp.setParent(self)
            self.comp_widget.append(widget_comp)

            image_widget = ImageWidget(None, self.widget_images[i] , widget_comp )
            image_widget.setGeometry(self.widget_images[i].geometry())
            image_widget.setParent(self)
            self.image_widgets.append(image_widget)

       
          
          
            
     
    def change_comp(self,current_comboBox,index):
        text=current_comboBox.currentText()
        current_data= [self.image_widgets[index-1],self.comp_widget[index-1]]
        current_data[1].display_component(current_data[0].ft_components_images[text])
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
