import sys
from PySide2.QtWidgets import *
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

from mainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.showMaximized();
    widget.show()

    sys.exit(app.exec_())