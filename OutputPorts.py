from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath  # Import QPainterPath here
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PIL import Image, ImageQt, ImageEnhance
from numpy.fft import ifft2, ifftshift
import numpy as np
from scipy.fft import fft2, fftshift
class Output_Widget(QWidget):
    def __init__(self, parent=None ):
        super(Output_Widget, self).__init__(parent)
        # mag&phase   or real&Img
        self.Component_Mode=None
        self.fft_combined=None

        self.pixmap=None

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



    def inverse_fourier(self , fft_combined):

        # imag = data[1] 
        # fft_combined = data[0] + 1j * imag
        # fft_combined = data[0] * np.exp(1j * data[1])

        fft_combined = np.fft.ifftshift(fft_combined)
        reconstructed_img = ifft2(fft_combined)

        reconstructed_img = np.real(reconstructed_img)

        reconstructed_img_normalized = (255 * (reconstructed_img - np.min(reconstructed_img)) / 
                                        (np.max(reconstructed_img) - np.min(reconstructed_img))).astype(np.uint8)
        reconstructed_img_normalized = np.clip(reconstructed_img_normalized, 0, 255).astype(np.uint8)       
        self.pixmap = self.convert_np_pixmap(reconstructed_img_normalized)
        self.update()

    # this function take the data and combine it
    def Set_Cropped_Data(self , all_data , component_Mode):

        self.fft_combined=np.zeros_like(all_data['0'][2].shape ,  dtype=np.float64)
        # print(all_data)

        
        if component_Mode=='Magandphase':
            all_Magnitudes = np.zeros_like(all_data['0'][2], dtype=np.float64)
            all_phases = np.zeros_like(all_data['0'][2], dtype=np.float64)

            for _ , value in all_data.items():
                if value[0]=='FT Magnitude':
                    all_Magnitudes += (value[1]/100) *value[2]
                elif value[0]=='FT Phase':
                    all_phases+= (value[1]/100) *value[2]

            self.fft_combined= all_Magnitudes * np.exp(1j * all_phases)

        elif component_Mode =='RealandImg':
            # take the shapee only hereee 
            all_Real=np.zeros_like(all_data['0'][2], dtype=np.float64)
            all_Img=np.zeros_like(all_data['0'][2], dtype=np.float64)
           
            for _ , value in all_data.items():
                if value[0]=='FT Real':
                        all_Real += (value[1]/100) *value[2]
                elif value[0]=='FT Imaginary':
                        all_Img+= (value[1]/100) *value[2]

            magnitude = np.sqrt(all_Real**2 + all_Img**2)  # Magnitude
            phase = np.arctan2(all_Img, all_Real) 
            self.fft_combined=  magnitude * np.exp(1j * phase)

        self.inverse_fourier( self.fft_combined)
  
    
    
    
    
    
    
    
    
    def convert_np_pixmap(self, np_arr):
        # Ensure the numpy array is in the correct format (grayscale)
        if len(np_arr.shape) == 2:  # Single channel grayscale image
            height, width = np_arr.shape
        else:
            raise ValueError("Input NumPy array must be a 2D grayscale image.")
        
        # Convert the NumPy array to bytes
        byte_data = np_arr.tobytes()
        
        # Create QImage from the byte data (using width, height, bytesPerLine, and format)
        qimage = QImage(byte_data, width, height, width, QImage.Format_Grayscale8)
        
        # Convert QImage to QPixmap for displaying in PyQt
        pixmap = QPixmap.fromImage(qimage)
        return pixmap
    
    def convert_pixmap_np(self, pixmap):
        # Convert QPixmap to QImage
        image = pixmap.toImage()
        
        # Ensure the QImage is in the correct format for manipulation
        image = image.convertToFormat(QImage.Format_Grayscale8)  # Convert to grayscale format
        
        # Access raw pixel data from the QImage
        width = image.width()
        height = image.height()
        
        # Create a NumPy array from the QImage pixel data
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        
        # Convert the byte data into a NumPy array with the appropriate shape (height, width) for grayscale
        np_array = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width))
        
        return np_array
            
    
