class Piece:
    def __init__(self, x, y, shape, color):
        """
        Initialize a new Tetris piece.
        :param x: Initial X position (column on the board)
        :param y: Initial Y position (row on the board)
        :param shape: 2D list representing the piece's shape
        :param color: RGB tuple for the piece's color
        """
        self._x = x
        self._y = y
        self._shape = shape
        self._color = color

    # Properties (Encapsulation)
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def shape(self):
        return self._shape

    @property
    def color(self):
        return self._color

    # Movement Methods
    def move_left(self):
        self._x -= 1

    def move_right(self):
        self._x += 1

    def move_down(self):
        self._y += 1

    def move(self, dx, dy):
        """Move by a specific delta x and delta y"""
        self._x += dx
        self._y += dy

    # Rotation Method
    def rotate(self):
        """
        Rotate the piece 90 degrees clockwise.
        Uses matrix transposition and reversal.
        """
        # Example of rotating a 2D matrix 90 degrees clockwise
        self._shape = [list(row) for row in zip(*self._shape[::-1])]

    def rotate_counter_clockwise(self):
        """
        Rotate the piece 90 degrees counter-clockwise.
        """
        # Example of rotating a 2D matrix 90 degrees counter-clockwise
        self._shape = [list(row)[::-1] for row in zip(*self._shape)]
