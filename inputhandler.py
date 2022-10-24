import pygame
from common import Directions


class InputHandler():
    def __init__(self):
        self.command = {
            pygame.K_w: Directions.UP,
            pygame.K_s: Directions.DOWN,
            pygame.K_a: Directions.LEFT,
            pygame.K_d: Directions.RIGHT,
            pygame.K_UP: Directions.UP,
            pygame.K_DOWN: Directions.DOWN,
            pygame.K_LEFT: Directions.LEFT,
            pygame.K_RIGHT: Directions.RIGHT
        }

    def handleInput(self, key):
        return (key, self.command.get(key, (0, 0)))
