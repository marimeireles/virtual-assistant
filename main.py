import sys
from PySide2.QtWidgets import *
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

from mainWindow import MainWindow
from dialog import Dialog
from audioManager import AudioRecorder, InferenceThread

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # view = QQuickView()
    # url = QUrl("main.qml")
    # view.setSource(url)

    dialog = Dialog()
    inferenceThread = InferenceThread()
    audioRecorder = AudioRecorder(dialog, inferenceThread)

    widget = MainWindow(dialog, audioRecorder)
    # widget.createWindowContainer(view)
    widget.showMaximized();
    widget.show()
    # view.show()

    # Start inference thread
    inferenceThread.start()

    ret = app.exec_()

    # Signal to inference thread that the application is quitting
    inferenceThread.setQuit()

    sys.exit(ret)