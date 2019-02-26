import pygame as pg
vec = pg.math.Vector2

from settings import *


# class Team:
#     white = ('white', WHITE)
#     black = ('black', BLACK)
#
#     def __init__(self, color):
#         if color:
#             self.color, self.fill = white
#         else:
#             self.color, self.fill = black
#
#     def switch(self):
#         if self.color == 'white':
#             self.color, self.fill = black
#         elif self.color == 'black':
#             self.color, self.fill = white
#

class Square(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        if color:
            self.color = 'white'
            self.f = WHITE
        else:
            self.color = 'black'
            self.f = BLACK

        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.pos = vec(x, y) * TILESIZE
        self.rect = pg.Rect((x, y), (TILESIZE, TILESIZE))
        self.image = pg.Surface.fill(self.f, self.rect)
