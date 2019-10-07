import sys

from PySide2.QtWidgets import *
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, QDateTime, Qt
from PySide2.QtGui import QGuiApplication

from mainWindow import MainWindow
from dialog import Dialog
from audioManager import AudioRecorder, InferenceThread

# if __name__ == "__main__":
#     app = QGuiApplication(sys.argv)

#     view = QQuickView()

#     view.rootContext().setContextProperty("applicationData", QDateTime.currentDateTime())
#     #can add the user dialog here and the machine, make an if in the qml depending on which then I do an specific thing
#     #the idea of the sql thing is a cool feature for the future

#     QQmlApplicationEngine(engine("chat.qml"))

#     # view.setSource(QUrl("chat.qml"))
#     # view.show()

    # app.exec_()

# import sys
# from os.path import abspath, dirname, join
# from PySide2.QtCore import QCoreApplication, QObject
# from PySide2.QtGui import QGuiApplication
# from PySide2.QtQml import QQmlApplicationEngine

# if __name__ == "__main__":
#     app = QGuiApplication()
#     engine = QQmlApplicationEngine()
#     # dialog = Dialog()
#     view = QDateTime.currentDateTime()
#     context = engine.rootContext()
#     context.setContextProperty("applicationData", view)
#     sentbyme = "Me"
#     context.setContextProperty("sentByMe", sentbyme)
#     # 'example_view.qml' needs to be changed
#     qml_file = join(dirname(__file__), "chat.qml")
#     engine.load(abspath(qml_file))
#     if not engine.rootObjects():
#         sys.exit(-1)

#     sys.exit(app.exec_())



# # This Python file uses the following encoding: utf-8
# import sys
# import os
# from PySide2.QtCore import QUrl, QStringListModel
# from PySide2.QtGui import QGuiApplication
# from PySide2.QtQml import QQmlApplicationEngine
# if __name__ == '__main__':
#     app = QGuiApplication(sys.argv)
#     engine = QQmlApplicationEngine()
#     engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))
#     if not engine.rootObjects():
#         sys.exit(-1)
#     sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = Dialog()
    inferenceThread = InferenceThread()
    audioRecorder = AudioRecorder(dialog, inferenceThread)

    widget = MainWindow(dialog, audioRecorder)
    widget.showMaximized();
    widget.show()

    # Start inference thread
    inferenceThread.start()

    ret = app.exec_()

    # Signal to inference thread that the application is quitting
    inferenceThread.setQuit()

    sys.exit(ret)