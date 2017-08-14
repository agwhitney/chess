from board import Board
from draw_board import draw_board
from game_states import Team, switch_teams
from pieces import initialize_pieces, return_king


def main():
    game_board = Board()
    game_board.initialize_squares()
    pieces = initialize_pieces()

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

        # Draw the board
        draw_board(game_board, pieces)

        # Move
        print("It is {}'s turn".format(player_turn))
        player_input = input("Starting and Ending Coordinates, separated by a space.\n").upper().split()
        start, end = player_input[0], player_input[1]   # They can type whatever but I'm only taking the first 2

        if start == 'CASTLE':   # TODO handling castling
            player_turn = switch_teams(player_turn)

        else:   # Regular old move
            x1, y1 = game_board.key[start]
            x2, y2 = game_board.key[end]

            piece = game_board.piece_in_square(x1, y1)
            if not piece:
                print("There's no piece in the starting square.")
                continue

            if (x2, y2) in piece.legal_moves(game_board):
                piece.move(x2, y2, game_board)
            else:
                print("That's not a legal move for that piece!")
                continue

            if player_king.in_check(game_board, pieces):
                print("You're putting your own king in check.")
                piece.move(x1, y1, game_board)


            player_turn = switch_teams(player_turn)


if __name__ == '__main__':
    main()
