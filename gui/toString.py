from piano_roll_grid import PianoRollGrid
from PyQt5.QtWidgets import QGraphicsScene

def toString(grid: QGraphicsScene) -> str:
    '''
    Method used to convert the exisitng noteButton grid into a string
    this will be the string we use for the model
    
    Usage:
        '''
    grid.items


if __name__ == '__main__':
    grid = PianoRollGrid(106, 8, 50, 20)
