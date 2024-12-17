import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QPlainTextEdit,
    QMessageBox, 
    QScrollArea)
from PyQt5.QtGui import QPixmap
from pathlib import Path
from playsound import playsound
import requests
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

def fire_message(message, x, y):
    msg_box = QMessageBox() 
    msg_box.setIcon(QMessageBox.Information) 
    msg_box.setText(message)
    msg_box.setWindowTitle("Info!")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.move(x, y)
    msg_box.exec_()

def homepage_pixelmap_factory():
    image_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"  # Example URL
    response = requests.get(image_url, stream=True)
    response.raise_for_status()  
    image_data = response.content
    pixmap = QPixmap()
    pixmap.loadFromData(image_data)
    return pixmap

class QMainWindows(QWidget):
    title = "Conceptor"
    WIDTH  = 245
    HEIGHT = 321
    
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv("data.csv")
        self.setWindowTitle(self.title)
        self.move(300, 300)
        self.resize(self.WIDTH, self.HEIGHT)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        ######### COMPONENTS ##############
        self.input   = QLineEdit()
        self.dropdown = QComboBox()
        self.desc  = QPlainTextEdit()
        self.submit = QPushButton("SAVE")

        ######### ADD WIDGETS ##########
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.desc)
        self.layout.addWidget(self.submit)

        ######### LISTENERS ##########
        self.submit.clicked.connect(self.on_submit_click)
        self.input.textChanged.connect(self.on_text_changed) 

    def suggestion(self):
        print("asd")

    def on_submit_click(self):
        concept = self.input.text()
        description = self.desc.toPlainText()
        if not concept or not description:
            fire_message("Fields are empty", self.x, self.y)
            return
        new_row = [concept, description]
        self.df.loc[len(self.df)] = new_row 
        self.df.to_csv('data.csv', index=False)
        playsound("repo/bing.mp4")
        self.input.clear()
        self.desc.clear()
        
    def on_text_changed(self):
        current_concept = self.input.text()
        concepts = self.df["concept"]
        recommendation_set = [c for c in concepts if c.startswith(current_concept)]
        if len(recommendation_set) > 3:
            recommendation_set = recommendation_set[0:3]
        self.dropdown.clear()
        self.dropdown.addItems(recommendation_set)
        self.dropdown.showPopup()

    def moveEvent(self, event):
        new_pos = event.pos()
        self.x, self.y = new_pos.x(), new_pos.y()
        super().moveEvent(event) 

    def resizeEvent(self, event):
        new_size = self.size() 
        self.WIDTH = new_size.width()
        self.HEIGHT = new_size.height()
        print(f"Window resized to width: {self.WIDTH}, height: {self.HEIGHT}")

    def scale_window(self, factor):
        geometry = self.geometry()
        self.WIDTH = geometry.width() * factor
        self.HEIGHT = geometry.height() * factor
        self.resize(self.HEIGHT, self.WIDTH)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindows()
    win.show()
    sys.exit(app.exec_())