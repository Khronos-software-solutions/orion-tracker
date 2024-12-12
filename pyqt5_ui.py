import sys
from extended_module import XMReader
from module import Pattern
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout

class TableWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        # Create a grid layout
        grid = QGridLayout()

        # Define the table data

        # Add the data to the grid layout
        for row_idx, row in enumerate(self.data):
            for col_idx, item in enumerate(row):
                label = QLabel(str(item))
                label.setStyleSheet("border: 1px solid black; padding: 5px;")
                grid.addWidget(label, row_idx, col_idx)

        # Set the grid layout to the main layout
        self.setLayout(grid)

        self.setWindowTitle('Table using QLabel')
        self.show()

if __name__ == '__main__':
    mod = XMReader('./amblight.xm')
    mod.load_file()
    pattern = Pattern(mod.header['channel_number'], mod.patterns[0]['row_number'])
    patterns = []
    for i in pattern.pattern:
        patterns.append(pattern.pattern[i])

    app = QApplication(sys.argv)
    ex = TableWidget(patterns)
    sys.exit(app.exec_())
