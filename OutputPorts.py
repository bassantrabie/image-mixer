from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath  # Import QPainterPath here
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PIL import Image, ImageQt, ImageEnhance
from numpy.fft import ifft2, ifftshift
import numpy as np
from scipy.fft import fft2, fftshift

from FTViewPort import CompWidget

import logging
logging.basicConfig(filemode="a", filename="our_log.log",
                    format="(%(asctime)s) | %(name)s| %(levelname)s | => %(message)s", level=logging.INFO)


class Output_Widget(QWidget):
    def __init__(self, parent=None ):
        super(Output_Widget, self).__init__(parent)
        # mag&phase   or real&Img
        self.Component_Mode=None
        self.fft_combined=None
        self.pixmap=None
        self.shape=(371, 311)

        # automatically run to paint the img
    def paintEvent(self, event):
        if self.__pixmap:
            painter = QPainter(self)
            # make img border raduis 
            rect = QRectF(self.rect())
            path = QPainterPath() 
            path.addRoundedRect(rect, 20, 20) 
            painter.setClipPath(path)
           
            # resize the img 
            scaled_pixmap = self.__pixmap.scaled(
                # set its geomerty from the main
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            
            painter.drawPixmap(self.rect(), scaled_pixmap)



    def inverse_fourier(self ):
        if self.fft_combined is not None:
            fft_combined = np.fft.ifftshift(self.fft_combined)
            reconstructed_img = ifft2(fft_combined)
            reconstructed_img = np.real(reconstructed_img)
            range_ = np.max(reconstructed_img) - np.min(reconstructed_img)

            if range_ == 0:
                # Avoid division by zero by setting normalized image to zeros or a constant value
                reconstructed_img_normalized = np.zeros_like(reconstructed_img, dtype=np.uint8)
            else:
                # Perform normalization as usual
                reconstructed_img_normalized = (255 * (reconstructed_img - np.min(reconstructed_img)) / range_).astype(np.uint8)

            reconstructed_img_normalized = np.clip(reconstructed_img_normalized, 0, 255).astype(np.uint8)       
            self.pixmap = self.convert_np_pixmap(reconstructed_img_normalized)
            logging.info("Calculated FFT inverse Correctly and update the output widget")
            self.update()



    def Calculate_Cropped_Data(self , current_Mode):
        created_Components=CompWidget.Get_All_created_widgets()
        if len(created_Components)>=0:
        
            if current_Mode=='Magandphase':
                self.fft_combined = np.zeros(self.shape, dtype=np.complex128)
                all_Magnitudes = np.zeros(self.shape, dtype=np.float64)
                all_phases = np.zeros(self.shape, dtype=np.complex128)
                
                for comp in created_Components:
                    if comp.get_Curr_Mode()=='FT Magnitude':
                        all_Magnitudes += (comp.get_slider_value()/100) *comp.get_crop_data_widget()             
                    if comp.get_Curr_Mode()=='FT Phase':
                        all_phases += (comp.get_slider_value()/100) *np.exp(1j * comp.get_crop_data_widget())
                    
                self.fft_combined= all_Magnitudes * np.exp(1j * np.angle(all_phases))

            else:    
                    
                self.fft_combined = np.zeros(self.shape, dtype=np.complex128)
                all_Real = np.zeros(self.shape, dtype=np.float64)
                all_Imag = np.zeros(self.shape, dtype=np.complex128)      

                for comp in created_Components:
                    if comp.get_Curr_Mode()=='FT Real':
                        all_Real += (comp.get_slider_value()/100) *comp.get_crop_data_widget()
                    if comp.get_Curr_Mode()=='FT Imaginary':
                        all_Imag += (comp.get_slider_value()/100) *comp.get_crop_data_widget()

                self.fft_combined= all_Magnitudes * np.exp(1j * np.angle(all_phases))
            
            self.inverse_fourier()


    # # this function take the data and combine it
    # def Set_Cropped_Data(self , all_data , component_Mode):

    #     try :
    #         # Initialize with complex data type since we're dealing with FFT
    #         self.fft_combined = np.zeros_like(all_data['0'][2], dtype=np.complex128)

    #         if component_Mode=='Magandphase':
    #             all_Magnitudes = np.zeros_like(all_data['0'][2], dtype=np.float64)
    #             all_phases = np.zeros_like(all_data['0'][2],  dtype=np.complex128)

    #             for _ , value in all_data.items():
    #                 if value[0]=='FT Magnitude':
    #                     all_Magnitudes += (value[1]/100) *value[2]
    #                 elif value[0]=='FT Phase':
    #                     all_phases+= (value[1]/100) *np.exp(1j * value[2])

    #             self.fft_combined= all_Magnitudes * np.exp(1j * np.angle(all_phases))

    #         elif component_Mode =='RealandImg':
    #             # take the shapee only hereee 
    #             all_Real=np.zeros_like(all_data['0'][2], dtype=np.float64)
    #             all_Img=np.zeros_like(all_data['0'][2], dtype=np.float64)
            
    #             for _ , value in all_data.items():
    #                 if value[0]=='FT Real':
    #                         all_Real += (value[1]/100) *value[2]
    #                 elif value[0]=='FT Imaginary':
    #                         all_Img+= (value[1]/100) *value[2]

    #             magnitude = np.sqrt(all_Real**2 + all_Img**2)  # Magnitude
    #             phase = np.arctan2(all_Img, all_Real) 
    #             self.fft_combined=  magnitude * np.exp(1j * phase)

    #         self.inverse_fourier( self.fft_combined)

    #     except Exception as e:
    #         logging.error(f"Error in Calculations of Combined Image : {e}")
    #         logging.info(f"the data is {all_data}")
  
    
    
    
    
    
    
    
    
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
            
    
