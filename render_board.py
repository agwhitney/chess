"""
Contains the functions for drawing the board and the pieces atop it.
Does it need it's own file? Who knows!
"""
import pprint
pp = pprint.PrettyPrinter(indent=4)


def draw_board(game_board, pieces):
    for piece in pieces:
        game_board.board[piece.y][piece.x] = '[{}]'.format(piece.symbol)
    pp.pprint(game_board.board)
