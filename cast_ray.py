"""Methods for gathering info about a path.
The ray gathers information along a path and returns the last square, or (if there's an ally there) the one before it.
Cardinals and Ordinals and Radial are separate for clarity when they're called in other places.
"""
# TODO Add a 'check' flag. The king can't move into check, so it should use the ray functions to check the desired move


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
    Returns a list of legal squares (in that direction).
    """
    dx, dy = step(piece.x, piece.y, direction)
    legal_squares = []

    while 0 <= dx <= board.width and 0 <= dy <= board.height:
        square = board.squares[dx][dy]
        target = board.piece_in_square(dx, dy)

        if not target:
            legal_squares.append(square)
            dx, dy = step(dx, dy, direction)

        elif target.color != piece.color:
            legal_squares.append(square)

            if target.name == 'King':
                target.checked = True

            break

        else:
            break

    return legal_squares


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
