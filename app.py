import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout,\
        QHBoxLayout, QVBoxLayout, QStatusBar, QTabWidget, QLabel, QSizePolicy, QSplitter
from PyQt6.QtCore import Qt

from layout_colorwidget import Color
from lims_widgets import PlateWidget, FixedAspectWidget

import sys
import management


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BRF Sanger Sequencing")
        self.setGeometry(100,100,1000,600)
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        # Apply stylesheet to the splitter handle
        main_splitter.setHandleWidth(4)
        main_splitter.setStyleSheet("""
                QSplitter::handle {
                    background-color: #EEDDDD;
                    border: 0px solid white;
                    width: 2px; /* For horizontal splitter */
                    height: 2px; /* For vertical splitter */
                    padding: 0px;
                }
                QSplitter::handle:hover {
                    background-color: cyan;
                }
            """)
        management_widget = management.ManagementWidget()
        #management_widget = QTabWidget()
        ## tab1 import sample submissions
        #tab1_content = QWidget()
        #tab1_layout = QVBoxLayout()
        #tab1_layout.addWidget(QLabel("Import sample submissions"))
        #tab1_content.setLayout(tab1_layout)
        ## tab2 show jobs by ID
        #tab2_content = QWidget()
        #tab2_layout = QVBoxLayout()
        #tab2_layout.addWidget(QLabel("Look up by existing submission ID"))
        #tab2_content.setLayout(tab2_layout)
        ## search by researcher
        #tab3_content = QWidget()
        #tab3_layout = QVBoxLayout()
        #tab3_layout.addWidget(QLabel("Look up by researcher"))
        #tab3_content.setLayout(tab3_layout)
        ## plateID
        #tab4_content = QWidget()
        #tab4_layout = QVBoxLayout()
        #tab4_layout.addWidget(QLabel("Look up by plate ID"))
        #tab4_content.setLayout(tab4_layout)
        ## add tabs to QTabWidget
        #management_widget.addTab(tab1_content, 'Import')
        #management_widget.addTab(tab2_content, 'Submission ID')
        #management_widget.addTab(tab3_content, 'Researcher')
        #management_widget.addTab(tab4_content, 'Plate ID')
        # add plate view in the 2nd column
        plate_frame = FixedAspectWidget(8,12)
        plate_layout = QHBoxLayout()
        plate_frame.setLayout(plate_layout)
        plate_widget_96 = PlateWidget(8,12)
        plate_layout.addWidget(plate_widget_96)
        # plate info column
        info_widget = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        info_widget.setSizePolicy(sizePolicy)
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel("Info about samples in the plate"))
        info_widget.setLayout(info_layout)

        # add these to the splitter
        main_splitter.addWidget(management_widget)
        main_splitter.addWidget(plate_frame)
        main_splitter.addWidget(info_widget)
        main_splitter.setSizes([200,300,100])

        main_layout.addWidget(main_splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.setStatusBar(QStatusBar(self))


def main():
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)

    # Open the qss styles file and read in the CSS-like styling code
    styles_fn = 'styles.qss'
    if Path(styles_fn).exists():
        with open(styles_fn, 'r') as f:
            style = f.read()

        # Set the stylesheet of the application
        app.setStyleSheet(style)

    # Create our window.
    window = MainWindow()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
if __name__ == '__main__':
    main()
