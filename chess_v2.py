"""Chess v2
Because things were getting a little out of hand in v1
Still trying to make Chess
"""

import copy
import pprint
pp = pprint.PrettyPrinter(indent=4)

CARDINALS = ['up', 'down', 'left', 'right']
ORDINALS = ['up-left', 'up-right', 'down-left', 'down-right']


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
            step = board.step(start, forward+direction, n=1)
            try:
                if board.piece_in(step) and self.color != board.piece_in(step).color:
                    moves.append(step)
            except:     # No piece in the square??
                pass
        # Passant step
        for direction in ['left', 'right']:
            pass
        return moves


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'rook', 'R')

    def legal_moves(self, board, start):
        moves = []
        for direction in CARDINALS:
            moves.extend(board.cast_ray(start, direction))
        return moves


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'knight', 'N')


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
        moves = []
        for direction in CARDINALS + ORDINALS:
            step = board.step(start, direction)
            if not board.piece_in(step):
                moves.append(step)
            elif board.piece_in(step).color != self.color:
                moves.append(step)
            else:
                pass
        # castling
        pass


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

        self._create_board()

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

    def piece_in(self, coord):
        """Returns the piece at a given coordinate (or None)."""
        # Does None fill the same role as False if I'm checking for a piece there w/ ifs?
        return self.square[coord][2]

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
        step_coord = move.get(direction, 'nothing')
        if step_coord in self.square:
            return step_coord
        else:
            # Some kind of error flag
            return "Step leads out of the board."

    def cast_ray(self, start, direction):
        """From a starting piece's square, makes a list of open squares in the given direction.
        If there's a piece there, it will add the legal square only if the colors don't match.
        Used by Piece class to generate legal moves.
        """
        open_squares = []
        coord = start
        while True:
            try:
                step_coord = self.step(coord, direction)
                piece = self.piece_in(start)
                obstacle = self.piece_in(step_coord)
                if not obstacle:
                    open_squares.append(step_coord)
                elif piece.color != obstacle.color:
                    open_squares.append(step_coord)
                    break
                else:
                    break
                coord = step_coord
            except:
                break
        return open_squares

    def get_direction(self, start, end):
        """From a start and end point, returns the direction from start to end.
        """
        dif = [b - a for b, a in zip(end, start)]    # [delta-row, delta-col]. Needs to be a list to be mutable
        directions = {
            'up'        : eval('dif[0] < 0 and dif[1] == 0'),
            'down'      : eval('dif[0] > 0 and dif[1] == 0'),
            'left'      : eval('dif[0] == 0 and dif[1] < 0'),
            'right'     : eval('dif[0] == 0 and dif[1] > 0'),
            'up-left'   : eval('dif[0] < 0 and dif[1] < 0'),
            'up-right'  : eval('dif[0] < 0 and dif[1] > 0'),
            'down-left' : eval('dif[0] > 0 and dif[1] < 0'),
            'down-right': eval('dif[0] > 0 and dif[1] > 0')
        }
        for dyr in directions:
            if directions[dyr]:
                return dyr

    def move_piece(self):
        while True:
            try:    # Try to gather all the needed variables, and retry on a failure
                start_alg, end_alg = input("Move where to where? (separate with space): ").upper().split()
                start = self.key[start_alg]   # tuple here and below
                end = self.key[end_alg]
                piece = self.piece_in(start)
                direction = self.get_direction(start, end)
            except (KeyError, ValueError) as err:
                print(err)
                continue

            if end in piece.legal_moves(self, start):
                self.square[end][2] = piece
                self.square[start][2] = None
                self.draw_board()
            else:
                print("Not a legal move")
            # break


if __name__ == '__main__':
    chess = Board()
    chess._place_pieces()
    chess.draw_board()
    chess.move_piece()
