import random
from pieces.shapes import IPiece, OPiece, TPiece, LPiece, JPiece, SPiece, ZPiece

class PieceFactory:
    """
    Factory Pattern for creating random Tetromino pieces.
    """
    
    # List of all available piece classes
    _PIECE_CLASSES = [IPiece, OPiece, TPiece, LPiece, JPiece, SPiece, ZPiece]

    @staticmethod
    def create_random_piece(x, y):
        """
        Creates and returns a random Tetromino piece at the specified coordinates.
        
        :param x: Initial X position (column)
        :param y: Initial Y position (row)
        :return: An instance of a Piece subclass
        """
        # Select a random class from the list
        piece_class = random.choice(PieceFactory._PIECE_CLASSES)
        
        # Instantiate and return the chosen piece
        return piece_class(x, y)
