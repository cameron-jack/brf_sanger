import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

from layout_colorwidget import Color

class RoundedBoxWidget(QWidget):
    def __init__(self,x=100,y=100,w=300,h=200):
        super().__init__()
        #self.setWindowTitle("Rounded Box Example")
        self.setGeometry(x, y, w, h)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Rounded QPushButton
        button = QPushButton("Rounded Button")
        button.setStyleSheet("""
            QPushButton {
                border-radius: 15px; /* Adjust radius as needed */
                background-color: #4CAF50;
                color: white;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(button)

        # Rounded QFrame (as a container for other widgets)
        frame = QWidget() # Using QWidget as a frame for simplicity
        frame.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 2px solid #ccc;
                border-radius: 20px; /* Adjust radius as needed */
            }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(10,10,10,10)
        frame_layout.setSpacing(10)
        frame_layout.addWidget(QPushButton("Inside Frame"))
        colours = ['red','orange','yellow','green','blue','purple']
        frame_layout.addWidget(Color('red'))
#        for c in colours:
#            frame_layout.addWidget(Color(c))
#        layout.setContentsMargins(0,0,0,0)
#        layout.setSpacing(10)
#        colours = ['red','orange','yellow','green','blue','purple']
#        for row in range(rows):
#            for col in range(cols):
#                c = (row*12+col) % len(colours)
#                layout.addWidget(Color(colours[c]), row, col)
        layout.addWidget(frame)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoundedBoxWidget()
    window.show()
    sys.exit(app.exec())
