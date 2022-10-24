from enum import Enum
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d


class Directions(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Controls():
    KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
    WASD = [K_w, K_s, K_a, K_d]
