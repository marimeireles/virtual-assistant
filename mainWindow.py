import sys
import random
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import *

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.conversationLayout = QVBoxLayout()
        self.gadgetLayout = QVBoxLayout()

class AudioRecorderTest(QMediaObject):
    def __init__(self):
        QWidget.__init__(self)
        self.audioRecorder = QAudioRecorder()