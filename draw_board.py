def draw_board(board, pieces):
    """Prints a formatted board, and should be flexible (aside from the labels) to any height/width."""
    letters = '    A  B  C  D  E  F  G  H'  # This is explicit. ...for now? (that's four spaces)

    print(letters)
    for y in range(board.height):
        print(' {} '.format(y + 1), end='')

        for x in range(board.width):
            for piece in pieces:
                if piece.x == x and piece.y == y:
                    print(piece.symbol, end='')
                    board.squares[x][y].piece_present = piece
                    break
            # For-else: else runs if for doesn't break (ie if there's no piece at x,y)
            else:
                print(board.squares[x][y].symbol, end='')
                board.squares[x][y].piece_present = None

        print(' {} '.format(y + 1))     # No end='' creates the newline
    print(letters)
