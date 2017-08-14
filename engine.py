from board import Board
from draw_board import draw_board
from teams import Team, switch_teams
from pieces import initialize_pieces, return_king


def main():
    game_board = Board()
    game_board.initialize_squares()
    pieces = initialize_pieces()

    player_turn = Team.WHITE

    message = None

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

        # Isolate the kings
        active_king = return_king(pieces, player_turn)
        inactive_king = return_king(pieces, switch_teams(player_turn))

        # Draw the board
        draw_board(game_board, pieces)

        # Present turn info and gather player's move input
        if message:
            print(message)
        print("It is {}'s turn".format(player_turn))
        player_input = input("Starting and Ending Coordinates, separated by a space.\n" +
                             "Type 'castle 0|8' to castle with the Rook at that position.\n").upper().split()
        start, end = player_input[0], player_input[1]   # They can type whatever but I'm only taking the first 2 words

        # Castling
        if start == 'CASTLE':   # TODO handling castling
            pass
            player_turn = switch_teams(player_turn)

        # Standard Move
        else:
            x1, y1 = game_board.key[start]
            x2, y2 = game_board.key[end]

            piece = game_board.piece_in_square(x1, y1)
            target = game_board.piece_in_square(x2, y2)

            # Is there a piece there?
            if not piece:
                message = "There's no piece in the starting square."
                continue

            # Is it the player's piece?
            if piece.color != player_turn:
                message = "That's not your piece to move!"
                continue

            # Move looks good to go! Do it!
            if (x2, y2) in piece.legal_moves(game_board):
                if target:
                    target.captured = True
                piece.x, piece.y = x2, y2
            # Unless it's not a legal move
            else:
                message = "That's not a legal move for that piece."
                continue

            # Did you put your king in check?
            if active_king.in_check(game_board, pieces):
                message = "That move puts your own king in check."
                if target:
                    target.captured = False
                piece.x, piece.y = x1, y1
                continue

            # Did you put their king in check?
            if inactive_king.in_check(game_board, pieces):
                message = "The {} King is in check!".format(inactive_king.color)

            # If the turn totally passes, then switch turns
            piece.moves_made += 1
            message = None
            player_turn = switch_teams(player_turn)



if __name__ == '__main__':
    main()
