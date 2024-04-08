import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import Qt

class PianoRollGrid(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.grid_size = 20  # Example grid size

        # Draw grid lines for illustration (optional)
        for i in range(0, 400, self.grid_size):
            self.scene.addLine(i, 0, i, 400)
            self.scene.addLine(0, i, 400, i)

    def mousePressEvent(self, event):
        # Calculate grid cell
        x = (event.x() // self.grid_size) * self.grid_size
        y = (event.y() // self.grid_size) * self.grid_size

        # Add a note rectangle
        self.addNote(x, y)

    def addNote(self, x, y):
        # This adds a rectangle representing a note; customize as needed
        rect = QGraphicsRectItem(x, y, self.grid_size, self.grid_size)
        rect.setBrush(Qt.blue)
        self.scene.addItem(rect)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PianoRollGrid()
    window.show()
    sys.exit(app.exec_())
