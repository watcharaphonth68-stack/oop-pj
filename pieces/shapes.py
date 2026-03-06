from pieces.piece import Piece
from utils.colors import CYAN, ORIGINAL_YELLOW, PURPLE, ORANGE, BLUE, GREEN, RED

"""
Tetris Standard Rotations (SRS - Super Rotation System style basic shapes)
0 = Empty, 1 = Solid Block
"""

class IPiece(Piece):
    def __init__(self, x, y):
        shape = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        super().__init__(x, y, shape, CYAN)


class OPiece(Piece):
    def __init__(self, x, y):
        # O piece never rotates so a 2x2 shape is sufficient
        shape = [
            [1, 1],
            [1, 1]
        ]
        super().__init__(x, y, shape, ORIGINAL_YELLOW)

    def rotate(self):
        # O piece does not rotate
        pass
        
    def rotate_counter_clockwise(self):
        pass


class TPiece(Piece):
    def __init__(self, x, y):
        shape = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        super().__init__(x, y, shape, PURPLE)


class LPiece(Piece):
    def __init__(self, x, y):
        shape = [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ]
        super().__init__(x, y, shape, ORANGE)


class JPiece(Piece):
    def __init__(self, x, y):
        shape = [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        super().__init__(x, y, shape, BLUE)


class SPiece(Piece):
    def __init__(self, x, y):
        shape = [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ]
        super().__init__(x, y, shape, GREEN)


class ZPiece(Piece):
    def __init__(self, x, y):
        shape = [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ]
        super().__init__(x, y, shape, RED)
