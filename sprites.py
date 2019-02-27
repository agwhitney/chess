import pygame as pg
vec = pg.math.Vector2

from os import path

from settings import *


class Piece(pg.sprite.Sprite):
    def __init__(self, game, team, x, y):
        self.groups = game.all_sprites, game.all_pieces, game.team_sprites[team]
        super().__init__(self.groups)

        self.pos = vec(x, y) * TILESIZE
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.rect.topleft = self.pos

    def move(self, destination):
        self.pos = destination.pos
        self.rect.topleft = destination.rect.topleft


class Pawn(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.image = pg.image.load(game.pawn_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))


class King(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.image = pg.image.load(game.king_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))


class Queen(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.image = pg.image.load(game.queen_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))


class Bishop(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.image = pg.image.load(game.bishop_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))


class Knight(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.image = pg.image.load(game.knight_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))


class Rook(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.image = pg.image.load(game.rook_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
