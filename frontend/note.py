from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class NoteItem(QGraphicsRectItem):
    def __init__(self, pitch, start_time, duration, x, y, width, height):
        super().__init__(x, y, width * duration, height)
        self.setBrush(QColor(150, 20, 120))  # A distinct color for the note
        self.setFlag(QGraphicsRectItem.ItemIsMovable, False)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)

class PianoRollScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Calculate grid position and create a new note
            x = int(event.scenePos().x()) // 40 * 40  # Snap to grid
            y = int(event.scenePos().y()) // 20 * 20
            note = NoteItem(pitch=y//20, start_time=x//40, duration=1, x=x, y=y, width=40, height=20)
            self.addItem(note)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # Implement more complex interactions like resizing if needed
