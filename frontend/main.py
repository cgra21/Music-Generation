import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRectF

from note import PianoRollScene

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Piano Roll Editor")
        self.setGeometry(100, 100, 800, 600)

        # Initialize the piano roll scene with interaction capabilities
        self.scene = PianoRollScene()
        self.scene.setSceneRect(0, 0, 1000, 500)

        # Setup view
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, 780, 580)
        self.setCentralWidget(self.view)

        self.init_grid()

    def init_grid(self):
        # Example grid initialization (this would be more complex in a full implementation)
        for i in range(0, 1000, 40):  # Example spacing
            self.scene.addLine(i, 0, i, 500)  # Vertical lines
        for j in range(0, 500, 20):  # Example spacing
            self.scene.addLine(0, j, 1000, j)  # Horizontal lines

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
