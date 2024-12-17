import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QPlainTextEdit,
    QComboBox,
    QMessageBox, 
    QScrollArea)
from PyQt5.QtGui import QPixmap
from pathlib import Path
from playsound import playsound
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])

        # Sends the current index (position) of the selected item.
        widget.currentIndexChanged.connect( self.index_changed )

        # There is an alternate signal to send the text.
        widget.currentTextChanged.connect( self.text_changed )

        self.setCentralWidget(widget)

    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        print(s)

app = QApplication(sys.argv)
win = QMainWindow()
win.show()
sys.exit(app.exec_())