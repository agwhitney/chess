"""Chess v2
Because things were getting a little out of hand in v1
Still trying to make Chess
"""

import copy
import pprint
pp = pprint.PrettyPrinter(indent=4)


def step(start, direction, n=1):
    """Given an origin square and a direction, gets the square one step away in that direction
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
    legal_coords = [(row, col) for row in range(1, 9) for col in range(1, 9)]
    if step_coord in legal_coords:
        return step_coord
    else:
        return "Step leads out of the board."


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
    def __init__(self, color):
        Piece.__init__(self, color, 'pawn', 'P')


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'rook', 'R')


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'knight', 'N')


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'bishop', 'B')


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'king', 'K')


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'queen', 'Q')


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
        return self.square[coord][2]

    def cast_ray(self, start, end):
        """From the starting square, casts a 'ray' in the direction of the ending square and returns the coordinate
        of the first piece that is in the way (which could be the ending piece!). If there are no pieces in the way,
        it will return None.
        """
        dif = [b - a for b, a in zip(end, start)]    # [delta-row, delta-col]. Needs to be a list to be mutable
        coord = start
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
        for step_dir in directions:
            if directions[step_dir]:    # If that's the direction
                while tuple(coord) != end:
                    step_coord = step(coord, step_dir)
                    if self.piece_in(step_coord):
                        return step_coord   # Returns here if there's an obstacle anywhere
                    coord = step_coord

    def move_piece(self):
        while True:
            try:    # Gather unique start and end and make sure the start has a piece
                start_alg, end_alg = input("Move where to where? (separate with space): ").upper().split()
                start = self.key[start_alg]   # tuple here and below
                end = self.key[end_alg]
                if start == end:
                    print("Start and End coordinate are the same")
                    continue
                if not self.piece_in(start):
                    print("Starting square is empty")
                    continue
            except (KeyError, ValueError) as err:
                print(err)
                continue

            piece = self.piece_in(start)
            self.square[end][2] = piece
            self.square[start][2] = None


if __name__ == '__main__':
    chess = Board()
