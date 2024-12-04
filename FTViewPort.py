from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath, QPen , QLinearGradient , QColor
from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtWidgets import QWidget
import numpy as np
class CompWidget(QWidget):
    all_widgets = []
    num_of_widgets=0
    def __init__(self, comp=None, parent=None , attachements=None):
        super(CompWidget, self).__init__(parent)
        self.widget_num= CompWidget.num_of_widgets
        CompWidget.num_of_widgets+=1
        self.Component=comp
        self.pixmap = None
        self.rect_start = None  # To store the starting point of the rectangle
        self.rect_end = None    # To store the current position for the rectangle
        self.data=None
        self.cropped_data=None
        
        self.combox=attachements['combox']
        self.slider=attachements['slider']
        CompWidget.all_widgets.append(self)
    
    def paintEvent(self, event):
        if self.pixmap:
            painter = QPainter(self)

            # Make image border radius
            rect = QRectF(self.rect())
            path = QPainterPath()
            path.addRoundedRect(rect, 20, 20)
            painter.setClipPath(path)

            # Resize the image
            scaled_pixmap = self.pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            # Draw the pixmap
            painter.drawPixmap(self.rect(), scaled_pixmap)
    
            if self.rect_start and self.rect_end:
                rect = QRectF(self.rect_start, self.rect_end)
                transparent_blue = QColor(0, 0, 255, 20)  
                painter.setBrush(transparent_blue)  
                painter.setPen(Qt.transparent)  
                painter.drawRect(rect)

                pen = QPen(Qt.blue, 2)
                painter.setPen(pen)
                rect = QRectF(self.rect_start, self.rect_end)
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        # Start the rectangle drawing at mouse click position
        self.rect_start = event.pos()
        self.rect_end = self.rect_start  # Set end point to the start initially

    def mouseMoveEvent(self, event):  
        # Update the end point while the mouse moves
        if self.rect_start:
            self.rect_end = event.pos()
            CompWidget.draw_rectangle_on_all_widgets(self.rect_start ,self.rect_end )

    def mouseReleaseEvent(self, event):
        # Complete the rectangle drawing on mouse release
        if self.rect_start and self.rect_end:
            self.rect_end = event.pos()
            CompWidget.draw_rectangle_on_all_widgets(self.rect_start ,self.rect_end )
            # CompWidget.extract_data_inside_rectangle()

           

    def display_component(self, Component , index):
        # Convert component to QPixmap
        if Component:
            self.combox.setCurrentIndex(index)
            self.data=Component['org']
            self.pixmap = self.convert_np_pixmap(Component['np_img'])
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




    @classmethod
    def draw_rectangle_on_all_widgets(cls, start, end):
        """This method draws the same rectangle on all widgets"""
        for widget in cls.all_widgets:
            if widget.pixmap:
                widget.rect_start = start
                widget.rect_end = end
                widget.update()  # Repaint each widget

    
    @classmethod
    def extract_data_inside_rectangle(cls , mode):
        for widget in cls.all_widgets:
            if widget.rect_start and widget.rect_end and widget.pixmap:
                # Calculate the QRectF from the rectangle start and end
                rect = QRectF(widget.rect_start, widget.rect_end)
                start_x = int(rect.x())
                start_y = int(rect.y())
                width = int(rect.width())
                height = int(rect.height())
               
                if mode=='InsideRegion':           
                    mask = np.zeros(widget.data.shape, dtype=np.float32)       
                    mask[start_y:start_y+height, start_x:start_x+width] = 1
                else:
                    mask =  np.ones(widget.data.shape, dtype=np.float32)       
                    mask[start_y:start_y+height, start_x:start_x+width] = 0

                
                
                widget.cropped_data = widget.data* mask

    @classmethod
    def Get_CroppedData(cls):
        data={}
        for widget in cls.all_widgets:
            if widget.cropped_data is not None :
                data[f"{widget.widget_num}"]=[f"{widget.combox.currentText()}" ,widget.slider.value(),widget.cropped_data]
                
            # else :
            #     print(f"No_cropprd_data in this widget :{widget.widget_num}")
        return data



    def get_combox(self):
        return self.combox