from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QFileDialog, QPushButton, QLabel

def get_submissions(parent):
    """ event driven dialog """
    file_names, name_filter = QFileDialog.getOpenFileNames(parent, 'Open files','','All Files (*);;Excel Files (*.xlsx)')
    return file_names


class SamplesWidget(QTabWidget):
    """
    menu/tab structure for organising samples into plates
    """
    def __init__(self):
        super().__init__()
        self.files_to_read = []
        # tab1 sample submissions
        tab1_content = QWidget()
        tab1_layout = QVBoxLayout()
        open_button = QPushButton(self)
        open_button.setText("Load submissions")
        open_button.clicked.connect(self.open_file_dialog)
        tab1_layout.addWidget(open_button)
        tab1_content.setLayout(tab1_layout)
        tab1_layout
        # tab2 show jobs by ID
        tab2_content = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel("Look up by existing submission ID"))
        tab2_content.setLayout(tab2_layout)
        # search by researcher
        tab3_content = QWidget()
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(QLabel("Look up by researcher"))
        tab3_content.setLayout(tab3_layout)
        # plateID
        tab4_content = QWidget()
        tab4_layout = QVBoxLayout()
        tab4_layout.addWidget(QLabel("Look up by plate ID"))
        tab4_content.setLayout(tab4_layout)

        # add tabs to QTabWidget
        self.addTab(tab1_content, 'Import')
        self.addTab(tab2_content, 'Submission ID')
        self.addTab(tab3_content, 'Researcher')
        self.addTab(tab4_content, 'Plate ID')


    def open_file_dialog(self):
        fnames = QFileDialog.getOpenFileNames(
            self,
            "Open Submission File(s)",
            "${HOME}",
            "Excel Files (*.xlsx);; All Files (*.*)",
        )
        self.files_to_read = fnames


if __name__ == '__main__':
    pass
