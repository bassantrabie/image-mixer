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
         
        widget_images = [self.Widget_Img_1, self.Widget_Img_2, self.Widget_Img_3, self.Widget_Img_4]
        # widget_Ftcomp=[self.Widget_Comp_1 , self.Widget_Comp_2 , self.Widget_Comp_3 , self.Widget_Comp_4]
        # List to store the ImageWidget instances
        self.image_widgets = []

        # Loop through the widget names and create ImageWidget instances dynamically
        for i  in  range(len(widget_images)):            
            # widget_comp=CompWidget(None , widget_Ftcomp[i])
            image_widget = ImageWidget(None, widget_images[i] )
            image_widget.setGeometry(widget_images[i].geometry())
            image_widget.setParent(self)
            self.image_widgets.append(image_widget)


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
