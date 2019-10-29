import datetime

from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlRecord
from PySide2.QtCore import QObject, Qt, Property, Slot, Signal, QByteArray

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
        print("Failed to query database")
    print('#######')
    print(query)


class SqlConversationModel(QSqlTableModel):
    recipientChanged = Signal()
    def __init__(self, parent=None):
        super(SqlConversationModel, self).__init__(parent)

        createTable()
        self.setTable(conversationsTableName)
        self.setSort(2, Qt.DescendingOrder)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)

        recipient = Property(str, self.recipient, notify=self.recipientChanged)
        print('Table was loaded succesfully 🌈🌈🌈\n')


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
        # print("inside data index:", index, " role", role)
        if role < Qt.UserRole:
            return QSqlTableModel.data(self, index, role)

        sqlRecord = QSqlRecord()
        sqlRecord = self.record(index.row())
        return sqlRecord.value(role - Qt.UserRole)

    # @Slot(result='hash')
    def roleNames(self):
        # print("inside roleNames")
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

    @Slot(str, str)
    def sendMessage(self, recipient, message):
        print("message to send: " + message)
        newRecord = self.record()
        newRecord.setValue("author", "Me")
        newRecord.setValue("recipient", recipient)
        print("recipient receiving the message you just sent: " + recipient)
        timestamp = datetime.datetime.now()
        newRecord.setValue("timestamp", timestamp)
        newRecord.setValue("message", message)
        if not self.insertRecord(self.rowCount(), newRecord):
            print("Failed to send message:" + lastError().text())
            return
        else:
            print('userMessage was succesfully inserted in table 🌸')

    def sendMachineMessage(self, recipient, message):
        print("message to send: " + message)
        newRecord = self.record()
        newRecord.setValue("author", "machine")
        newRecord.setValue("recipient", recipient)
        print("recipient receiving the message you just sent: " + recipient)
        timestamp = datetime.datetime.now()
        newRecord.setValue("timestamp", timestamp)
        newRecord.setValue("message", message)
        if not self.insertRecord(self.rowCount(), newRecord):
            print("Failed to send message:" + lastError().text())
            return
        else:
            print('Mahcine Message was succesfully inserted in table 🌸')


        self.submitAll()

