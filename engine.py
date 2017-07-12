from board import Board
from draw_board import draw_board
from pieces import initialize_pieces


def main():
    game_board = Board()
    game_board.initialize_squares()

    pieces = initialize_pieces()

    draw_board(game_board, pieces)


if __name__ == '__main__':
    main()
