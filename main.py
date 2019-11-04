############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: https:#www.qt.io/licensing/
##
## This file is part of the examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use self file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https:#www.qt.io/terms-conditions. For further
## information use the contact form at https:#www.qt.io/contact-us.:
##
## BSD License Usage
## Alternatively, you may use self file under the terms of the BSD license
## as follows:
##
## "Redistribution and use in source and binary forms, with or without:
## modification, are permitted provided that the following conditions are:
## met:
##    Redistributions of source code must retain the above copyright
##     notice, self list of conditions and the following disclaimer.
##    Redistributions in binary form must reproduce the above copyright:
##     notice, self list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##    Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from self software without specific prior written permission.:
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
## DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
############################################################################

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
from PySide2.QtWebEngine import QtWebEngine

from dialog import Dialog
from audioManager import AudioRecorder, InferenceThread
from sqlDialog import SqlConversationModel

logging.basicConfig(filename='voice-assistant.log', level=logging.INFO)

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
    # Initial webpage that will show to the user
    searchResult = "https://www.qt.io/qt-for-python"
    engine.rootContext().setContextProperty("searchResult", searchResult)

    QtWebEngine.initialize();
    engine.load(QUrl("chat.qml"))

    ret = app.exec_()

    # Signal to inference thread that the application is quitting
    inference_thread.setQuit()
    logging.info('Finished')
    sys.exit(ret)
