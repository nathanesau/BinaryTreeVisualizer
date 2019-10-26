import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from bst import BST
from mainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # example (todo: allow user to interactively create nodes)
    a = BST()
    a.insert(7)
    a.insert(6)
    a.insert(10)
    a.insert(3)
    a.insert(4)
    a.insert(5)
    a.insert(8)
    a.insert(12)
    a.insert(9)
    a.deleteNode(7)
    pixmap = a.getPixmap()
    
    mainWindow = MainWindow()
    mainWindow.addPixmap(pixmap) # show pixmap
    mainWindow.show()

    app.exec()