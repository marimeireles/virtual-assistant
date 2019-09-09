from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide2.QtCore import Signal

class Dialog(QWidget):
    # change = Signal
    def __init__(self):
        super(Dialog, self).__init__()

        self.userLayout = QVBoxLayout()
        self.machineLayout = QVBoxLayout()

        self.userText = ""
        self.machineText = ""

        self.setLayout(self.userLayout)

    def showUserMessage(self):
        self.userQLabel = QLabel()
        self.userQLabel.setText(self.userText)

        self.userLayout.addWidget(self.userQLabel)

    def setUserMessage(self, string):
        self.userText = string

    def getUserMessage(self):
        return self.userText

    def showMachineMessage():
        pass