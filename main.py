import pygame as pg

from os import path

from board import Board
from settings import *
from pieces import *
from square import Square


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()  # Necessary?
        pg.key.set_repeat(500, 100)  # same?
        self.load_data()

    def load_data(self):
        game_dir = path.dirname(__file__)
        board_file = path.join(game_dir, 'board_setup.txt')
        image_path = path.join(game_dir, 'images')

        self.board_map = Board(board_file)
        self.pawn_img = {'white': path.join(image_path, WHITE_PAWN), 'black': path.join(image_path, BLACK_PAWN)}
        self.king_img = {'white': path.join(image_path, WHITE_KING), 'black': path.join(image_path, BLACK_KING)}
        self.queen_img = {'white': path.join(image_path, WHITE_QUEEN), 'black': path.join(image_path, BLACK_QUEEN)}
        self.bishop_img = {'white': path.join(image_path, WHITE_BISHOP), 'black': path.join(image_path, BLACK_BISHOP)}
        self.knight_img = {'white': path.join(image_path, WHITE_KNIGHT), 'black': path.join(image_path, BLACK_KNIGHT)}
        self.rook_img = {'white': path.join(image_path, WHITE_ROOK), 'black': path.join(image_path, BLACK_ROOK)}

    def new(self):
        # These probably aren't all needed
        self.all_sprites = pg.sprite.Group()
        self.all_pieces = pg.sprite.Group()
        self.white_team = pg.sprite.Group()
        self.black_team = pg.sprite.Group()
        self.team_sprites = {'white': self.white_team, 'black': self.black_team}
        self.board_squares = pg.sprite.Group()
        self.piece_selected = None

        # Set up the board
        flip = True
        for row, squares in enumerate(self.board_map.data):
            flip = not flip
            for col, square in enumerate(squares):
                # Draw board squares
                color = ORANGE if flip else BLUE
                Square(self, color, col, row)
                flip = not flip

                # Draw pieces
                if square[0] == 'W':
                    team = 'white'
                elif square[0] == 'B':
                    team = 'black'
                piece = square[1]

                if piece == 'P':
                    Pawn(self, team, col, row)
                elif piece == 'K':
                    King(self, team, col, row)
                elif piece == 'Q':
                    Queen(self, team, col, row)
                elif piece =='B':
                    Bishop(self, team, col, row)
                elif piece == 'N':
                    Knight(self, team, col, row)
                elif piece == 'R':
                    Rook(self, team, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        raise SystemExit

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT), 2)
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (WIDTH, y), 2)

    def draw(self):
        for sprite in self.board_squares:
            self.screen.blit(sprite.image, sprite.pos)
        for sprite in self.all_pieces:
            self.screen.blit(sprite.image, sprite.pos)
        if self.piece_selected:
            for square in self.piece_selected.legal_moves:
                a = pg.Surface((TILESIZE, TILESIZE))
                a.set_alpha(150)
                a.fill(PURPLE)
                self.screen.blit(a, (square.x, square.y))
        self.draw_grid()
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if not self.piece_selected:
                    for piece in self.all_pieces:
                        if piece.rect.collidepoint(event.pos):
                            self.piece_selected = piece
                            self.piece_selected.generate_moves(self)

                elif self.piece_selected:
                    for square in self.board_squares:
                        if square.rect.collidepoint(event.pos):
                            if square.pos in self.piece_selected.legal_moves:
                                self.piece_selected.move(square)
                            self.piece_selected = None


if __name__ == '__main__':
    g = Game()
    while True:
        g.new()
        g.run()
