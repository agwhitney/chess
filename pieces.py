"""Piece class and the subclasses for each piece, and the initialize_pieces function for placing the
pieces at the beginning of the game.
"""
from teams import Team
from cast_ray import cardinals, ordinals, radial, step


class Piece:
    """Piece object containing properties about the pieces.
    Child classes contain the legal moves; Parent class contains the move function.
    """
    def __init__(self, x, y, color, name, symbol, moves_made=0, captured=False):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.moves_made = moves_made
        self.captured = captured

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

    def legal_moves(self, board, only_diagonals=False):
        legal_squares = []
        forward = 'north' if self.color == Team.WHITE else 'south'

        # Forward Step
        one_step = step(self.x, self.y, forward)
        if not board.piece_in_square(one_step[0], one_step[1]):
            legal_squares.append(one_step)

        # First Turn Two-Step
        if self.moves_made == 0:
            two_step = step(one_step[0], one_step[1], forward)
            legal_squares.append(two_step)
            self.passant = True

        # Diagonal Captures, including Passant Captures
        for side in ['east', 'west']:
            # Diagonal
            diagonal = step(self.x, self.y, forward + side)
            target_dgnl = board.piece_in_square(diagonal[0], diagonal[1])
            if target_dgnl:
                if target_dgnl.color != self.color:
                    legal_squares.append(diagonal)

            # Passant
            lateral = step(self.x, self.y, side)
            target_lat = board.piece_in_square(lateral[0], lateral[1])
            if target_lat:
                if target_lat.name == 'Pawn' and target_lat.passant is True and target_lat.color != self.color:
                    legal_squares.append(diagonal)
                    target_lat.captured = True

        # Remove non-diagonal squares (used for check checking)
        if only_diagonals is True:
            for square in legal_squares:
                if square[1] == self.y:
                    legal_squares.remove(square)

        return legal_squares

    # def promote(self, pieces):
    #     """Removes this piece and replaces it with a desired piece.
    #     Desired piece is a queen right now no matter what, but who doesn't want a queen?
    #     What are they gonna have instead? A knight? Might as well just have another king
    #     since they're probably gonna lose anyway.
    #     """


class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'Rook', '[R]')

    def legal_moves(self, board):
        return cardinals(self, board)


class Knight(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'Knight', '[N]')

    def legal_moves(self, board):
        """Legal squares determined by taking all the options as a list, then removing options
        as necessary (i.e. not in board or team-occupied) and returning a new list.
        """
        potential_squares = [
            (self.x + 2, self.y + 1),
            (self.x + 2, self.y - 1),
            (self.x - 2, self.y + 1),
            (self.x - 2, self.y - 1),
            (self.x + 1, self.y + 2),
            (self.x - 1, self.y + 2),
            (self.x + 1, self.y - 2),
            (self.x - 1, self.y - 2)
        ]
        legal_squares = []
        for square in potential_squares:
            target = board.piece_in_square(square[0], square[1])
            if target:
                if target.color != self.color:
                    legal_squares.append(square)

            if square in board.square_coordinates():
                legal_squares.append(square)

        return legal_squares


class Bishop(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'Bishop', '[B]')

    def legal_moves(self, board):
        return ordinals(self, board)


class King(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'King', '[K]')

    def legal_moves(self, board):
        """Added explicitly then removed as appropriate.
        Checks are (will be) determined at the end of a turn in a separate place
        """
        potential_squares = [
            step(self.x, self.y, 'north'),
            step(self.x, self.y, 'south'),
            step(self.x, self.y, 'east'),
            step(self.x, self.y, 'west'),
            step(self.x, self.y, 'northeast'),
            step(self.x, self.y, 'northwest'),
            step(self.x, self.y, 'southeast'),
            step(self.x, self.y, 'southwest'),
        ]
        legal_squares = []
        for square in potential_squares:
            target = board.piece_in_square(square[0], square[1])
            if target:
                if self.color != target.color:
                    legal_squares.append(square)

            if square in board.square_coordinates():
                legal_squares.append(square)

        return legal_squares

    def in_check(self, board, pieces):
        """Checks whether or not a king is in check at its position by creating a list of dangerous squares
        and seeing if the king is in them.
        """
        danger_zone = []
        for piece in pieces:
            if piece.color == self.color:
                continue

            if piece.name == 'Pawn':
                danger_zone.extend(piece.legal_moves(board, only_diagonals=True))

            else:
                danger_zone.extend(piece.legal_moves(board))

        if (self.x, self.y) in danger_zone:
            return True


class Queen(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color, 'Queen', '[Q]')

    def legal_moves(self, board):
        return radial(self, board)


# Utilities
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


def return_king(pieces, player_turn):
    """Returns the player's king"""
    for piece in pieces:
        if piece.color == player_turn and piece.name == 'King':
            return piece
