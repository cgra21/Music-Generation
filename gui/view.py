from PyQt5.QtWidgets import QGraphicsView
from piano_roll_grid import PianoRollGrid
from PyQt5.QtCore import Qt


class Viewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(PianoRollGrid(88, 20, 50, 20))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)