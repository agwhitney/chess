def draw_board(game_board, pieces):
    """Prints a formatted board, and should be flexible (aside from the labels) to any height/width.
    I feel like it goes a bit too deep on the loops, """
    letters = '    A  B  C  D  E  F  G  H'  # This is explicit. Deal with it. (that's 4 spaces)

    print(letters)
    for y in range(game_board.height):
        print(' {} '.format(y), end='')

        for x in range(game_board.width):
            for piece in pieces:
                if piece.x == x and piece.y == y:
                    print(piece.symbol, end='')
                    break
            # For-else: else runs if for doesn't break (ie if there's no piece at x,y
            else:
                for square in game_board.squares:
                    if square.x == x and square.y == y:
                        print(square.symbol, end='')

        print(' {} '.format(y))     # No end='' creates the newline
    print(letters)
