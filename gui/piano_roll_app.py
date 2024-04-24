# piano_roll_app.py
import sys
import os
import subprocess
import platform

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from view import Viewer
from menuBar import Menu
from toMidi import MidiConverter
from toString import StringConverter
from newAction import NewAction

import pickle

class Window(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle('MIDI Creation App')
        self.resize(900, 600)
        self.centralWidget = Viewer()
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)
        self.setMenuBar(Menu(self, midi_callback=self.export_midi, tensor_callback=self.save_tensor, new_callback=self.newAction))

    def export_midi(self):
        print("Exporting MIDI...")
        grid = self.centralWidget.scene()
        converter = MidiConverter(grid)
        converter.convert_to_midi("output.mid")
        print("MIDI file has been saved.")
    
    def save_tensor(self):
        print("Saving Tesnor...")
        grid = self.centralWidget.scene()
        converter = StringConverter(grid)
        tensor = converter.extract_string()
        with open('tensor.pkl', 'wb') as f:
            pickle.dump(tensor, f)

    def newAction(self):
        if NewAction.show_confirmation_dialog():
            grid = self.centralWidget.scene()
            grid.clearNotes()
            grid.updateGrid()
        else:
            print("Not Updating!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())