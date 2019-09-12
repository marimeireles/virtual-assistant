from audioManager import AudioRecorder
from dialog import Dialog

from PySide2.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self, audioRecorder, dialog):
        super(MainWindow, self).__init__()

        self.audioRecorder = audioRecorder
        self.dialog = dialog

        self.mainLayout = QHBoxLayout()

        self.conversationLayout = QHBoxLayout()
        self.gadgetLayout = QHBoxLayout()

        self.gadgetLayout.addWidget(self.audioRecorder)
        self.conversationLayout.addWidget(self.dialog)