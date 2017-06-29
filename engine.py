from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from render_board import draw_board


def main():
    game_board = Board()
    # Place all of the starting pieces
    pieces = {}
    for i in range(1, 9):
        pieces['wp{}'.format(i)] = Pawn(2, i, False)
        pieces['bp{}'.format(i)] = Pawn(7, i, True)

        if i == 1 or i == 8:
            pieces['wr{}'.format(i)] = Rook(1, i, False)
            pieces['br{}'.format(i)] = Rook(8, i, True)
        if i == 2 or i == 7:
            pieces['wn{}'.format(i)] = Knight(1, i, False)
            pieces['bn{}'.format(i)] = Knight(8, i, True)
        if i == 3 or i == 6:
            pieces['wb{}'.format(i)] = Bishop(1, i, False)
            pieces['bb{}'.format(i)] = Bishop(8, i, True)
        if i == 4:
            pieces['wq{}'.format(i)] = Queen(1, i, False)
            pieces['bq{}'.format(i)] = Queen(8, i, True)
        if i == 5:
            pieces['wk{}'.format(i)] = King(1, i, False)
            pieces['bk{}'.format(i)] = King(8, i, True)

    draw_board(game_board, [pieces[i] for i in pieces])


if __name__ == '__main__':
    main()
