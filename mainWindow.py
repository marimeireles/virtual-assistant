import sys
import random
from PySide2.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.conversationLayout = QVBoxLayout()
        self.gadgetLayout = QVBoxLayout()

        view = QQuickView()
        url = QUrl("view.qml")

        view.setSource(url)