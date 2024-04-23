# piano_roll_grid.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor

import sys
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItemGroup
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

        self.note_buttons = []

        self.setSceneRect(0, 0, cols * x_size + self.key_width, rows * y_size)
        self.updateGrid(self.rows, self.cols, initial_setup=True)

    def updateGrid(self, rows, cols, initial_setup=False):
        self.rows = rows
        for i in range(self.rows):
            y = i * self.y_size

            if ((i + 21) % 12) in [1,3,6,8,10]:
                bg_color = QColor('lightblue')  # Background color for black keys
            else:
                bg_color = QColor('white')  # Background color for white keys

            # Create a full-width background rectangle for each row
            bg_rect = QGraphicsRectItem(0, y, self.cols * self.x_size + self.key_width, self.y_size)
            bg_rect.setBrush(bg_color)
            bg_rect.setPen(QPen(Qt.NoPen))
            self.addItem(bg_rect)   


            key = QGraphicsRectItem(0, y, self.key_width, self.y_size)
            if ((i+21) % 12) in [1, 3, 6, 8, 10]:  
                key.setBrush(QColor('black'))
            else:
                key.setBrush(QColor('white'))
            self.addItem(key)
        
        self.drawMeasures(cols)
        self.drawHorizontalLines()

    def mouseDoubleClickEvent(self, event):
        x = event.scenePos().x() - self.key_width
        y = event.scenePos().y()
        if x >= 0:  # Ensure clicks are within the grid area past the key width
            col = int(x // self.x_size)
            row = int(y // self.y_size)
            if 0 <= col < self.cols and 0 <= row < self.rows:
                self.addNoteButton(row, col)
                

            
    def drawMeasures(self, cols):
        dark_pen = QPen(Qt.darkGray)
        dark_pen.setWidth(2)  # Optional: Make the line thicker for visibility
        for j in range(cols):
            if j % 4 == 0:  # Every 4th column
                x = j * self.x_size + self.key_width
                self.addLine(x, 0, x, self.rows * self.y_size, dark_pen)
        light_pen = QPen(QColor(140, 233, 236))
        light_pen.setWidth(1)
        for j in range(cols):
            if j % 4 != 0:
                x = j * self.x_size + self.key_width
                self.addLine(x, 0, x, self.rows * self.y_size, light_pen)
    
    def drawHorizontalLines(self):
        light_pen = QPen(QColor(140, 233, 236))
        for i in range(self.rows):
            y = i * self.y_size
            # Draw a line from the right edge of the keys to the end of the scene
            self.addLine(self.key_width, y, self.width(), y, light_pen)

    def addNoteButton(self, row_index, col_index):
        x = col_index * self.x_size + self.key_width
        y = row_index * self.y_size
        button = noteButton(x, y, self.x_size, self.y_size, row_index)
        self.addItem(button)
        self.note_buttons.append(button)
        return button
    
    def addColumn(self):
        # TODO
        pass

    def delColumn(self):
        # TODO
        pass

    def get_note_buttons(self):
        return self.note_buttons
    

if __name__ == '__main__':
    grid = PianoRollGrid(50, 50, 50, 20)  
    grid.run()



        # if initial_setup:
        #     # Create the grid of rectangles
        #     for j in range(cols):
        #         col_buttons = []
        #         for i in range(rows):
        #             col_buttons.append(self.addNoteButton(i, j))
        #         self.note_buttons.append(col_buttons)
        #     self.drawLine(cols)
        # else:
        #     # Adjust columns dynamically
        #     current_cols = len(self.note_buttons)
        #     if cols > current_cols:
        #         # Add new columns
        #         for j in range(current_cols, cols):
        #             column_buttons = []
        #             for i in range(rows):
        #                 column_buttons.append(self.addNoteButton(i, j))
        #             self.note_buttons.append(column_buttons)
        #         self.drawLine(cols)
        #     elif cols < current_cols:
        #         # Remove excess columns
        #         for j in range(cols, current_cols):
        #             column_to_remove = self.note_buttons.pop()
        #             for item in column_to_remove:
        #                 self.removeItem(item)
