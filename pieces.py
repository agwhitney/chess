"""Piece class and the subclasses for each piece, and the initialize_pieces function for placing the
pieces at the beginning of the game.
"""
from game_states import Team
from cast_ray import cardinals, ordinals, radial, step


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
        return "<{} {} at ({}, {})>".format(self.color, self.name, self.x, self.y)


class Pawn(Piece):
    def __init__(self, x, y, color, passant=False):
        super().__init__(x, y, color, 'Pawn', '[P]')
        self.passant = passant

    def legal_moves(self, board):
        legal_squares = []

        if self.color == Team.BLACK:
            legal_squares.append(step(self.x, self.y, 'south'))

        elif self.color == Team.WHITE:
            legal_squares.append(step(self.x, self.y, 'north'))

        return legal_squares


class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'Rook', '[R]')

    def legal_moves(self, board):
        return cardinals(self, board)


class Knight(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'Knight', '[N]')

    def legal_moves(self, board):
        legal_squares = [
            (self.x + 2, self.y + 1),
            (self.x + 2, self.y - 1),
            (self.x - 2, self.y + 1),
            (self.x - 2, self.y - 1),
            (self.x + 1, self.y + 2),
            (self.x - 1, self.y + 2),
            (self.x + 1, self.y - 2),
            (self.x - 1, self.y - 2)
        ]
        return legal_squares


class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'Bishop', '[B]')

    def legal_moves(self, board):
        return ordinals(self, board)


class King(Piece):
    def __init__(self, x, y, color, checked=False):
        super().__init__(x, y, color, 'King', '[K]')
        self.checked = checked

    def legal_moves(self, board):
        pass


class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'Queen', '[Q]')

    def legal_moves(self, board):
        return radial(self, board)


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
