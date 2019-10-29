import sys
import os

from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, QDateTime, Qt, QStandardPaths, QDir, QStringListModel
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

    app = QApplication()

    inferenceThread = InferenceThread()
    # Start inference thread
    inferenceThread.start()

    sqlConversationModel = SqlConversationModel()
    qmlRegisterType(SqlConversationModel, "SqlConversationModel", 1, 0, "SqlConversationModel")
    connectToDatabase()
    engine = QQmlApplicationEngine()
    # engine.rootContext().setContextProperty("sqlConversationModel", sqlConversationModel)

    #I need to receive the same SqlConversationModel than I'm passing to my QML. but I'm not being able to, why?
    #see dialog.py line 60
    dialog = Dialog(sqlConversationModel)

    audioRecorder = AudioRecorder(dialog, inferenceThread)
    engine.rootContext().setContextProperty("audioRecorder", audioRecorder)
    engine.rootContext().setContextProperty("toggleRecord", audioRecorder.toggleRecord())

    engine.load(QUrl("chat.qml"))
    ret = app.exec_()

    # # Signal to inference thread that the application is quitting
    inferenceThread.setQuit()
    sys.exit(ret)