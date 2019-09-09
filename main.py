import sys
from PySide2.QtWidgets import *
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

from mainWindow import MainWindow
from dialog import Dialog
from audioManager import AudioRecorder

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = Dialog()
    audioRecorder = AudioRecorder(dialog)

    widget = MainWindow(dialog, audioRecorder)
    widget.showMaximized();
    widget.show()

    sys.exit(app.exec_())