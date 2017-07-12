"""Methods for gathering info about a path.
The ray gathers information along a path and returns the last square, or
(if there's an ally there) the one before it.
"""


def north(piece, board):
    legal_squares = []

    for dy in range(piece.y - 1, -1, -1):    # square next to piece to top edge of board
        target = board.piece_in_square(piece.x, dy)
        if not target:
            legal_squares.append(board.squares[piece.x][dy])

        elif target.color != piece.color:
            legal_squares.append(board.squares[piece.x][dy])

    return legal_squares
