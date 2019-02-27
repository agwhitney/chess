import pygame as pg

from os import path

from board import Board
from settings import *
from sprites import *


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
        self.image_path = path.join(game_dir, 'images')

        self.board = Board(board_file)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.white_team = pg.sprite.Group()
        self.black_team = pg.sprite.Group()

        flip = True
        for row, squares in enumerate(self.board.data):
            flip = not flip
            for col, square in enumerate(squares):
                # Draw board squares
                color = ORANGE if flip else BLUE
                pg.draw.rect(self.screen, color, (row * TILESIZE, col * TILESIZE, TILESIZE, TILESIZE))
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
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.pos)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


if __name__ == '__main__':
    g = Game()
    while True:
        g.new()
        g.run()
