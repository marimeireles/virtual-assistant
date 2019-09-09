from audioRecorder import AudioRecorder
from PySide2.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.conversationLayout = QVBoxLayout()
        self.gadgetLayout = QVBoxLayout()

        self.setLayout(self.conversationLayout)

        self.gadgetLayout.addWidget(AudioRecorder())
        self.setLayout(self.gadgetLayout)
