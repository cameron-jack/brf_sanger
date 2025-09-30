from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QPushButton, QFrame, QGraphicsItem, QSizePolicy, QLabel

from PyQt6.QtGui import QPainter, QResizeEvent, QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QRectF, QSize, QRect, QEvent

import sys


class RoundBox(QFrame):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)


    def sizeHint(self):
        """
        Provide a reasonable initial size hint
        """
        return QSize(20, 20)


    def resizeEvent(self, event):
        # called after all events
        new_size = event.size()
        if new_size.width() == event.oldSize().width() and new_size.height() == event.oldSize().height():
            return
        radius = int(min(new_size.width(), new_size.height()) // 2)
        ss = self.styleSheet()
        #print(f'resizeEvent: styleSheet {ss=}')
        if 'border_radius' in ss:
            pre = ss.split('border_radius: ')[0]
            post = ss.split('border_radius: ')[1].split('px; ', 0)[1]
            ss = f'{pre}' + f' border_radius: {radius}' + f'{post}'
            #print(f'resizeEvent {ss=}')
        else:
            ss = f'RoundBox {{ background-color: cyan; border: 2px solid darkgray; border-radius: {radius}px; }}'
        self.setStyleSheet(ss)


    def event(self, event):
        if event.type() == QEvent.Type.HoverEnter:
            #print("Mouse entered widget!")
            radius = int(min(self.width(), self.height()) // 2)
            #print(f'{radius=} {self.width()=} {self.height()=}')
            ss = f'RoundBox {{ background-color: green; border: 3px solid darkgray; border-radius: {radius}px;}}'
            #print(f'Should happen once {ss=}')
            self.setStyleSheet(ss)
            #print(f'After setting stylesheet {self.styleSheet()=}')
        elif event.type() == QEvent.Type.HoverLeave:
            #print("Mouse left widget!")
            radius = int(min(self.width(), self.height()) // 2)
            ss = f'RoundBox {{ background-color: cyan; border: 2px solid darkgray; border-radius: {radius}px; }}'
            self.setStyleSheet(ss)
        return super().event(event)


class CircleWidget(QWidget):
    """
    DEPRECATED
    """

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.aspect_ratio = 1.0
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)


    def heightForWidth(self, width):
        return int(width / self.aspect_ratio)


    def sizeHint(self):
        """
        Provide a reasonable initial size hint
        """
        return QSize(10, int(10/self.aspect_ratio))


    def paintEvent(self, event):
        painter = QPainter(self)
        bounding_rect = self.rect()
        size = min(self.rect().width(), self.rect().height())
        new_bounds = QRectF(self.rect().left(),self.rect().top(),size,size)
        new_bounds2 = QRectF(self.rect().left()+1,self.rect().top()+1,size-2,size-2)
        painter.drawEllipse(new_bounds)
        painter.drawEllipse(new_bounds2)




class PlateWidget(QFrame):
    """
    Define an interactive plate widget and layout of up to 384-well capacity
    """
    def __init__(self, rows=8, cols=12):
        super().__init__()
        self.aspect_ratio = cols/rows
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        self.setSizePolicy(sizePolicy)
        layout = QGridLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(0)
        row_labels = ' ABCDEFGHIJKLMNOP'
        self.rows = rows
        self.cols = cols
        for row in range(rows+1):
            for col in range(cols+1):
                if row == 0 and col == 0:
                    pass
                elif row == 0:  # numbers
                    label = QLabel(str(col))
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(label, row, col)
                else:  # on to the wells now
                    if col == 0:
                       label = QLabel(row_labels[row])
                       label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                       layout.addWidget(label, row, col)
                    else:
                       # Apply the same spacing trick to maintain the aspect ratio
                       spacer_frame = MiniFixedAspectWidget(1,1)
                       spacer_layout = QHBoxLayout()
                       spacer_frame.setLayout(spacer_layout)
                       well = RoundBox()
                       #well = CircleWidget()
                       #well = QLabel('.')
                       spacer_layout.addWidget(well)
                       layout.addWidget(spacer_frame, row, col)
        self.setLayout(layout)
        self.initial_font_size = 20  # Base font size
        self.initial_width = self.width()
        self.update_font_size()


    def resizeEvent(self, event):
        #super().resizeEvent(event)
        self.update_font_size()


    def update_font_size(self):
        # Calculate a new font size based on the current window width
        # You can adjust this scaling logic as needed (e.g., based on height, or a combination)
        scale_factor = self.width() / self.initial_width
        new_font_size = int(self.initial_font_size * scale_factor)
        layout = self.layout()
        for c in range(self.cols):
            label = layout.itemAtPosition(0,c+1).widget()
            font = label.font()
            font.setPointSize(new_font_size)
            label.setFont(font)
        for r in range(self.rows):
            label = layout.itemAtPosition(r+1,0).widget()
            font = label.font()
            font.setPointSize(new_font_size)
            label.setFont(font)


class FixedAspectWidget(QWidget):
    """
    Define a widget that maintains a fixed aspect ratio
    Uses Talljosh's soluition: https://stackoverflow.com/questions/452333/how-to-maintain-widgets-aspect-ratio-in-qt
    """
    def __init__(self, rows=8, cols=12):
        super().__init__()
        self.aspect_ratio = (cols+1)/(rows+1)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)


    def heightForWidth(self, width):
        return int(width / self.aspect_ratio)


    def sizeHint(self):
        """
        Provide a reasonable initial size hint
        """
        return QSize(200, int(200/self.aspect_ratio))


    def resizeEvent(self, event):
        new_size = event.size()
        if int(new_size.width() // self.aspect_ratio) < int(new_size.height()):
            # constrained by width
            new_width = int(new_size.width())
            new_height = int(new_width // self.aspect_ratio)
        else:
            # constrained by height
            new_height = int(new_size.height())
            new_width = int(new_height * self.aspect_ratio)
        h_margin = (new_size.width() - new_width) // 2
        v_margin = (new_size.height() - new_height) // 2
        self.setContentsMargins(h_margin,v_margin,h_margin,v_margin)


class MiniFixedAspectWidget(FixedAspectWidget):
    def __init__(self, rows=1, cols=1):
        super().__init__()
        self.aspect_ratio = 1.0
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)


    def sizeHint(self):
        """
        Provide a reasonable initial size hint
        """
        return QSize(20, int(20/self.aspect_ratio))
