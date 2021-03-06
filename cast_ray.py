"""Methods for gathering info about a path.
The ray gathers information along a path and returns the last square, or (if there's an ally there) the one before it.
Cardinals and Ordinals and Radial are separate for clarity when they're called in other places.
"""


def cardinals(piece, board):
    """cast_ray() in the four cardinal directions"""
    legal_squares = []

    for direction in ['north', 'south', 'east', 'west']:
        squares = cast_ray(piece, board, direction)
        legal_squares.extend(squares)

    return legal_squares


def ordinals(piece, board):
    """cast_ray() in the four ordinal directions"""
    legal_squares = []

    for direction in ['northeast', 'northwest', 'southeast', 'southwest']:
        squares = cast_ray(piece, board, direction)
        legal_squares.extend(squares)

    return legal_squares


def radial(piece, board):
    """cast_ray() in all eight compass directions"""
    legal_squares = []

    legal_squares.extend(cardinals(piece, board))
    legal_squares.extend(ordinals(piece, board))

    return legal_squares


def cast_ray(piece, board, direction):
    """Casts a ray in one direction by iterating in steps in that direction.
    Returns a list of legal square coordinates (in that direction).
    """
    dx, dy = step(piece.x, piece.y, direction)
    legal_squares = []

    while (dx, dy) in board.square_coordinates():
        square = board.square(dx, dy)
        target = board.piece_in_square(dx, dy)

        if not target:
            legal_squares.append((square.x, square.y))
            dx, dy = step(dx, dy, direction)
            continue

        elif target.color != piece.color:
            legal_squares.append((square.x, square.y))
            break

        else:
            break

    return legal_squares


def castling_path_clear(king, rook, board, direction):
    """Similar to cast_ray, but this will return True if there are no pieces between
    the start (king) and end (rook) coordinates.
    """
    dx, dy = step(king.x, king.y, direction)

    while (dx, dy) in board.square_coordinates():
        target = board.piece_in_square(dx, dy)

        if not target:
            dx, dy = step(dx, dy, direction)

        elif target == rook:
            return True

        else:
            return False


def step(x, y, direction):
    """Returns the coordinates a step in a given direction away from the origin.
    """
    directions = {
        'north': (x, y - 1),
        'south': (x, y + 1),
        'east': (x + 1, y),
        'west': (x - 1, y),
        'northeast': (x + 1, y - 1),
        'northwest': (x - 1, y - 1),
        'southeast': (x + 1, y + 1),
        'southwest': (x - 1, y + 1)
    }
    return directions.get(direction)
