"""
Piece class and the subclasses for each piece
"""
from game_states import Team


class Piece:
    """Piece object containing properties about the pieces."""
    def __init__(self, x, y, color, name, symbol, moves_made=0):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.moves_made = moves_made

        if self.color == Team.BLACK:
            self.symbol = self.symbol.lower()
        else:
            self.symbol = symbol

    def __repr__(self):
        color = 'Black' if self.color else 'White'
        return "<{} {} ({})>".format(color, self.name, self.symbol)

    def move(self, new_x, new_y):
        self.x, self.y = new_x, new_y


class Pawn(Piece):
    def __init__(self, x, y, color, passant=False):
        super().__init__(x, y, color, 'pawn', '[P]')
        self.passant = passant


class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'rook', '[R]')


class Knight(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'knight', '[N]')


class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'bishop', '[B]')


class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'king', '[K]')


class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'queen', '[Q]')
