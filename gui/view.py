from PyQt5.QtWidgets import QGraphicsView
from piano_roll_grid import PianoRollGrid
from PyQt5.QtCore import Qt


class Viewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(PianoRollGrid(107, 20, 100, 40))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)