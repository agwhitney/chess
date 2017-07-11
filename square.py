from game_states import Team


class Square:
    def __init__(self, x, y, color, piece_present=None):
        self.x = x
        self.y = y
        self.color = color
        self.piece_present = piece_present

        if color == Team.WHITE:
            self.symbol = '[ ]'
        elif color == Team.BLACK:
            self.symbol = '[/]'

    def __repr__(self):
        return "<{} Square at ({}, {})>".format(self.color, self.x, self.y)
