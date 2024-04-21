# main.py
import sys
from PyQt5.QtWidgets import QApplication
from piano_roll_app import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
