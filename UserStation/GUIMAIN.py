from time import sleep
import sys

import VidThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel


def MyApplication():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle('PyQt5 App')
    window.setGeometry(1000,1600,1500,800)
    window.move(50,50)

    Btn1 = QPushButton("Auto")
    Btn1.
   
    Video = QLabel(parent=window)
    Video.setGeometry(800,800,800,800)
    Video.setText("Hello World")

    MyLayout = QVBoxLayout()
    MyLayout.addWidget(Btn1)
    
    MyLayout.addWidget(Video)


    window.setLayout(MyLayout)
    window.show()
    sleep(10)
    sys.exit(app.exec_())

MyApplication()