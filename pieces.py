import pygame as pg
vec = pg.math.Vector2

from settings import *


def piece_at_pos(game, pos):
    for piece in game.all_pieces:
        if piece.pos == pos:
            return piece
    return None


class Piece(pg.sprite.Sprite):
    def __init__(self, game, team, x, y):
        self.groups = game.all_sprites, game.all_pieces, game.team_sprites[team]
        super().__init__(self.groups)

        self.team = team
        self.move_count = 0
        self.legal_moves = []

        self.pos = vec(x, y) * TILESIZE
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.rect.topleft = self.pos

    def move(self, destination):
        self.pos = destination.pos
        self.rect.topleft = destination.rect.topleft
        self.move_count += 1

    def generate_moves(self, game):
        return []


class Pawn(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.name = 'pawn'
        self.image = pg.image.load(game.pawn_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

    def generate_moves(self, game):
        moves = []
        start = vec(self.pos)
        forward = UP if self.team == 'white' else DOWN

        # One step
        test = start + forward
        piece = piece_at_pos(game, test)
        if not piece:
            moves.append(vec(test))
            # Two step
            if self.move_count == 0:
                test += forward
                piece = piece_at_pos(game, test)
                if not piece:
                    moves.append(vec(test))

        # Diagonal capture
        for test in (start + forward + RIGHT, start + forward + LEFT):
            piece = piece_at_pos(game, test)
            if piece:
                if piece.team != self.team:
                    moves.append(vec(test))

        # # Passant
        # else:
        #     if piece.team != self.team and piece.name == 'pawn' and piece.move_count == 1:
        #         moves.append(test + LEFT)
        #         moves.append(test + RIGHT)

        self.legal_moves = moves


class King(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.name = 'king'
        self.image = pg.image.load(game.king_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

    def generate_moves(self, game):
        moves = []
        start = vec(self.pos)

        for d in CARDINALS + ORDINALS:
            test = start + d
            piece = piece_at_pos(game, test)
            if piece:
                if piece.team != self.team:
                    moves.append(vec(test))
            else:
                moves.append(vec(test))
        self.legal_moves = moves


class Queen(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.name = 'queen'
        self.image = pg.image.load(game.queen_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

    def generate_moves(self, game):
        moves = []
        start = vec(self.pos)

        for d in CARDINALS + ORDINALS:
            test = start + d
            while 0 <= test.x < WIDTH and 0 <= test.y < HEIGHT:
                piece = piece_at_pos(game, test)
                if piece:
                    if piece.team != self.team:
                        moves.append(vec(test))
                    break
                else:
                    moves.append(vec(test))
                test += d
        self.legal_moves = moves


class Bishop(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.name = 'bishop'
        self.image = pg.image.load(game.bishop_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

    def generate_moves(self, game):
        moves = []
        start = vec(self.pos)

        for d in ORDINALS:
            test = start + d
            while 0 <= test.x < WIDTH and 0 <= test.y < HEIGHT:
                piece = piece_at_pos(game, test)
                if piece:
                    if piece.team != self.team:
                        moves.append(vec(test))
                    break
                else:
                    moves.append(vec(test))
                test += d
        self.legal_moves = moves


class Knight(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.name = 'knight'
        self.image = pg.image.load(game.knight_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

    def generate_moves(self, game):
        moves = []
        start = vec(self.pos)
        tests = [start + UP + UP + LEFT,
                     start + UP + UP + RIGHT,
                     start + DOWN + DOWN + LEFT,
                     start + DOWN + DOWN + RIGHT,
                     start + LEFT + LEFT + UP,
                     start + LEFT + LEFT + DOWN,
                     start + RIGHT + RIGHT + UP,
                     start + RIGHT + RIGHT + DOWN
                     ]
        for test in tests:
            piece = piece_at_pos(game, test)
            if piece:
                if piece.team != self.team:
                    moves.append(vec(test))
            else:
                moves.append(vec(test))
        self.legal_moves = moves


class Rook(Piece):
    def __init__(self, game, team, x, y):
        super().__init__(game, team, x, y)
        self.name = 'rook'
        self.image = pg.image.load(game.rook_img[team])
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))

    def generate_moves(self, game):
        moves = []
        start = vec(self.pos)

        for d in CARDINALS:
            test = start + d
            while 0 <= test.x < WIDTH and 0 <= test.y < HEIGHT:
                piece = piece_at_pos(game, test)
                if piece:
                    if piece.team != self.team:
                        moves.append(vec(test))
                    break
                else:
                    moves.append(vec(test))
                test += d
        self.legal_moves = moves
