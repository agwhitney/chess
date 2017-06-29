
class Board:
    def __init__(self):
        board, squares, key = self.create_board()
        self.board = board      # Visual Representation
        self.squares = squares    # tuple(coord)) : [str(coord), str(color)]
        self.key = key          # string(coord) : tuple(coord)

    def create_board(self):
        """Creates the board object, the base visual, and a coordinate translator.
        Note that coordinates are (row, column) - down and right.
        """
        board = []
        squares = {}
        key = {}
        checker = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        for number in range(1, 9):
            row = []
            checker += 1
            for letter in letters:
                checker += 1
                if checker % 2 == 0:
                    color = 'white'
                    row.append('[ ]')
                else:
                    color = 'black'
                    row.append('[/]')

                coord_alg = '{}{}'.format(letter, number)
                coord = (number, letters.index(letter) + 1)

                key[coord_alg] = coord
                squares[coord] = [coord_alg, color]

            board.append(row)
        # Insert the top and left algebraic labels
        board.insert(0, [' {} '.format(i) for i in letters])
        board[0].insert(0, '   ')
        for i in range(1, 9):
            board[i].insert(0, ' {} '.format(i))

        return board, squares, key

    def color(self, y, x):
        square = tuple(y, x)
        return self.squares(square)[1]
