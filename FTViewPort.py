from PyQt5.QtGui import QPainter, QPixmap, QImage, QPainterPath, QPen , QLinearGradient , QColor
from PyQt5.QtCore import QRectF, Qt, QPoint
from PyQt5.QtWidgets import QWidget

class CompWidget(QWidget):
    all_widgets = []
    def __init__(self, comp=None, parent=None):
        super(CompWidget, self).__init__(parent)
        self.pixmap = comp
        self.rect_start = None  # To store the starting point of the rectangle
        self.rect_end = None    # To store the current position for the rectangle
        
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
           

    def display_component(self, comp):
        # Convert component to QPixmap
        qimage = QImage(
            comp.tobytes(),
            comp.width,
            comp.height,
            comp.width,
            QImage.Format_Grayscale8
        )
        self.pixmap = QPixmap.fromImage(qimage)
        self.update()


    @classmethod
    def draw_rectangle_on_all_widgets(cls, start, end):
        """This method draws the same rectangle on all widgets"""
        for widget in cls.all_widgets:
            if widget.pixmap:
                widget.rect_start = start
                widget.rect_end = end
                widget.update()  # Repaint each widget
    