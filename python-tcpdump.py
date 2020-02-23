# Modules imports
import sys
import subprocess

# PyQt5 imports
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'tcpdump-buddy'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create a text field for the Jumpbox
        self.jumpbox_text = QLineEdit(self, placeholderText="Jumpbox hostname or IP address")
        self.jumpbox_text.move(20, 20)
        self.jumpbox_text.resize(280,40)

        # Create a text field for the target compute
        self.target_text = QLineEdit(self, placeholderText="Target server to dump")
        self.target_text.move(20, 80)
        self.target_text.resize(280,40)

        # Create a text field for the tcpdump filter
        self.filter_text = QLineEdit(self, placeholderText="TCPDUMP filter syntax (auto ignore for tcp port 22 - ssh traffic)")
        self.filter_text.move(20, 140)
        self.filter_text.resize(280,40)

        button = QPushButton('Start tcpdump', self)
        button.setToolTip('Dump all the traffic!')
        button.resize(280,40)
        button.move(20,200)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        process = subprocess.Popen(['wireshark'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())