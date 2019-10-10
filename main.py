import sys

from PySide2.QtWidgets import *
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, QDateTime, Qt, QStandardPaths, QDir
from PySide2.QtGui import QGuiApplication
from PySide2.QtSql import QSqlDatabase
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType

from mainWindow import MainWindow
from dialog import Dialog
from audioManager import AudioRecorder, InferenceThread
from sqlDialog import SqlConversationModel

def connectToDatabase():
    database = QSqlDatabase.database()
    if not database.isValid():
        database = QSqlDatabase.addDatabase("QSQLITE")
        if not database.isValid():
            print("Cannot add database")

    writeDir = QDir()
    # writeDir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    if not writeDir.mkpath("."):
        print("Failed to create writable directory")

    # Ensure that we have a writable location on all devices.
    fileName = writeDir.absolutePath() + "/chat-database.sqlite3"
    # When using the SQLite driver, open() will create the SQLite database if it doesn't exist.
    database.setDatabaseName(fileName)
    if not database.open():
        print("Cannot open database")
        QFile.remove(fileName)

if __name__ == "__main__":

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication()

    # what is this
    qmlRegisterType(SqlConversationModel, "io.qt.examples.chattutorial", 1, 0, "SqlConversationModel")

    connectToDatabase()

    engine = QQmlApplicationEngine()
    engine.load(QUrl("chat.qml"))

    dialog = Dialog()
    inferenceThread = InferenceThread()
    audioRecorder = AudioRecorder(dialog, inferenceThread)

    app = app.exec_()

    # Signal to inference thread that the application is quitting
    inferenceThread.setQuit()

    sys.exit(app)

### this is working if I just want to run things the way I'm currently doing
#remember to erase the stuff in the dialog thing, where I'm adding sql modules

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     dialog = Dialog()
#     inferenceThread = InferenceThread()
#     audioRecorder = AudioRecorder(dialog, inferenceThread)

#     widget = MainWindow(dialog, audioRecorder)
#     widget.showMaximized();
#     widget.show()

#     # Start inference thread
#     inferenceThread.start()

#     ret = app.exec_()

#     # Signal to inference thread that the application is quitting
#     inferenceThread.setQuit()

#     sys.exit(ret)