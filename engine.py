from board import Board
from draw_board import draw_board
from pieces import initialize_pieces
from game_states import Team, switch_teams


def main():
    game_board = Board()
    game_board.initialize_squares()

    pieces = initialize_pieces()

    draw_board(game_board, pieces)

    player_turn = Team.WHITE

    # While True loop for the game:
    # All it really has to do is take input,
    # convert it into a move,
    # check the legality (done by the piece, I think),
    # and make the move.
    # And then change the turn, I guess.
    while True:

        prompt = input()

        draw_board(game_board, pieces)  # TODO Flip the board for the second player
        player_turn = switch_teams(player_turn)
        break


if __name__ == '__main__':
    main()
