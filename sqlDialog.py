import datetime

from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide2.QtCore import QObject, Qt, Property, Slot, Signal

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

    query.exec("INSERT INTO Conversations VALUES('Me', 'machine', '2016-01-07T14:36:06', 'Hello!')");
    query.exec("INSERT INTO Conversations VALUES('machine', 'Me', '2016-01-07T14:36:16', 'Good afternoon.')");


class SqlConversationModel(QObject):
    recipientChanged = Signal()
    def __init__(self, parent=QSqlTableModel):
        super(SqlConversationModel, self).__init__()
        
        self.table = QSqlTableModel()

        createTable()
        self.table.setTable(conversationsTableName)
        self.table.setSort(2, Qt.DescendingOrder)
        self.table.setEditStrategy(QSqlTableModel.OnManualSubmit)

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
        if role < Qt.UserRole:
            return data(index, role)

        self.sqlRecord = record(index.row())
        return self.sqlRecord.value(role - Qt.UserRole)

    def roleNames(self):
        self.names
        self.names[Qt.UserRole] = "author"
        self.names[Qt.UserRole + 1] = "recipient"
        self.names[Qt.UserRole + 2] = "timestamp"
        self.names[Qt.UserRole + 3] = "message"
        return self.names

    @Slot(str, str)
    def sendMessage(self, recipient, message):
        print("message to send: " + message)
        newRecord = self.table.record()
        newRecord.setValue("author", "Me")
        newRecord.setValue("recipient", recipient)
        print("recipient receiving the message you just sent: " + recipient)
        timestamp = datetime.datetime.now()
        newRecord.setValue("timestamp", timestamp)
        newRecord.setValue("message", message)
        if not self.table.insertRecord(self.table.rowCount(), newRecord):
            print("Failed to send message:" + lastError().text())
            return
        else:
            print('Message was succesfully inserted in table 🌸')

        self.table.submitAll()

