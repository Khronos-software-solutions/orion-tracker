import sys
from extended_module import XMReader
from module import Pattern
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget, QLabel

class Main(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setWindowTitle('OrionTracker')
        self.setGeometry(400, 800, 700, 500)

        # Initialize UI components
        self.initUI()

        # Placeholder for playback state
        self.is_playing = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_playback)

    def initUI(self):
        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Play/Pause Button
        self.play_pause_button = QPushButton('Play', self)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        layout.addWidget(self.play_pause_button)

        # Volume Slider
        self.volume_label = QLabel('Volume', self)
        layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)  # Volume range from 0 to 100
        self.volume_slider.setValue(50)  # Default volume at 50%
        layout.addWidget(self.volume_slider)

        # Set layout to central widget
        central_widget.setLayout(layout)

    def toggle_play_pause(self):
        if self.is_playing:
            self.is_playing = False
            self.play_pause_button.setText('Play')
            self.timer.stop()
        else:
            self.is_playing = True
            self.play_pause_button.setText('Pause')
            self.timer.start(100)  # Update playback every 100 ms

    def update_playback(self):
        # Here you would implement the logic to update the playback of the XM file
        # For example, you could read the next pattern and play it
        print("Playing...")  # Placeholder for actual playback logic

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
    ex.show()  # Show the main window
    sys.exit(app.exec_())