from board import Board
from draw_board import draw_board
from pieces import initialize_pieces, return_king
from game_states import Team, switch_teams


def main():
    game_board = Board()
    game_board.initialize_squares()
    pieces = initialize_pieces()

    draw_board(game_board, pieces)
    player_turn = Team.WHITE

    # ----------------
    # ENGINE LOOP
    # ----------------
    while True:
        # Reset and clean up corpses
        for piece in pieces:
            if piece.captured is True:
                pieces.remove(piece)

            if piece.name == 'Pawn' and piece.color == player_turn:
                if piece.passant is True:
                    piece.passant = False

        player_king = return_king(pieces, player_turn)

        # Move
        print("It is {}'s turn".format(player_turn))
        start, end = input("Starting and Ending Coordinates, separated by a space.\n").upper().split()

        if start == 'CASTLE':
            pass    # function for castling

        else:
            x1, y1 = game_board.key[start]
            x2, y2 = game_board.key[end]

            piece = game_board.piece_in_square(x1, y1)
            piece.move(x2, y2, game_board)

            player_turn = switch_teams(player_turn)
            draw_board(game_board, pieces)


if __name__ == '__main__':
    main()
