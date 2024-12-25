from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath  # Import QPainterPath here
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QWidget, QFileDialog
from PIL import Image, ImageQt, ImageEnhance
from numpy.fft import ifft2, ifftshift
import numpy as np
from scipy.fft import fft2, fftshift
import logging
import copy
logging.basicConfig(filemode="a", filename="our_log.log",
                    format="(%(asctime)s) | %(name)s| %(levelname)s | => %(message)s", level=logging.INFO)

class ImageWidget(QWidget):
    def __init__(self, image_path=None, parent=None , comp_widget=None ):
        super(ImageWidget, self).__init__(parent)
        self.__pixmap = None  
        self.__image=None
        self.__resized_img=None
        self.__ft_components={}

        self.__comp_widget=comp_widget

        self.__pressed_mouse=False
        self.__changes_image=None
        self.__pressed_pos_x=0
        self.__pressed_pos_y=0
        self.__Move_pos_x=0
        self.__Move_pos_y=0
        self.__brightness = 0
        self.__contrast = 0



        self.setMouseTracking(True)

        if image_path:
            self.load_image(image_path)
    
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

    
    def load_image(self, image_path):
        try:
            logging.info("Image uploaded successfully.")
            # read image for processing and convert to grayscale
            self.__image = Image.open(image_path).convert('L')
            # sure the resized_img is the size of widget 
            self.__resized_img = self.__image.resize((self.width(), self.height()))
            np_arr=np.array(self.__resized_img )
            
            self.__changes_image=copy.deepcopy(np_arr)
            
            self.__pixmap=self.convert_np_pixmap(np_arr)
            slider=self.__comp_widget.get_slider()
            slider.setValue(100)
            # repaint
            self.update() 
        
            # calculate the fft components 
            self.calculate_ft_components()
            combox=self.__comp_widget.get_combox()
            #initalize drawing for the magnitude  
            self.__comp_widget.set_component(self.__ft_components[combox.currentText()] , combox.currentText())
            
            function_update_ouput=self.__comp_widget.get_output_display_funciton()
            function_update_ouput()
        
        except Exception as e:
            logging.warning(f"Error opening image: {e}")
        


    
    def mouseDoubleClickEvent(self, event):
        """This method is automatically called on double-click."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg *.gif);;All Files (*)")
        if file_path:
            self.load_image(file_path) 

        else:
            logging.info(f"Didn't choose an Image")


    



    
    def calculate_ft_components(self):
        fft = fft2(self.__resized_img)

        # Shift the zero-frequency component to the center
        fft_shifted = fftshift(fft)

        # Compute the magnitude of the spectrum
        mag = np.abs(fft_shifted)
        mag_log = 15 * np.log(mag + 1e-10).astype(np.uint8)
        phase = np.angle(fft_shifted).astype(np.uint8)
        real = 15 * np.log(np.abs(np.real(fft_shifted)) +1e-10).astype(np.uint8)
        imaginary = fft_shifted.imag.astype(np.uint8)


    
        # Store the numerical components
        self.__ft_components['FT Magnitude'] ={'org': np.abs(fft_shifted)  , 'np_img':mag_log}
        self.__ft_components['FT Phase']     ={'org':np.angle(fft_shifted) , 'np_img':phase}
        self.__ft_components['FT Real']      ={'org':np.real(fft_shifted)  , 'np_img':real}
        self.__ft_components['FT Imaginary'] ={'org': np.imag(fft_shifted) , 'np_img':imaginary}

        logging.info("Calculated FFT to uploaded Image")



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

    def mousePressEvent(self, event):
            """
            Save the initial mouse position when the mouse is pressed.

            Parameters:
                event (QMouseEvent): The mouse event object.
            """
            self.__pressed_pos_x = event.x()
            self.__pressed_pos_y = event.y()
            # print(f"Mouse pressed at ({self.pressed_pos_x}, {self.pressed_pos_y})")
            self.__pressed_mouse = True

    def mouseMoveEvent(self, event):
        if self.__pressed_mouse and self.__pixmap is not None:
            # Calculate mouse movement deltas
            delta_x = event.x() - self.__pressed_pos_x
            delta_y = event.y() - self.__pressed_pos_y

            # Image dimensions for normalization
            image_width = self.__changes_image.shape[1]
            image_height = self.__changes_image.shape[0]

            # Normalize deltas and scale
            normalized_dx = delta_x / image_width
            normalized_dy = delta_y / image_height

            # Adjust brightness and contrast with range limits
            new_brightness = self.__brightness + normalized_dx * 100
            new_contrast = self.__contrast + normalized_dy * 40

            # Strictly clamp values to -100 and 100
            self.__brightness = max(-90, min(90, new_brightness))
            self.__contrast = max(-90, min(90, new_contrast))
            # Apply brightness and contrast to the image
            changed_image = self.apply_brightness_contrast(self.__changes_image, self.__brightness, self.__contrast)
            # Update pixmap and redraw
            self.__pixmap = self.convert_np_pixmap(changed_image)
            self.update()

            # Update last mouse position
            self.__pressed_pos_x = event.x()
            self.__pressed_pos_y = event.y()

            # print(f"Updated Brightness: {self.brightness}, Contrast: {self.contrast}")

    def apply_brightness_contrast(self, image, brightness=0, contrast=0):
        # Strictly clamp brightness and contrast to -100 and 100
        brightness = max(-100, min(100, brightness))
        contrast = max(-100, min(100, contrast))

        brightness_factor = (brightness + 255) / 255.0
        brightness_enhancer = ImageEnhance.Brightness(
            self.__image.resize(self.__resized_img.size))
        img_with_brightness_adjusted = brightness_enhancer.enhance(
            brightness_factor)

        # Adjust contrast
        contrast_factor = (self.__contrast + 127) / 127.0
        contrast_enhancer = ImageEnhance.Contrast(img_with_brightness_adjusted)
        self.__resized_img = contrast_enhancer.enhance(contrast_factor)


        # calculate the fft components 
        self.calculate_ft_components()
        combox=self.__comp_widget.get_combox()
        #initalize drawing for the magnitude  
        self.__comp_widget.set_component(self.__ft_components[combox.currentText()] , combox.currentText())
        
        function_update_ouput=self.__comp_widget.get_output_display_funciton()
        function_update_ouput()

        # Convert to float for calculations
        image = image.astype(np.float32)

        # Brightness adjustment
        if brightness != 0:
            image += brightness

        # Contrast adjustment
        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            image = f * (image - 127) + 127

        # Clip values to the valid range [0, 255]
        image = np.clip(image, 0, 255)

        # Convert back to uint8 for display
        return image.astype(np.uint8)

            
    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to finalize changes.

        Parameters:
            event (QMouseEvent): The mouse event object.
        """
        if self.__pressed_mouse:
            # print(f"Final Brightness: {self.brightness}, Final Contrast: {self.contrast}")
            self.__pressed_mouse = False
            self.__Move_pos_x = 0
            self.__Move_pos_y = 0
   
    def is_uploaded_img(self):
        if self.__image is not None :
            return True
        return False
    
    def get_fft_components(self):
        return self.__ft_components
    


