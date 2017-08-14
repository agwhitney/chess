from board import Board
from cast_ray import castling_path_clear
from draw_board import draw_board
from pieces import initialize_pieces, return_king
from teams import Team, switch_teams


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
            message = None  # Clear the message variable

        print("It is {}'s turn".format(player_turn))
        player_input = input("Starting and Ending Coordinates, separated by a space.\n" +
                             "Type 'castle east|west' to castle with the Rook in that direction.\n"
                             ).upper().split()
        try:
            start, end = player_input[0], player_input[1]
        except IndexError:
            message = "Try typing that out again?"
            continue

        # MOVE HANDLING

        # Castling
        if start == 'CASTLE':
            # Determine the rook in question
            rook_y = 0 if player_turn == Team.BLACK else 7
            if end == 'WEST':
                rook = game_board.piece_in_square(0, rook_y)
            elif end == 'EAST':
                rook = game_board.piece_in_square(7, rook_y)
            else:
                message = "Please specify a direction ('east' or 'west')."
                continue

            # Has either piece moved?
            if active_king.moves_made > 0 or rook.moves_made > 0:
                message = "One or both of the pieces has moved previously."
                continue

            # Is the path clear?
            if not castling_path_clear(active_king, rook, game_board, end.lower()):  # TODO normalize uppercase?
                message = "The path between the king and rook isn't clear."
                continue

            # Is the king in check?
            if active_king.in_check(game_board, pieces):
                message = "You can't castle out of check!"
                continue

            # Looks good!
            king_previous = active_king.x
            rook_previous = rook.x
            if end == 'WEST':
                active_king.x -= 2
                rook.x = active_king.x + 1

            elif end == 'EAST':
                active_king.x += 2
                rook.x = active_king.x - 1

            # Did you put your king in check?
            if active_king.in_check(game_board, pieces):
                message = "That move puts your own king in check."
                active_king.x = king_previous
                rook.x = rook_previous
                continue

            # Did you put their king in check?
            if inactive_king.in_check(game_board, pieces):
                message = "The {} King is in check!".format(inactive_king.color)

            # Everything went smoothly!
            active_king.moves_made += 1     # Castling is considered a king's move, so I've omitted adding to the rook
            player_turn = switch_teams(player_turn)

        # Standard Move
        elif start in game_board.key and end in game_board.key:
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
            player_turn = switch_teams(player_turn)

        # Mistake
        else:
            message = "Try typing that again?"
            continue


if __name__ == '__main__':
    main()
