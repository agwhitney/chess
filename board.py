from game_states import Team, switch_teams
from square import Square
from itertools import product


class Board:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.squares = self.initialize_squares()    # list of tuple coordinates
        self.key = self.create_key()                # dict(str(alg_coord) : tuple(coordinate))

    def initialize_squares(self):
        """Returns width * height nested list of squares.
        Loop x then y because it will be called as squares[x][y].
        """
        squares = []

        color = Team.WHITE
        for x in range(self.width):
            columns = []
            for y in range(self.height):
                columns.append(Square(x, y, color))
                color = switch_teams(color)

            squares.append(columns)
            color = switch_teams(color)

        return squares

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

    def piece_in_square(self, x, y):
        """Returns a piece object present in (x, y); or None."""
        return self.squares[x][y].piece_present
