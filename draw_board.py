def draw_board(board, pieces):
    """Prints a w*h formatted board.
    As is, row numbers are flexible, but column letters are explicit and only go to H.
    Also updates the board.squares.piece_present attribute with the piece or with None.
    """
    # First row: The letters. Repeated for the last row, also
    print("   ", end='')    # Four spaces in the corner...
    for x in range(board.width):
        if x != board.width - 1:
            print(" {} ".format(chr(65 + x)), end='')
        else:
            print(" {} ".format(chr(65 + x)))   # Last one needs to have a newline!

    # Print the numbers and board/piece symbols
    for y in range(board.height):
        print(" {} ".format(y + 1), end='')

        for x in range(board.width):
            for piece in pieces:
                if piece.x == x and piece.y == y:
                    print(piece.symbol, end='')
                    board.square(x, y).piece_present = piece
                    break
            else:   # no break; i.e. no piece at that coordinate
                print(board.square(x, y).symbol, end='')
                board.square(x, y).piece_present = None    # If there was a piece there, there ain't now

        print(" {} ".format(y + 1))     # No end='' creates the newline

    # Print the last row of letters (same as above)
    print("   ", end='')    # Four spaces in the corner...
    for x in range(board.width):
        if x != board.width - 1:
            print(" {} ".format(chr(65 + x)), end='')
        else:
            print(" {} ".format(chr(65 + x)))   # Newline is a safe bet
