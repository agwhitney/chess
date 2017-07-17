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
        prompt = input("Starting and Ending Coordinates, separated by a space.\n").upper().split()
        move(game_board, pieces, player_turn, prompt[0], prompt[1])

        draw_board(game_board, pieces)  # TODO Flip the board for the second player
        player_turn = switch_teams(player_turn)


if __name__ == '__main__':
    main()
