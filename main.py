import sys
import os

from PySide2.QtWidgets import *
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

    qmlRegisterType(SqlConversationModel, "SqlConversationModel", 1, 0, "SqlConversationModel")

    connectToDatabase()
    a = SqlConversationModel()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("SqlConversationModel", a)
    engine.load(QUrl("chat.qml"))

    '''
    >I tried textRole: "SqlConversationModel" and it didn't work on my ApplicationWindow mode
    it may work in a different mode? (these modes are called qtquick control). it worked in a combobox
    but I obviously cant put everything I have in a combo box :p
    >next step here is try to implement a stackview here and try to activate
    root.StackView.view.push("qrc:/ConversationPage.qml", { inConversationWith: model.display })
    the inConversationWith somehow
    >my model isn't being recognized inside the function on line 56 or something, but I have the feeling I'm 
    importing it correctly in the begining where I do model:Sqlblablabla, otherwise it would accuse an error here right?
    '''

    # dialog = Dialog()
    # inferenceThread = InferenceThread()
    # audioRecorder = AudioRecorder(dialog, inferenceThread)

    # app = app.exec_()

    # # Signal to inference thread that the application is quitting
    # inferenceThread.setQuit()
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