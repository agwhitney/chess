from pygame.math import Vector2 as vec


TITLE = "Chess"

BOARD_SETUP_MAP = 'board_setup.txt'

TILESIZE = 64
WIDTH = TILESIZE * 8
HEIGHT = TILESIZE * 8
FPS = 60

BLACK = (0, 0, 0)
ORANGE = (255, 120, 120)
BLUE = (0, 100, 200)

# White images
WHITE_KING = 'white_king.png'
WHITE_QUEEN = 'white_queen.png'
WHITE_BISHOP = 'white_bishop.png'
WHITE_KNIGHT = 'white_knight.png'
WHITE_ROOK = 'white_rook.png'
WHITE_PAWN = 'white_pawn.png'

# Black images
BLACK_KING = 'black_king.png'
BLACK_QUEEN = 'black_queen.png'
BLACK_BISHOP = 'black_bishop.png'
BLACK_KNIGHT = 'black_knight.png'
BLACK_ROOK = 'black_rook.png'
BLACK_PAWN = 'black_pawn.png'

# Direction unit vectors
UP = vec(0, -1) * TILESIZE
DOWN = vec(0, 1) * TILESIZE
LEFT = vec(-1, 0) * TILESIZE
RIGHT = vec(1, 0) * TILESIZE
