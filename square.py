from game_states import Team


class Square:
    """The Squares that make up the board.
    Doesn't really need x or y attributes, because they're generated as a list of lists (so it
    pretty much does that anyway) and called like that. Keeping it for now because it's useful
    for sanity-checks.
    """
    def __init__(self, x, y, color, piece_present=None):
        self.x = x
        self.y = y
        self.color = color
        self.piece_present = piece_present  # This is updated in draw_board and used for casting rays

        if color == Team.WHITE:
            self.symbol = '[ ]'
        elif color == Team.BLACK:
            self.symbol = '[/]'

    def __repr__(self):
        return "<{} Square at ({}, {})>".format(self.color, self.x, self.y)
