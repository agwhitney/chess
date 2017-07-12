"""Piece class and the subclasses for each piece, and the initialize_pieces function for placing the
pieces at the beginning of the game.
"""
from game_states import Team


class Piece:
    """Piece object containing properties about the pieces.
    Child classes contain the legal moves; Parent class contains the move function.
    """
    def __init__(self, x, y, color, name, symbol, moves_made=0):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.moves_made = moves_made

        if self.color == Team.BLACK:
            self.symbol = symbol.lower()
        else:
            self.symbol = symbol

    def __repr__(self):
        return "<{} {} ({})>".format(self.color, self.name, self.symbol)

    def move(self, new_x, new_y):
        self.x, self.y = new_x, new_y
        self.moves_made += 1


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


def initialize_pieces():
    pieces = []

    for x in range(8):
        pieces.append(Pawn(x, 1, Team.BLACK))
        pieces.append(Pawn(x, 6, Team.WHITE))

        if x == 0 or x == 7:
            pieces.append(Rook(x, 0, Team.BLACK))
            pieces.append(Rook(x, 7, Team.WHITE))

        if x == 1 or x == 6:
            pieces.append(Knight(x, 0, Team.BLACK))
            pieces.append(Knight(x, 7, Team.WHITE))

        if x == 2 or x == 5:
            pieces.append(Bishop(x, 0, Team.BLACK))
            pieces.append(Bishop(x, 7, Team.WHITE))

        if x == 3:
            pieces.append(Queen(x, 0, Team.BLACK))
            pieces.append(Queen(x, 7, Team.WHITE))

        if x == 4:
            pieces.append(King(x, 0, Team.BLACK))
            pieces.append(King(x, 7, Team.WHITE))

    return pieces
