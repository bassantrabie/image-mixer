from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath, QPen , QLinearGradient , QColor
from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtWidgets import QWidget
import numpy as np
import PyQt5
import logging

logging.basicConfig(filemode="a", filename="our_log.log",
                    format="(%(asctime)s) | %(name)s| %(levelname)s | => %(message)s", level=logging.INFO)
class CompWidget(QWidget ):
    all_widgets = []
    num_of_widgets=0
    def __init__(self, comp=None, parent=None , attachements=None ,function_tst=None):
        super(CompWidget, self).__init__(parent)
        self.__widget_num= CompWidget.num_of_widgets
        CompWidget.num_of_widgets+=1
        self.__Component=comp
        self.__pixmap = None
        self.__rect_start = None  # To store the starting point of the rectangle
        self.__rect_end = None    # To store the current position for the rectangle
        
        self.__data=None
        self.__cropped_data=None
        
        self.__combox=attachements['combox']
        self.__slider=attachements['slider']
        CompWidget.all_widgets.append(self)

        self.function_tst=function_tst

    # override on the Qwidget
    def paintEvent(self, event):
        if self.__pixmap:
            painter = QPainter(self)

            # Make image border radius
            rect = QRectF(self.rect())
            path = QPainterPath()
            path.addRoundedRect(rect, 20, 20)
            painter.setClipPath(path)

            # Resize the image
            scaled_pixmap = self.__pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Draw the pixmap
            painter.drawPixmap(self.rect(), scaled_pixmap)
            if self.__rect_start and self.__rect_end:
                rect = QRectF(self.__rect_start, self.__rect_end)
                transparent_blue = QColor(0, 0, 255, 20)  
                painter.setBrush(transparent_blue)  
                painter.setPen(Qt.transparent)  
                painter.drawRect(rect)
                pen = QPen(Qt.blue, 2)
                painter.setPen(pen)
                rect = QRectF(self.__rect_start, self.__rect_end)
                painter.drawRect(rect)


    def mousePressEvent(self, event):
        # Start the rectangle drawing at mouse click position
        self.__rect_start = event.pos()
        self.__rect_end = self.rect_start  # Set end point to the start initially


    def mouseMoveEvent(self, event):  
        # Update the end point while the mouse moves
        if self.__rect_start:
            self.__rect_end = event.pos()
            CompWidget.draw_rectangle_on_all_widgets(self.__rect_start ,self.__rect_end )
            
            # self.function_tst()
        

    def mouseReleaseEvent(self, event):
        # Complete the rectangle drawing on mouse release
        if self.__rect_start and self.__rect_end:
            self.__rect_end = event.pos()
            CompWidget.draw_rectangle_on_all_widgets(self.__rect_start ,self.__rect_end )
            self.function_tst()
           

           

    def set_component(self, Component , text):
        # Convert component to QPixmap
        if Component:
            self.__combox.setCurrentText(text)
            self.__data=Component['org']
            self.__pixmap = self.convert_np_pixmap(Component['np_img'])

            if self.__rect_start is None:
                self.__rect_start = PyQt5.QtCore.QPoint(41, 48)
                self.__rect_end = PyQt5.QtCore.QPoint(253, 303)
            CompWidget.draw_rectangle_on_all_widgets(self.__rect_start ,self.__rect_end )            
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

     
    def get_data_shape(self):
        # print(f"lengthhh : {len(self.cropped_data)}")
        if self.__data is not None:
            return self.__data.shape
        else : return 0
       


    def get_crop_data_widget(self):
        return self.__cropped_data
    
    def get_Curr_Mode(self):
        return  f"{self.__combox.currentText()}"
    
    def get_widget_number(self):
        return self.__widget_num
    
    def get_slider_value(self):
        return self.__slider.value()
    
    def get_combox(self):
        return self.__combox
    
    
    def get_slider(self):
        return self.__slider
    
    def get_output_display_funciton(self):
        return self.function_tst


    @classmethod
    def draw_rectangle_on_all_widgets(cls, start, end):
        """This method draws the same rectangle on all widgets"""
        for widget in cls.all_widgets:
            if widget.__pixmap:
                logging.info(f"here in the widget number : {widget.__widget_num}")
                widget.__rect_start = start
                widget.__rect_end = end
                widget.update()  # Repaint each widget

    @classmethod
    def clear_rectangle_on_all_widgets(cls):
        logging.info("Remove the Rectangles from the all widgets")
        for widget in cls.all_widgets:
            if widget.__pixmap:
                widget.__rect_start = None
                widget.__rect_end = None
                widget.update()  # Repaint each widget



    
    @classmethod
    def extract_data_inside_rectangle(cls , mode):
        for widget in cls.all_widgets:
            if widget.__rect_start and widget.__rect_end and widget.__pixmap:
                if (widget.__rect_start == widget.__rect_end ):
                    rect_start  = PyQt5.QtCore.QPoint(41, 48)
                    rect_end = PyQt5.QtCore.QPoint(253, 303)
                else:
                    rect_start =widget.__rect_start
                    rect_end   =widget.__rect_end

                # Calculate the QRectF from the rectangle start and end
                rect = QRectF(rect_start, rect_end)
                start_x = int(rect.x())
                start_y = int(rect.y())
                width = int(rect.width())
                height = int(rect.height())
               
                if mode=='InsideRegion':           
                    mask = np.zeros(widget.__data.shape, dtype=np.float32)       
                    mask[start_y:start_y+height, start_x:start_x+width] = 1
                else:
                    mask =  np.ones(widget.__data.shape, dtype=np.float32)       
                    mask[start_y:start_y+height, start_x:start_x+width] = 0

                
             
                widget.__cropped_data = widget.__data* mask

    # @classmethod
    # def Get_CroppedData(cls):
    #     data={}
    #     for widget in cls.all_widgets:
    #         if widget.cropped_data is not None :
    #             data[f"{widget.widget_num}"]=[f"{widget.combox.currentText()}" ,widget.slider.value(),widget.cropped_data]
                
    #         # else :
    #         #     print(f"No_cropprd_data in this widget :{widget.widget_num}")
    #     logging.info("Calculated the Cropped Data")
    #     return data
    
    @classmethod
    def Get_All_created_widgets(cls):
        exist_widgets=[]
        for widget in cls.all_widgets:
            if widget.__cropped_data is not None :
                exist_widgets.append(widget)
        return exist_widgets

   