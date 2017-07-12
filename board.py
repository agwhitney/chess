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
            for x in range(self.width):
                squares.append(Square(x, y, color))
                color = switch_teams(color)

            color = switch_teams(color)

        return squares
