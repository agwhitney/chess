import pygame as pg
vec = pg.math.Vector2

from os import path

from settings import *


class Piece(pg.sprite.Sprite):
    def __init__(self, game, team, x, y):
        if team == 'white':
            self.team = team
            self.groups = game.all_sprites, game.white_team
        else:
            self.team = team
            self.groups = game.all_sprites, game.black_team
        super().__init__(self.groups)

        self.pos = vec(x, y) * TILESIZE
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)


class Pawn(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)

        if team == 'white':
            self.image = pg.image.load(path.join(game.image_path, WHITE_PAWN))
        else:
            self.image = pg.image.load(path.join(game.image_path, BLACK_PAWN))
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
