from teams import Team, switch_teams
from square import Square
from itertools import product


class Board:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.key = self.create_key()                # dict(str(alg_coord) : tuple(coordinate))
        self.squares_list = self.initialize_squares()

    def create_key(self):
        """A key for converting algebraic coordinates into cartesian coordinates.
        key['A4'] = (0, 3)]
        """
        key = {}
        letters = [chr(i) for i in range(65, 65 + self.width)]
        numbers = [str(i + 1) for i in range(self.height)]

        cartesian = product(range(self.width), range(self.height))
        algebraic = [l + n for l, n in product(letters, numbers)]

        for alg, car in zip(algebraic, cartesian):
            key[alg] = car

        return key

    def initialize_squares(self):
        """1-D list of square objects"""
        squares = []
        for x in range(self.width):
            for y in range(self.height):
                color = Team.WHITE if (x + y) % 2 else Team.BLACK
                squares.append(Square(x, y, color))
        return squares

    def piece_in_square(self, x, y):
        """Returns the piece in square (x, y), which is None by default.
        Pieces are placed into squares in the draw_board method.
        """
        for square in self.squares_list:
            if square.x == x and square.y == y:
                return square.piece_present

    def square_coordinates(self):
        """Generator of tuples of the square coordinates - useful for looping over.
        Do I use it, though?
        """
        for square in self.squares_list:
            yield (square.x, square.y)

    def square(self, x, y):
        """Returns the SQUARE OBJECT at (x, y)."""
        for square in self.squares_list:
            if square.x == x and square.y == y:
                return square
