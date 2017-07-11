from board import Board
from render_functions import draw_board
from pieces import Pawn
from game_states import Team


def main():
    game_board = Board()
    game_board.initialize_squares()

    p = Pawn(2, 1, Team.WHITE)
    game_board.place_pieces([p])
    draw_board(game_board)


if __name__ == '__main__':
    main()
