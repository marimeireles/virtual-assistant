from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide2.QtCore import Signal, QUrl, Qt

#all of this needs to be inside a box with a scroll mode

class Dialog(QWidget):
    def __init__(self):
        super(Dialog, self).__init__()
        self.chatLayout = QVBoxLayout()

        self.userLayout = QVBoxLayout()
        self.machineLayout = QVBoxLayout()

        self.chatLayout.addLayout(self.userLayout)
        self.chatLayout.addLayout(self.machineLayout)

        self.userText = ""
        self.machineText = ""

        self.userLayout.setAlignment(Qt.AlignRight)
        self.machineLayout.setAlignment(Qt.AlignLeft)

        self.setLayout(self.chatLayout)


    def showUserMessage(self):
        self.userQLabel = QLabel()
        self.userQLabel.setText(self.userText)

        self.userLayout.addWidget(self.userQLabel)


        import requests

        headers = {
            'Content-type': 'application/json',
        }

        data = "{\"sender\": \"user1\", \"message\": \" " + self.userText + " hello\"}"

        response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)

        # r = requests.get(url = 'http://localhost:5005/') 
        print(response.text)
        # print(r.text)
        print('🌸')

    def setUserMessage(self, string):
        self.userText = string

    def getUserMessage(self):
        return self.userText

    def showMachineMessage():
        pass


