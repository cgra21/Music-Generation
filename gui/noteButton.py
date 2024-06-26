from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QApplication, QGraphicsItem
from PyQt5.QtGui import QColor, QBrush, QPainter
from PyQt5.QtCore import QPointF, Qt
import sys

class noteButton(QGraphicsRectItem):
    def __init__(self, x, y, w, h, row, duration=1):
        super().__init__(x, y, w, h)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.setPen(Qt.lightGray)
        self.normalBrush = QBrush(Qt.blue)
        self.setBrush(self.normalBrush)

        self.mousePressOffset = QPointF(0, 0)

        # In order to calculate the note value, we need to add
        # 21 to the row value, since they start at 21
        self.noteValue = 127 - row
        # Dur is just 1 for now, since we only include quarter notes
        self.dur = duration
        self.base_width = w  # Width of a single duration unit
        self.is_resizing_right = False
        self.is_resizing_left = False
        self.moving = False

        self.start_y = y
        self.start_x = self.rect().left()
        self.end_x = self.rect().left() + self.rect().width()

    def hoverMoveEvent(self, event):
        if abs(event.pos().x() - self.rect().right()) < 10:
            self.setCursor(Qt.SizeHorCursor)
        elif abs(event.pos().x() - self.rect().center().x()) < (self.rect().width()-10):
            self.setCursor(Qt.OpenHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if abs(event.pos().x() - self.rect().right()) < 10:
            self.is_resizing_right = True

        elif abs(event.pos().x() - self.rect().center().x()) < (self.rect().width()-10):
            self.moving = True
            self.setCursor(Qt.ClosedHandCursor)
        else:
            self.is_resizing_right = False
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_resizing_right:
            new_width = event.pos().x() - self.rect().left()
            snapped_width = round(new_width / (self.base_width * 0.25)) * (self.base_width * 0.25)
            self.setRect(self.rect().left(), self.rect().top(), snapped_width, self.rect().height())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_resizing_right:
            self.dur = self.rect().width() / self.base_width
            self.is_resizing_right = False
        elif self.moving:
            # print(self.pos().x())
            self.setCursor(Qt.OpenHandCursor)
            self.moving = False
        else:
            super().mouseReleaseEvent(event)

    # TODO FIX SNAPPING ISSUE, HONESTLY NO IDEA WHY SO IT STAYS FOR NOW
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # Constrain the y-coordinate to remain constant, only x-coordinate can change
            increment = self.base_width * 0.25
            snapped_x = round(value.x() / increment) * increment
            # print(snapped_x)
            return QPointF(snapped_x, self.pos().y())
        return super().itemChange(change, value)
    
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