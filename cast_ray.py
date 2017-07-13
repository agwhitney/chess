"""Methods for gathering info about a path.
The ray gathers information along a path and returns the last square, or
(if there's an ally there) the one before it.
"""

# There must be some way to clean up all of these functions, since they're all doing very similar things...
# TODO Add a 'check' flag. The king can't move into check, so it should use the ray functions to check the desired move

# CARDINALS


def north(piece, board):
    legal_squares = []

    # THESE ARE THE ONLY THINGS THAT CHANGE SO HOW DO I REPEAT LESS REPETITIONS
    for dy in range(piece.y - 1, -1, -1):    # square next to piece to top edge of board
        target = board.piece_in_square(piece.x, dy)
        square = board.squares[piece.x][dy]

        if not target:
            legal_squares.append(square)

        elif target.color != piece.color:
            legal_squares.append(square)
            break

        else:
            break

    return legal_squares


def south(piece, board):
    legal_squares= []

    for dy in range(piece.y + 1, board.height + 1):
        target = board.piece_in_square(piece.x, dy)
        square = board.squares[piece.x][dy]

        if not target:
            legal_squares.append(square)

        elif target.color != piece.color:
            legal_squares.append(square)
            break

        else:
            break

    return legal_squares


def east(piece, board):
    legal_squares = []

    for dx in range(piece.x + 1, board.width + 1):
        target = board.piece_in_square(dx, piece.y)
        square = board.squares[dx][piece.y]

        if not target:
            legal_squares.append(square)

        elif target.color != piece.color:
            legal_squares.append(square)
            break

        else:
            break

    return legal_squares


def west(piece, board):
    legal_squares = []

    for dx in range(piece.x - 1, -1, -1):
        target = board.piece_in_square(dx, piece.y)
        square = board.squares[dx][piece.y]

        if not target:
            legal_squares.append(square)

        elif target.color != piece.color:
            legal_squares.append(square)
            break

        else:
            break

    return legal_squares


# ORDINALS


def northeast(piece, board):
    legal_squares = []

    for dx, dy in zip(range(piece.x + 1, board.width + 1), range(piece.y - 1, -1, -1)):
        target = board.piece_in_square(dx, dy)
        square = board.squares[dx][dy]

        if not target:
            legal_squares.append(square)

        elif target.color != piece.color:
            legal_squares.append(square)
            break

        else:
            break

    return legal_squares


def northwest(piece, board):
    legal_squares = []

    for dx, dy in zip(range(piece.x - 1, -1, -1), range(piece.y - 1, -1, -1)):
        target = board.piece_in_square(dx, dy)
        square = board.squares[dx][dy]

        if not target:
            legal_squares.append(square)

        elif target.color != piece.color:
            legal_squares.append(square)
            break

        else:
            break

    return legal_squares


def southeast(piece, board):
    legal_squares = []

    for dx, dy in zip(range(piece.x + 1, board.width + 1), range(piece.y + 1, board.height + 1)):
        target = board.piece_in_square(dx, dy)
        square = board.squares[dx][dy]

        if not target:
            legal_squares.append(square)

        elif target.color != piece.color:
            legal_squares.append(square)
            break

        else:
            break

    return legal_squares


def southwest(piece, board):
    legal_squares = []

    for dx, dy in zip(range(piece.x - 1, -1, -1), range(piece.y + 1, board.height + 1, -1)):
        target = board.piece_in_square(dx, dy)
        square = board.squares[dx][dy]

        if not target:
            legal_squares.append(square)

        elif target.color != piece.color:
            legal_squares.append(square)
            break

        else:
            break

    return legal_squares
