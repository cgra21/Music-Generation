# piano_roll_app.py
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from view import Viewer
from menuBar import Menu
from toMidi import MidiConverter

class Window(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle('MIDI Creation App')
        self.resize(900, 600)
        self.centralWidget = Viewer()
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)
        self.setMenuBar(Menu(self, midi_callback=self.export_midi))

    def export_midi(self):
        print("Exporting MIDI...")
        grid = self.centralWidget.scene()
        converter = MidiConverter(grid)
        converter.convert_to_midi("output.mid")
        print("MIDI file has been saved.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())