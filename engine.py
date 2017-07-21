from board import Board
from draw_board import draw_board
from pieces import initialize_pieces
from game_states import Team, switch_teams
from move_functions import move


def main():
    game_board = Board()
    game_board.initialize_squares()

    pieces = initialize_pieces()

    draw_board(game_board, pieces)

    player_turn = Team.WHITE

    while True:
        """Parts of a turn:
        Reset: Remove Captured=True pieces; Reset team's pawns to passant=False; create state of object data
        Move: Use the move function and do a legal move (checked by the pieces)
        Cleanup: Promote any pawns; check for a checked king.
            If needed (you put yourself in check) reset to the state and just loop again without changing turns
        Issues for the future: checkmate? Maybe create a list of danger squares from enemy and safe squares from you
        """
        # Reset phase
        for piece in pieces:
            if piece.name == 'Pawn':
                if piece.passant is True:
                    piece.passant = False

            if piece.captured is True:
                pieces.remove(piece)

        # Move -I just do it somewhere else
        prompt = input("Starting and Ending Coordinates, separated by a space.\n").upper().split()

        # Cleanup
        draw_board(game_board, pieces)  # TODO Flip the board for the second player
        player_turn = switch_teams(player_turn)


if __name__ == '__main__':
    main()
