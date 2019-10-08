from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide2.QtCore import QObject

conversationsTableName = "Conversations"

def createTable():
    # if(QSqlDatabase.database().tables().contains(conversationsTableName)):
    #     pass

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

# this is basically what I'll have to do but Ill have a function to do that so this is just a sanit thing to keep in minda
# query.exec("INSERT INTO Conversations VALUES('Me', 'Ernest Hemingway', '2016-01-07T14:36:06', 'Hello!')");

class SqlConversationModel(QObject):
    def __init__(self, parent=QSqlTableModel):
        super(SqlConversationModel, self).__init__()
        createTable()
        setTable(conversationsTableName)
        setSort(2, Qt.DescendingOrder)
        setEditStrategy(QSqlTableModel.OnManualSubmit)

    def recipient(self):
        return self.recipient

    def setRecipient(self, recipient):
        if recipient == self.recipient:
            pass

        self.recipient = recipient

        filterString = ("(recipient = '{}' AND author = 'Me') OR (recipient = 'Me' AND author='{}')").format(m_recipient)
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
    
    def sendMessage(self, recipient, message):
        newRecord = record()
        newRecord.setValue("author", "Me")
        newRecord.setValue("recipient", recipient)
        newRecord.setValue("timestamp", timestamp)
        newRecord.setValue("message", message)
        if not insertRecord(rowCount(), newRecord):
            print("Failed to send message:" + lastError().text())
            return

        submitAll()