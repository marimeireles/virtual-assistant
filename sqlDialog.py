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
        logging.debug("Table was loaded succesfully.")


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
