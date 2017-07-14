from game_states import Team, switch_teams
from square import Square


class Board:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.squares = self.initialize_squares()

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

    def piece_in_square(self, x, y):
        """Returns a piece object present in (x, y); or None."""
        return self.squares[x][y].piece_present
