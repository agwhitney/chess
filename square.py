import pygame as pg
vec = pg.math.Vector2

from settings import *


class Square(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        self.groups = game.all_sprites, game.board_squares
        super().__init__(self.groups)

        self.color = color
        self.pos = vec(x, y) * TILESIZE
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.fill(color)
        self.rect.topleft = self.pos
