"""Chess by Adam
Wherein I try to make a functioning game of chess
"""

import copy
import pprint
pp = pprint.PrettyPrinter(indent=4)     # use pp.pprint instead of print


class Piece:
    """Pieces contain guidelines for legal moves. The engine accepts the move that's desired
    and processes it, and checks its legality against the object definition (differentials)
    position = coordinates as list; color = string; symbol = string (character)
    """
    def __init__(self, color, name, symbol, hasMoved=False):
        self.color = color
        self.name = name
        self.symbol = symbol
        self.hasMoved = hasMoved

        if self.color == 'black':
            self.symbol = self.symbol.lower()

    def __repr__(self):
        return "<{} {} ({})>".format(self.color, self.name, self.symbol)


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'pawn', 'P')

    def legal_moves(self, difference):
        if self.color == 'white':
            if difference[0] == -1:
                return True
            elif not self.hasMoved and difference[0] == -2:
                return True
            else:
                return False

        elif self.color == 'black':
            if difference[0] == 1:
                return True
            elif not self.hasMoved and difference[0] == 2:
                return True
            else:
                return False


class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'rook', 'R')

    @staticmethod
    def legal_moves(difference):
        if 0 in (difference[0], difference[1]):
            return True
        else:
            return False
      

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'knight', 'N')

    @staticmethod
    def legal_moves(difference):
        if abs(difference[0]) == 2 and abs(difference[1]) == 1:
            return True
        elif abs(difference[0]) == 1 and abs(difference[1]) == 2:
            return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'bishop', 'B')

    @staticmethod
    def legal_moves(difference):
        if difference[0] == difference[1]:
            return True
        else:
            return False


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'king', 'K')

    @staticmethod
    def legal_moves(difference):
        if abs(difference[0]) <= 1 and abs(difference[1]) <= 1:
            return True
        else:
            return False


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 'queen', 'Q')

    @staticmethod
    def legal_moves(difference):
        if 0 in (difference[0], difference[1]):
            return True
        elif difference[0] == difference[1]:
            return True
        else:
            return False


class Board:
    """Creates the board as a list of strings, a metadata dictionary for each square,
    and a key to translate algebraic coordinates to cartesian.
    """
    def __init__(self):
        """Creates a board object
        board = 9x9 list (visual; Piece symbols are placed on top)
        square = dictionary: tuple to list(string, string, object/None)
        key = dictionary: string to tuple
        """
        self.board = []     # Visual presentation
        self.square = {}    # Maps square (cartesian) to metadata (algCoord, color, piece present)
        self.key = {}       # Maps algebraic(string) to cartesian coordinates(tuple)
        
        # Create the empty checkered board
        count = 0   # For the checker pattern
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for letter in letters:     # Denotes row
            row = []
            count += 1      # Checker, not stripe
            for number in range(8):  # Denotes column
                count += 1
                coord_alg = '{}{}'.format(letter, number+1)
                if count % 2 == 0:
                    color = 'white'
                    row.append('[ ]')   # White
                else:
                    color = 'black'
                    row.append('[/]')   # Black
                self.key[coord_alg] = (letters.index(letter)+1, number+1)
                self.square[(letters.index(letter)+1, number+1)] = [coord_alg, color, None]
            self.board.append(row)

        # Append the reference row and column
        # Bonus: Now the coordinates fit: (1,1) on the board is actually [1,1]
        self.board.insert(0, [' {} '.format(i) for i in range(9)])
        for row in self.board[1:]:
            row.insert(0, ' {} '.format(letters[self.board.index(row)-1]))
      
    def __repr__(self, square=None):
        """Return some kind of info (maybe the board, redundant to __str__?). 
        If square is a string in Key, return info about that square.
        """
        if square in self.key:
            coord = self.key[square]
            return self.square[coord]
        else:
            return self.board

    def clear_path(self, start, end):
        """Returns True if the straight path between start and end is free of obstacles
        (ie self.square(square)[2] is None throughout. Returns False if not clear. Does not
        check the end coordinate; leaves that to the engine (checking move legality).
        start and end are tuple coordinates
        """


class Engine:
    """Brings the Piece and Board classes together to make a chess game!"""
    def __init__(self):
        self.board = Board()
        self.create_pieces()

    def create_pieces(self):
        # Pawns
        for i in range(1, 9):
            self.board.square[(2, i)][2] = Pawn('black')
            self.board.square[(7, i)][2] = Pawn('white')
        # Rooks
        for col in [1, 8]:
            self.board.square[(1, col)][2] = Rook('black')
            self.board.square[(8, col)][2] = Rook('white')
        # Knights
        for col in [2, 7]:
            self.board.square[(1, col)][2] = Knight('black')
            self.board.square[(8, col)][2] = Knight('white')
        # Bishops
        for col in [3, 6]:
            self.board.square[(1, col)][2] = Bishop('black')
            self.board.square[(8, col)][2] = Bishop('white')
        # Queens
        self.board.square[(1, 4)][2] = Queen('black')
        self.board.square[(8, 4)][2] = Queen('white')
        # Kings
        self.board.square[(1, 5)][2] = King('black')
        self.board.square[(8, 5)][2] = King('white')

    def draw_board(self):
        """Goes through self.board.square and draws the present pieces on their square, then prints the board.
        Doesn't change self.board.board - just uses it as a clean sheet each time.
        Doesn't return anything - just prints the updated board
        """
        board = copy.deepcopy(self.board.board)    # Deep copy of the empty board, keeping the original intact
        for coord in self.board.square:
            piece = self.board.square[coord][2]
            if piece is not None:
                board[coord[0]][coord[1]] = '[{}]'.format(piece.symbol)
        pp.pprint(board)

    def move_piece(self):
        """Gather as input starting and ending algebraic coordinates.
        The differential is used with Piece functions to determine if it is legal.
        If not, or if there is no piece in the starting square, it will start over.
        """
        while True:
            # Gather move coordinates (algebraic) and get the differential
            try:
                start, end = input("Move where to where? (separate with space): ").upper().split()
                start_coord = self.board.key[start]   # tuple here and below
                end_coord = self.board.key[end]
                if start_coord == end_coord:
                    print("The start and end are the same.")
                    continue
            except (KeyError, ValueError):
                print("You messed up!")
                continue
            # Is there even a piece on that square?
            if self.board.square[start_coord][2] is None:
                print("No piece in that square")
                continue    # Start the loop again
            else:
                piece = self.board.square[start_coord][2]
                #

            # Check legality in a different function - if it's True, then do the moving bid'nis. False: try again
            if self.check_move(piece, start_coord, end_coord) is True:
                print("neat")
                piece.hasMoved = True
                self.board.square[end_coord][2] = piece
                self.board.square[start_coord][2] = None
                self.draw_board()
                #break
            else:
                print("not neat")
                continue    # Start the loop again

    def check_move(self, piece, start_coord, end_coord):
        """Checks the legality of a given move for a given piece, taking info provided from Engine.move_piece().
        move = [delta-row, delta-col]; piece = Piece object in starting square
        """
        move = [b - a for b, a in zip(end_coord, start_coord)]

        # Check that the move would pass on a blank board
        if piece.legal_moves(move):
            return True


if __name__ == '__main__':
    """'The end of your file has raw logic not wrapped in if __name__ == "__main__":.
    This means that if someone were to import your file, your program would actually run. This is very bad form.'
    """
    chess = Engine()
    chess.draw_board()
    chess.move_piece()
