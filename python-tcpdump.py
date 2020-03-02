# Modules imports
import sys
import subprocess

# PyQt5 imports
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# Build pyinstaller .exe
# pyinstaller --onefile --noconsole --paths venv\Lib\site-packages python-tcpdump.py

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
        self.target_text.move(20, 60)
        self.target_text.resize(280,40)

        # Create a text field for the tcpdump filter
        self.tcpdump_filter_text = QLineEdit(self, placeholderText="TCPDUMP filter syntax (auto ignore for tcp port 22 - ssh traffic)")
        self.tcpdump_filter_text.move(20, 100)
        self.tcpdump_filter_text.resize(280,40)

        # Create a text field for the SSH username
        self.username_text = QLineEdit(self, placeholderText="SSH username")
        self.username_text.move(20, 140)
        self.username_text.resize(280,40)

        button = QPushButton('Start tcpdump', self)
        button.setToolTip('Dump all the traffic!')
        button.move(20,220)
        button.resize(280,40)
        button.clicked.connect(self.on_click)
        
        self.show()

    @pyqtSlot()
    def on_click(self):
        jumpbox = self.jumpbox_text.text()
        target = self.target_text.text()
        username = self.username_text.text()
        tcpdump_filter = self.tcpdump_filter_text.text()
        print(tcpdump_filter)
        plinkCommand = [r"C:\Program Files\PuTTY\plink", 
        "-batch", 
        "-proxycmd", 
        r"C:\Program Files\PuTTY\plink "+username+"@"+jumpbox+" -pw test123 -nc "+target+":22", 
        username+"@"+target, 
        "-pw", 
        "test123", 
        r"sudo tcpdump -enni any -l -s 0 -w - not port 22 and "+tcpdump_filter, 
        "|", 
        r'C:\Program Files\Wireshark\Wireshark.exe', "-k", "-i", "-"]
        process = subprocess.Popen(plinkCommand, shell=True)
        stdout, stderr = process.communicate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
