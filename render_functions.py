def draw_board(game_board):
    letters = '    A  B  C  D  E  F  G  H'  # This is explicit. Deal with it. (that's 4 spaces)

    print(letters)
    for y in range(game_board.height):
        print(' {} '.format(y), end='')
        for x in range(game_board.width):
            print(game_board.squares[y][x].symbol, end='')
        print(' {} '.format(y))     # No end='' creates the newline
    print(letters)

