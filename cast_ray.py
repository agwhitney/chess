"""Methods for gathering info about a path.
The ray gathers information along a path and returns the last square, or (if there's an ally there) the one before it.
Cardinals and Ordinals are separate for clarity when they're called in other places.
"""
# TODO Add a 'check' flag. The king can't move into check, so it should use the ray functions to check the desired move


def cardinals(piece, board):
    legal_squares = []

    for direction in ['north', 'south', 'east', 'west']:
        squares = cast_ray(piece, board, direction)
        legal_squares.append(squares)

    return legal_squares


def ordinals(piece, board):
    legal_squares = []

    for direction in ['northeast', 'northwest', 'southeast', 'southwest']:
        squares = cast_ray(piece, board, direction)
        legal_squares.append(squares)

    return legal_squares


def step(x, y, direction):
    """Returns the coordinates a step in a given direction away from the origin.
    Potential issue of having squares outside of the board?
    """
    directions = {
        'north': (x, y - 1),
        'south': (x, y + 1),
        'east': (x + 1, y),
        'west': (x - 1, y),
        'northeast': (x + 1, y - 1),
        'northwest': (x - 1, y - 1),
        'southeast': (x + 1, y + 1),
        'southwest': (x - 1, y - 1)
    }
    return directions.get(direction)    # No default should be fine because this shouldn't ever be used by a user


def cast_ray(piece, board, direction):
    """Casts a ray in one direction by iterating in steps in that direction."""
    dx, dy = step(piece.x, piece.y, direction)
    legal_squares = []

    while True:
        try:
            square = board.squares[dx][dy]
            target = board.piece_in_square(dx, dy)

            if not target:
                legal_squares.append(square)
                dx, dy = step(dx, dy, direction)

            elif target.color != piece.color:
                legal_squares.append(square)
                break

            else:
                break

        except IndexError:
            break

    return legal_squares
