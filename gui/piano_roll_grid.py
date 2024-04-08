# piano_roll_grid.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor

import sys
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import Qt
from noteButton import noteButton

class PianoRollGrid(QGraphicsScene):
    def __init__(self, rows, cols, x_size, y_size) -> None:
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.x_size = x_size
        self.y_size = y_size
        self.key_width = x_size
        self.setSceneRect(0, 0, cols * x_size + self.key_width, rows * y_size)
        self.initUI()

    def initUI(self):
        for i in range(self.rows):
            y = i * self.y_size
            key = QGraphicsRectItem(0, y, self.key_width, self.y_size)
            if (i % 12) in [1, 3, 6, 8, 10]:  
                key.setBrush(QColor('black'))
            else:
                key.setBrush(QColor('white'))
            self.addItem(key)


        # Create the grid of rectangles
        for i in range(self.rows):
            for j in range(self.cols):
                # Calculate position
                x = j * self.x_size + self.key_width
                y = i * self.y_size
                
                # Create a rectangle item and add it to the scene
                rect = noteButton(x, y, self.x_size, self.y_size)
                self.addItem(rect)
                
        dark_pen = QPen(Qt.darkGray)
        dark_pen.setWidth(2)  # Optional: Make the line thicker for visibility
        for j in range(self.cols):
            if j % 4 == 0:  # Every 4th column
                x = j * self.x_size + self.key_width
                self.addLine(x, 0, x, self.rows * self.y_size, dark_pen)

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    grid = PianoRollGrid(50, 50, 50, 20)  
    grid.run()

