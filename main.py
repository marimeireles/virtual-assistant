import sys
import os
import logging 

from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, QDateTime, Qt, QStandardPaths, QDir, QStringListModel
from PySide2.QtGui import QGuiApplication
from PySide2.QtSql import QSqlDatabase
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWebEngineWidgets import QWebEngineView

from dialog import Dialog
from audioManager import AudioRecorder, InferenceThread
from sqlDialog import SqlConversationModel

logging.basicConfig(filename='myapp.log', level=logging.INFO)

def connectToDatabase():
    database = QSqlDatabase.database()
    if not database.isValid():
        database = QSqlDatabase.addDatabase("QSQLITE")
        if not database.isValid():
            logger.error("Cannot add database")

    writeDir = QDir()
    # writeDir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    if not writeDir.mkpath("."):
        logger.error("Failed to create writable directory")

    # Ensure that we have a writable location on all devices.
    fileName = writeDir.absolutePath() + "/chat-database.sqlite3"
    # When using the SQLite driver, open() will create the SQLite database if it doesn't exist.
    database.setDatabaseName(fileName)
    if not database.open():
        logger.error("Cannot open database")
        QFile.remove(fileName)

if __name__ == "__main__":
    logging.info('Started')
    app = QApplication()
    # QWebEngineView.initialize() 

    connectToDatabase()

    inference_thread = InferenceThread()
    # Start inference thread
    inference_thread.start()
    sql_conversation_model = SqlConversationModel()
    dialog = Dialog(sql_conversation_model)
    audio_recorder = AudioRecorder(dialog, inference_thread)

    engine = QQmlApplicationEngine()
    # Export pertinent objects to QML
    engine.rootContext().setContextProperty("chat_model", sql_conversation_model)
    engine.rootContext().setContextProperty("audio_recorder", audio_recorder)
    amplitude = 0
    engine.rootContext().setContextProperty("amplitude", amplitude)
    engine.load(QUrl("chat.qml"))

    ret = app.exec_()

    # Signal to inference thread that the application is quitting
    inference_thread.setQuit()
    logging.info('Finished')
    sys.exit(ret)