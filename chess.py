"""Chess v2
Because things were getting a little out of hand in v1
Still trying to make Chess
"""

import copy
import pprint
pp = pprint.PrettyPrinter(indent=4)

CARDINALS = ['up', 'down', 'left', 'right']
ORDINALS = ['up-left', 'up-right', 'down-left', 'down-right']
BS = [(10, 10), None, None]     # Bullshit coordinate - spoof square to catch exceptions with board.step
# Functionally, if it steps outside the board it will move here. Matches the format of board.square


class Piece:
    """Piece object containing properties about the pieces."""
    def __init__(self, color, name, symbol, count=0):
        self.color = color
        self.name = name
        self.symbol = symbol
        self.count = count

        if self.color == 'black':
            self.symbol = self.symbol.lower()

    def __repr__(self):
        return "<{} {} ({})>".format(self.color, self.name, self.symbol)

    def friend_check(self, board, position):
        """Checks the color of self vs. the color of a piece in (position), using the board.piece_in() function
        Returns True if the two pieces are FRIENDLY, so if not friend_check() implies an enemy.
        """
        try:
            ufo = board.piece_in(position)
            friend = True if ufo.color == self.color else False
        except (AttributeError, KeyError):  # Catch if there's no piece in that position or if it's not in board
            friend = False
        return friend


class Pawn(Piece):
    def __init__(self, color, passant=False):
        Piece.__init__(self, color, 'pawn', 'P')
        self.passant = passant

    def legal_moves(self, board, start):
        moves = []
        forward = 'up' if self.color == 'white' else 'down'
        # One step
        step = board.step(start, forward, n=1)
        if not board.piece_in(step):
            moves.append(step)
        # Two step
        step = board.step(start, forward, n=2)
        if not board.piece_in(step) and self.count == 0:
            moves.append(step)
        # Capture step
        for direction in ['left', 'right']:
            step = board.step(start, forward+'-'+direction, n=1)
            if not self.friend_check(board, step):
                moves.append(step)
        # Passant step
        for direction in ['left', 'right']:
            step = board.step(start, direction, n=1)
            side = board.piece_in(step)
            if side:
                if side.name == 'pawn' and side.color != self.color:
                    if side.passant is True and side.count == 1:
                        moves.append(forward+'-'+direction)     # TODO How to remove the passant-ed pawn?
                        #  TODO Set pawn's passant flag when it passants
        return moves


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'rook', 'R')

    def legal_moves(self, board, start):
        moves = []
        for direction in CARDINALS:
            moves.extend(board.cast_ray(start, direction))
        print(moves)
        return moves


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'knight', 'N')

    def legal_moves(self, board, start):
        moves = []
        for direction in ORDINALS:  # Move gathered in two steps: a diagonal step, and then a step with a diagonal comp.
            first = board.step(start, direction)    # eg an 'up-right' step followed by...
            move_one = board.step(first, direction.split('-')[0])   # ... an 'up' step...
            move_two = board.step(first, direction.split('-')[1])   # ... and a 'right' step
            if not self.friend_check(board, move_one):
                moves.append(move_one)
            if not self.friend_check(board, move_two):
                moves.append(move_two)
        return moves


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'bishop', 'B')

    def legal_moves(self, board, start):
        moves = []
        for direction in ORDINALS:
            moves.extend(board.cast_ray(start, direction))
        return moves


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'king', 'K')

    def legal_moves(self, board, start):
        # TODO Checking for checking and disallowing self checking
        moves = []
        for direction in CARDINALS + ORDINALS:
            step = board.step(start, direction)
            if not board.piece_in(step):
                moves.append(step)
            elif not self.friend_check(board, start):
                moves.append(step)
            else:
                pass
        return moves


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'queen', 'Q')

    def legal_moves(self, board, start):
        moves = []
        for direction in CARDINALS + ORDINALS:
            moves.extend(board.cast_ray(start, direction))
        return moves


