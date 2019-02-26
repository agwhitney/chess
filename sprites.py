import pygame as pg
vec = pg.math.Vector2

from settings import *


class Piece(pg.sprite.Sprite):
    def __init__(self, game, team, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)

        self.team = team
        self.pos = vec(x, y) * TILESIZE
        self.image = None
