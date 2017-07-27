def draw_board(board, pieces):
    """Prints a w*h formatted board.
    As is, row numbers are flexible, but column letters are explicit and only go to H.
    Also updates the board.squares.piece_present attribute with the piece or with None.
    """
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

            else:   # no break; i.e. if there's no piece at that coordinate
                print(board.squares[x][y].symbol, end='')
                board.squares[x][y].piece_present = None

        print(' {} '.format(y + 1))     # No end='' creates the newline
    print(letters)
