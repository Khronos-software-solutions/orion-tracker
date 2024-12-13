import sys
from extended_module import XMReader
from module import Pattern
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QSizePolicy

class Main(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()  
        scroll = QScrollArea()
        # Create a grid layout
        grid = QGridLayout()

        # Define the table data

        # Add the data to the grid layout
        for row_idx, row in enumerate(self.data):
            for col_idx, item in enumerate(row):
                label = QLineEdit(str(item))
                label.setFont(QFont("Courier New", 10))
                label.setContentsMargins(0, 0, 0, 0)
                label.setTextMargins(0, 0, 0, 0)
                label.setStyleSheet("border: 1px solid black; padding: 2px;")
                grid.addWidget(label, col_idx, row_idx)

        # Set the grid layout to the main layout

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setLayout(grid)
        scroll.setContentsMargins(0,0,0,0)
        self.vbox.addWidget(scroll)
        wid = QWidget()
        wid.setLayout(self.vbox)
        self.setCentralWidget(wid)
        
        self.setWindowTitle('Orion tracker')
        self.show()

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