class Board:
    """Has info about the board and controls all that occurs atop it."""
    def __init__(self):
        """Creates a board object
        board = 9x9 list (visual; Piece symbols are placed on top)
        square = dictionary: tuple to list(string, string, object/None)
        key = dictionary: string to tuple
        """
        self.board = []  # Visual presentation
        self.square = {}  # Maps square (cartesian) to metadata (algCoord, color, piece present)
        self.key = {}  # Maps algebraic(string) to cartesian coordinates(tuple)
        self.player = {1: 'white', -1: 'black'}   # Used for turns and checking teams

        self._create_board()
        self._place_pieces()

    def _create_board(self):
        """Creates the empty checkered board."""
        count = 0  # For the checker pattern
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for letter in letters:  # Denotes row
            row = []
            count += 1  # Checker, not stripe
            for number in range(8):  # Denotes column
                count += 1
                coord_alg = '{}{}'.format(letter, number + 1)
                if count % 2 == 0:
                    color = 'white'
                    row.append('[ ]')  # White
                else:
                    color = 'black'
                    row.append('[/]')  # Black
                self.key[coord_alg] = (letters.index(letter) + 1, number + 1)
                self.square[(letters.index(letter) + 1, number + 1)] = [coord_alg, color, None]
            self.board.append(row)

        # Append the reference row and column
        # Bonus: Now the coordinates fit: (1,1) on the board is actually [1,1]
        self.board.insert(0, [' {} '.format(i) for i in range(9)])
        for row in self.board[1:]:
            row.insert(0, ' {} '.format(letters[self.board.index(row) - 1]))

    def _place_pieces(self):
        # Pawns
        for i in range(1, 9):
            self.square[(2, i)][2] = Pawn('black')
            self.square[(7, i)][2] = Pawn('white')
        # Rooks
        for col in [1, 8]:
            self.square[(1, col)][2] = Rook('black')
            self.square[(8, col)][2] = Rook('white')
        # Knights
        for col in [2, 7]:
            self.square[(1, col)][2] = Knight('black')
            self.square[(8, col)][2] = Knight('white')
        # Bishops
        for col in [3, 6]:
            self.square[(1, col)][2] = Bishop('black')
            self.square[(8, col)][2] = Bishop('white')
        # Queens
        self.square[(1, 4)][2] = Queen('black')
        self.square[(8, 4)][2] = Queen('white')
        # Kings
        self.square[(1, 5)][2] = King('black')
        self.square[(8, 5)][2] = King('white')

        self.draw_board()

    def draw_board(self):
        """Goes through self.square and draws the present pieces on their square, then prints the board.
        Doesn't change self.board - just uses it as a clean sheet each time.
        Doesn't return anything - just prints the updated board
        """
        board = copy.deepcopy(self.board)    # Deep copy of the empty board, keeping the original intact
        for coord in self.square:
            piece = self.piece_in(coord)
            if piece:
                board[coord[0]][coord[1]] = '[{}]'.format(piece.symbol)
        pp.pprint(board)

    def piece_in(self, position):
        """Returns the piece at a given coordinate (or None)."""
        try:
            return self.square[position][2]
        except KeyError:    # If fed [position] isn't in the board
            return

    def step(self, start, direction, n=1):
        """Given an origin square and a direction, gets the square n steps away in that direction
        and returns the coordinate of that square.
        origin = tuple(row, col); direction = string
        returns tuple(coord); or error string
        """
        move = {
            'up':         (start[0] - n, start[1]),
            'down':       (start[0] + n, start[1]),
            'left':       (start[0], start[1] - n),
            'right':      (start[0], start[1] + n),
            'up-left':    (start[0] - n, start[1] - n),
            'up-right':   (start[0] - n, start[1] + n),
            'down-left':  (start[0] + n, start[1] - n),
            'down-right': (start[0] + n, start[1] + n)
        }
        if move.get(direction) in self.square:
            return move.get(direction)
        else:
            return BS[0]

    def cast_ray(self, start, direction):
        """From a starting piece's square, makes a list of open squares in the given direction.
        If there's a piece there, it will add the legal square only if the colors don't match.
        Used by Piece class to generate legal moves.
        """
        open_squares = []
        coord = start
        piece = self.piece_in(start)
        while True:
            step_coord = self.step(coord, direction)
            obstacle = self.piece_in(step_coord)
            if step_coord == BS[0]:
                break
            elif not obstacle:    # If the square in question is empty
                open_squares.append(step_coord)
            elif not piece.friend_check(self, step_coord):  # If the obstacle is an enemy
                open_squares.append(step_coord)
                break
            else:       # If an ally
                break
            coord = step_coord
        return open_squares

    def move_piece(self, turn):
        while True:
            try:    # Try to gather all the needed variables, and retry on a failure
                start_alg, end_alg = input("Move where to where? (separate with space): ").upper().split()
                start = self.key[start_alg]   # tuple here and below
                end = self.key[end_alg]
                piece = self.piece_in(start)
            except (KeyError, ValueError) as err:
                print(err)
                continue
            if piece.color != self.player[turn]:
                print("That's not your piece!")
                continue

            if end in piece.legal_moves(self, start):
                self.square[end][2] = piece
                self.square[start][2] = None
                piece.count += 1
                self.draw_board()
                break
            else:
                print("Not a legal move")
                continue

    def play_game(self):
        p = 1     # 1 or -1 to go with self.player
        turn_count = {'white': 0, 'black': 0}
        while True:     # While not game over
            print("It is {}'s turn".format(self.player[p]))
            self.move_piece(p)
            turn_count[self.player[p]] += 1
            p *= -1


if __name__ == '__main__':
    chess = Board()
    chess.play_game()
