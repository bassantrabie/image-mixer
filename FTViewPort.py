from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath  # Import QPainterPath here
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PIL import Image, ImageQt, ImageEnhance

import numpy as np
from scipy.fft import fft2, fftshift
class CompWidget(QWidget):
    def __init__(self, comp=None, parent=None):
        super(CompWidget, self).__init__(parent)
        self.pixmap=comp        

    
    # automatically run to paint the img
    def paintEvent(self, event):
        if self.pixmap:
            painter = QPainter(self)
            # make img border raduis 
            rect = QRectF(self.rect())
            path = QPainterPath() 
            path.addRoundedRect(rect, 20, 20) 
            painter.setClipPath(path)
           
            # resize the img 
            scaled_pixmap = self.pixmap.scaled(
                # set its geomerty from the main
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            
            painter.drawPixmap(self.rect(), scaled_pixmap)
   
    def display_component(self,comp ):
        qt_image = ImageQt.ImageQt(comp)
        self.pixmap = QPixmap.fromImage(qt_image)
        self.update()
    
    
