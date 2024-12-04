from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath  # Import QPainterPath here
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PIL import Image, ImageQt, ImageEnhance
from numpy.fft import ifft2, ifftshift
import numpy as np
from scipy.fft import fft2, fftshift
class ImageWidget(QWidget):
    def __init__(self, image_path=None, parent=None , comp_widget=None ):
        super(ImageWidget, self).__init__(parent)
        
        self.pixmap = None  
        self.image=None
        self.resized_img=None
        self.ft_components={}
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
        # img = QImage(image_path)
        # grayscale_image = img.convertToFormat(QImage.Format_Grayscale8)  
        # self.pixmap = QPixmap.fromImage(grayscale_image)
       

        
        # read image for processing and convert to grayscale
        self.image = Image.open(image_path).convert('L')
        # sure the resized_img is the size of widget 
        self.resized_img = self.image.resize((self.width(), self.height()))
        np_arr=np.array(self.resized_img )
        self.pixmap=self.convert_np_pixmap(np_arr)
       
        # repaint
        self.update() 
       
        # calculate the fft components 
        self.calculate_ft_components()
        combox=self.comp_widget.get_combox()
        # print(combox.currentText())
        #initalize drawing for the magnitude  
        self.comp_widget.display_component(self.ft_components[combox.currentText()] , 0)


    
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
        phase = np.angle(fft_shifted).astype(np.uint8)
        real = 15 * np.log(np.abs(np.real(fft_shifted)) +1e-10).astype(np.uint8)
        imaginary = fft_shifted.imag.astype(np.uint8)


    
        # Store the numerical components
        self.ft_components['FT Magnitude'] ={'org': np.abs(fft_shifted)  , 'np_img':mag_log}
        self.ft_components['FT Phase']     ={'org':np.angle(fft_shifted) , 'np_img':phase}
        self.ft_components['FT Real']      ={'org':np.real(fft_shifted)  , 'np_img':real}
        self.ft_components['FT Imaginary'] ={'org': np.imag(fft_shifted) , 'np_img':imaginary}


    # def inverse_fourier(self, data=None):
    #     fft_combined = self.ft_components['FT Real'] + 1j * self.ft_components['FT Imaginary']

    #     # Perform the inverse FFT
    #     ifft_shifted = ifftshift(fft_combined)
    #     reconstructed_img = ifft2(ifft_shifted)

    #     # Take the real part of the inverse FFT result
    #     reconstructed_img = np.real(reconstructed_img)

    #     # Normalize the image to 0-255 and convert to uint8
    #     reconstructed_img_normalized = (255 * (reconstructed_img - np.min(reconstructed_img)) / 
    #                                     (np.max(reconstructed_img) - np.min(reconstructed_img))).astype(np.uint8)

    #     # Convert the numpy array to a PIL image
    #     pil_image = Image.fromarray(reconstructed_img_normalized, mode='L')

    #     # Convert the PIL image to QImage for use in the GUI
    #     qim = QImage(
    #         pil_image.tobytes(),
    #         pil_image.width,
    #         pil_image.height,
    #         pil_image.width,
    #         QImage.Format_Grayscale8,
    #     )

    #     # Convert QImage to QPixmap and store it for display
    #     self.pixmap = QPixmap.fromImage(qim)

    #     # Update the GUI widget to display the reconstructed image
    #     self.update()
   
    def inverse_fourier(self, data):

        # imag = data[1] 
        # fft_combined = data[0] + 1j * imag
        fft_combined = data[0] * np.exp(1j * data[1])

        fft_combined = np.fft.ifftshift(fft_combined)
        reconstructed_img = ifft2(fft_combined)

        reconstructed_img = np.real(reconstructed_img)

        reconstructed_img_normalized = (255 * (reconstructed_img - np.min(reconstructed_img)) / 
                                        (np.max(reconstructed_img) - np.min(reconstructed_img))).astype(np.uint8)
        reconstructed_img_normalized = np.clip(reconstructed_img_normalized, 0, 255).astype(np.uint8)       
        self.pixmap = self.convert_np_pixmap(reconstructed_img_normalized)
        self.update()
    

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