import sys
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QLineEdit)
from PySide2.QtCore import Slot, Qt

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
            "Hola Mundo", "Привет мир"]

        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

        # CreateMenus()

        self.edit = QLineEdit("Write my name here..")
        self.button1 = QPushButton("Show Greetings")

        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.button1)
        # Set dialog layout

        self.button1.clicked.connect(self.greetings)

        self.audioRecorder = QAudioRecorder
        self.layout.addWidget(self.audioRecorder)



    def greetings(self):
        print ("Hello {}".format(self.edit.text()))

    @Slot()
    def magic(self):    
        self.text.setText(random.choice(self.hello))

    # def CreateMenus():
    #     fileMenu = menuBar().addMenu("Settings")

    # def SettingsOpt():
    #     Settings.setMenu(menu)
    #     Settings.setPopupMode(QToolButton.MenuButtonPopup)
    #     Settings.addAction("Settings", SettingsAction())

    # def SettingsAction():
    #     self.text = QLabel("SettingsAction")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.showMaximized();
    widget.show()

    sys.exit(app.exec_())
