from enum import Enum


class Team(Enum):
    WHITE = 1
    BLACK = 2


def switch_teams(color):
    if color == Team.WHITE:
        return Team.BLACK
    elif color == Team.BLACK:
        return Team.WHITE
