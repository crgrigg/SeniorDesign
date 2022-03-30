from time import sleep
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('PyQt5 App')
window.setGeometry(100,200,280,80)
window.move(60,15)

helloMsg = QLabel('<h1>Hello World!</h1>',parent=window)
helloMsg.move(60,15)

window.show()
sleep(10)

sys.exit(app.exec_())