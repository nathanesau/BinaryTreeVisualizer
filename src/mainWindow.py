from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qrc_resources # pyrcc5 resources.qrc -o qrc_resources.py

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.treeWidget = QLabel()
        self.setCentralWidget(self.treeWidget)
        self.setWindowTitle("Binary Tree Visualizer")
        self.setWindowIcon(QIcon(":icon.png"))
    
    def addPixmap(self, pixmap):
        self.treeWidget.setPixmap(pixmap)
        self.treeWidget.show()