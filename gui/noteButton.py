from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QApplication, QGraphicsItem
from PyQt5.QtGui import QColor, QBrush, QPainter
from PyQt5.QtCore import Qt
import sys

class noteButton(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setPen(Qt.lightGray)
        self.normalBrush = QBrush(Qt.white)
        self.hoverBrush = QBrush(QColor(93, 226, 231))
        self.clickedBrush = QBrush(Qt.blue)
        self.setBrush(self.normalBrush)
        self.isClicked = False

    def hoverEnterEvent(self, event):
        # Only change to hover color if the item hasn't been clicked
        if self.brush() != self.clickedBrush:
            self.setBrush(self.hoverBrush)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Only revert to normal color if the item hasn't been clicked
        if self.brush() != self.clickedBrush:
            self.setBrush(self.normalBrush)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        self.isClicked = not self.isClicked  # Toggle the clicked state
        if self.isClicked:
            self.setBrush(self.clickedBrush)  # Change to clicked color
        else:
            self.setBrush(self.normalBrush)  # Revert to normal color
        super().mousePressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)

    # Create and add a custom rectangle item to the scene
    rectItem = noteButton(0, 0, 100, 100)
    scene.addItem(rectItem)

    view.show()
    sys.exit(app.exec_())