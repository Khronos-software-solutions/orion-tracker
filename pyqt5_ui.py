import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class OpenMPTTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenMPT-like Table")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and set a layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create a table widget
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(16)  # Number of tracks
        self.table_widget.setColumnCount(64)  # Number of beats/steps

        # Set the table headers
        self.table_widget.setHorizontalHeaderLabels([f"{i}" for i in range(64)])
        self.table_widget.setVerticalHeaderLabels([f"Channel {i+1}" for i in range(16)])

        # Populate the table with empty items
        for row in range(16):
            for col in range(64):
                self.table_widget.setItem(row, col, QTableWidgetItem(""))

        # Add the table widget to the layout
        layout.addWidget(self.table_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenMPTTable()
    window.show()
    sys.exit(app.exec_())
