import sys
from extended_module import XMReader
from module import Pattern
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QSizePolicy, QSlider, QPushButton, QLabel

class Main(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setWindowTitle('OrionTracker')
        self.setGeometry(400, 800, 700, 500)
        self.initUI()
        self.is_playing = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_playback)

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect()

            
        

if __name__ == '__main__':
    mod = XMReader('./amblight.xm')
    mod.load_file()
    pattern = Pattern(mod.header['channel_number'], mod.patterns[0]['row_number'])
    pattern.from_byte_pattern(mod.patterns[0]['data'])
    patterns = []
    for i in pattern.pattern:
        patterns.append(pattern.pattern[i])

    app = QApplication(sys.argv)
    ex = Main(patterns)
    sys.exit(app.exec_())
