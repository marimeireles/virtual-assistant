from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide2.QtCore import QObject, Qt, Property, Slot

conversationsTableName = "Conversations"

def createTable():

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

class SqlConversationModel(QObject):
    def __init__(self, parent=QSqlTableModel):
        super(SqlConversationModel, self).__init__()
        self.table = QSqlTableModel()
        print('🌈🌈🌈')
        tableExists = self.table.database().tables()
        if(tableExists[0]):
            pass
        else:
            createTable()
        self.table.setTable(conversationsTableName)
        self.table.setSort(2, Qt.DescendingOrder)
        self.table.setEditStrategy(QSqlTableModel.OnManualSubmit)

    def getRecipient(self):
        print('🦊')
        # print(self.recipient)
        return self.recipient

    def setRecipient(self, recipient):
        if recipient == self.recipient:
            pass

        self.recipient = recipient

        filterString = ("(recipient = '{}' AND author = 'Me') OR (recipient = 'Me' AND author='{}')").format(m_recipient)
        setFilter(filterString)
        select()

        emit(recipientChanged())
    recipient = property(getRecipient, setRecipient, str)
        ##there is something wrong here I should check the cpp

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
        # recipient = Property(str, getRecipient, setRecipient)
        print("message: " + message)
        newRecord = self.table.record()
        newRecord.setValue("author", "Me")
        newRecord.setValue("recipient", recipient)
        print("recipient: " + recipient)
        import datetime
        timestamp = datetime.datetime.now()
        newRecord.setValue("timestamp", timestamp)
        # self.message = message
        newRecord.setValue("message", message)
        if not self.table.insertRecord(self.table.rowCount(), newRecord):
            print("Failed to send message:" + lastError().text())
            return
        else:
            print('it worked you 🌸')

        self.table.submitAll()

