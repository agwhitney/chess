from game_states import Team, switch_teams
from square import Square


class Board:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.squares = self.initialize_squares()

    def initialize_squares(self):
        squares = []

        color = Team.WHITE
        for y in range(self.height):
            column = []
            for x in range(self.width):
                column.append(Square(x, y, color))
                color = switch_teams(color)

            squares.append(column)
            color = switch_teams(color)

        return squares

    def place_pieces(self, pieces):
        """Checks the pieces positions on the board and updates the squares
        Needs work.
        """
        for piece in pieces:
            self.squares[piece.x][piece.y].piece_present = piece
            self.squares[piece.x][piece.y].symbol = piece.symbol
