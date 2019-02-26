import pygame as pg

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
        pass

    def new(self):
        self.all_sprites = pg.sprite.Group()

        # Draw a board
        flip = True
        for row in range(8):
            flip = not flip
            for col in range(8):
                color = WHITE if flip else BLACK
                pg.draw.rect(self.screen, color, (row * TILESIZE, col * TILESIZE, TILESIZE, TILESIZE))
                flip = not flip

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
            pg.draw.line(self.screen, RED, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, RED, (0, y), (WIDTH, y))

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
