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

import datetime
import logging

from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlRecord
from PySide2.QtCore import QObject, Qt, Property, Slot, Signal, QByteArray

from dialog import Dialog

conversationsTableName = "Conversations"

def createTable():
    if conversationsTableName in QSqlDatabase.database().tables():
        return

    query = QSqlQuery()
    if not query.exec_(
        "CREATE TABLE IF NOT EXISTS 'Conversations' ("
        "'author' TEXT NOT NULL,"
        "'recipient' TEXT NOT NULL,"
        "'timestamp' TEXT NOT NULL,"
        "'message' TEXT NOT NULL,"
        "FOREIGN KEY('author') REFERENCES Contacts ( name ),"
        "FOREIGN KEY('recipient') REFERENCES Contacts ( name )"
        ")"):
        logging.error("Failed to query database")
    logging.info(query)


class SqlConversationModel(QSqlTableModel):
    recipientChanged = Signal()
    def __init__(self, parent=None):
        super(SqlConversationModel, self).__init__(parent)

        createTable()
        self.setTable(conversationsTableName)
        self.setSort(2, Qt.DescendingOrder)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)

        recipient = Property(str, self.recipient, notify=self.recipientChanged)
        self.select()
        logging.debug("Table was loaded successfully.")


    def recipient():
        return self.recipient

    def setRecipient(self, recipient):
        if recipient == self.recipient:
            pass

        self.recipient = recipient

        filterString = ("(recipient = '{}' AND author = 'Me') OR (recipient = 'Me' AND author='{}')").format(self.recipient)
        setFilter(filterString)
        select()

        emit(recipientChanged())

    def data(self, index, role):
        if role < Qt.UserRole:
            return QSqlTableModel.data(self, index, role)

        sqlRecord = QSqlRecord()
        sqlRecord = self.record(index.row())

        return sqlRecord.value(role - Qt.UserRole)

    def roleNames(self):
        '''Converts dict to hash because that's the result expected by QSqlTableModel'''
        names = {}
        author = "author".encode()
        recipient = "recipient".encode()
        timestamp = "timestamp".encode()
        message = "message".encode()

        names[hash(Qt.UserRole)] = author
        names[hash(Qt.UserRole + 1)] = recipient
        names[hash(Qt.UserRole + 2)] = timestamp
        names[hash(Qt.UserRole + 3)] = message

        return names

    @Slot(str, str, str)
    def send_message(self, recipient, message, author):
        newRecord = self.record()
        newRecord.setValue("author", author)
        newRecord.setValue("recipient", recipient)
        timestamp = datetime.datetime.now()
        newRecord.setValue("timestamp", str(timestamp))
        newRecord.setValue("message", message)

        logging.debug("Message: \"{message}\" \n Received by: \"{recipient}\"")

        if not self.insertRecord(self.rowCount(), newRecord):
            logging.error("Failed to send message: " + lastError().text())
            return

        self.submitAll()
        self.select()
