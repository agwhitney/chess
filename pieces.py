"""
Piece class and the subclasses for each piece
"""

class Piece:
    """Piece object containing properties about the pieces."""
    def __init__(self, y, x, color, name, symbol, count=0):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.symbol = symbol
        self.count = count

        if self.color:
            self.symbol = self.symbol.lower()

    def __repr__(self):
        color = 'Black' if self.color else 'White'
        return "<{} {} ({})>".format(color, self.name, self.symbol)


class Pawn(Piece):
    def __init__(self, y, x, color, passant=False):
        super().__init__(y, x, color, 'pawn', 'P')
        self.passant = passant


class Rook(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color, 'rook', 'R')


class Knight(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color, 'knight', 'N')


class Bishop(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color, 'bishop', 'B')


class King(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color, 'king', 'K')


class Queen(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color, 'queen', 'Q')
