from game_states import Team


class Square:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

        if color == Team.WHITE:
            self.symbol = '[ ]'
        elif color == Team.BLACK:
            self.symbol = '[/]'

    def __repr__(self):
        return "<{} Square at ({}, {})>".format(self.color, self.x, self.y)
