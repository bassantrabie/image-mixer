from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath  # Import QPainterPath here
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PIL import Image, ImageQt, ImageEnhance

import numpy as np
from scipy.fft import fft2, fftshift
class ImageWidget(QWidget):
    def __init__(self, image_path=None, parent=None , comp_widget=None ):
        super(ImageWidget, self).__init__(parent)
        self.pixmap = None  
        self.image=None
        self.resized_img=None
        self.ft_components={}
        self.ft_components_images={}
        self.comp_widget=comp_widget
        
        if image_path:
            self.load_image(image_path)
    
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

    
    def load_image(self, image_path):
        img = QImage(image_path)
        grayscale_image = img.convertToFormat(QImage.Format_Grayscale8)  
        self.pixmap = QPixmap.fromImage(grayscale_image)
       
        # repaint
        self.update() 
        
        # read image for processing and convert to grayscale
        self.image = Image.open(image_path).convert('L')
        # sure the resized_img is the size of widget 
        self.resized_img = self.image.resize((self.width(), self.height()))
        # calculate the fft components 
        self.calculate_ft_components()
        
        #initalize drawing for the magnitude  
        self.comp_widget.display_component(self.ft_components_images['FT Magnitude'])


    
    def mouseDoubleClickEvent(self, event):
        """This method is automatically called on double-click."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg *.gif);;All Files (*)")
        if file_path:
            self.load_image(file_path) 
    



    
    def calculate_ft_components(self):
        fft = fft2(self.resized_img)

        # Shift the zero-frequency component to the center
        fft_shifted = fftshift(fft)

        # Compute the magnitude of the spectrum
        mag = np.abs(fft_shifted)
        mag_log = 15 * np.log(mag + 1e-10).astype(np.uint8)

        # Compute the phase of the spectrum
        phase = np.angle(fft_shifted).astype(np.uint8)

        # Compute the real and imaginary components
        real = 15 * np.log(np.abs(np.real(fft_shifted)) + 1e-10).astype(np.uint8)
       
        imaginary = fft_shifted.imag.astype(np.uint8)


        # Store the results as images
        self.ft_components_images['FT Magnitude'] = Image.fromarray(mag_log, mode="L")
        self.ft_components_images['FT Phase'] = Image.fromarray(phase, mode='L')
        self.ft_components_images["FT Real"] = Image.fromarray(real, mode='L')
        self.ft_components_images["FT Imaginary"] = Image.fromarray(imaginary, mode='L')

        # Store the numerical components
        self.ft_components['FT Magnitude'] = np.abs(fft_shifted)
        self.ft_components['FT Phase'] = np.angle(fft_shifted)
        self.ft_components['FT Real'] = fft_shifted.real
        self.ft_components['FT Imaginary'] = fft_shifted.imag

        

