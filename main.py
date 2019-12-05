#############################################################################
##
## Copyright (C) 2019 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 3 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL3 included in the
## packaging of this file. Please review the following information to
## ensure the GNU Lesser General Public License version 3 requirements
## will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 2.0 or (at your option) the GNU General
## Public license version 3 or any later version approved by the KDE Free
## Qt Foundation. The licenses are as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-2.0.html and
## https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

import sys
import os
import logging
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, QDir

from PySide2.QtGui import QGuiApplication
from PySide2.QtSql import QSqlDatabase
from PySide2.QtQml import QQmlApplicationEngine
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

    # Ensure that we have a writable location on all devices
    fileName = writeDir.absolutePath() + "/chat-database.sqlite3"
    database.setDatabaseName(fileName)
    # open() will create the SQLite database if it doesn't exist
    if not database.open():
        logger.error("Cannot open database")
        QFile.remove(fileName)

if __name__ == "__main__":
    logging.info('Started')
    app = QGuiApplication()

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
    qmlFile = os.path.join(os.path.dirname(__file__), "chat.qml")
    engine.load(QUrl.fromLocalFile(os.path.abspath(qmlFile)))

    ret = app.exec_()

    # Signal to inference thread that the application is quitting
    inference_thread.setQuit()
    logging.info('Finished')
    sys.exit(ret)
