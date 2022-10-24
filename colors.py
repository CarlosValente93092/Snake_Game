import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def change_color(surface, color, width, height):
    color += (0,)
    for w in range(width):
        for h in range(height):
            surface.set_at((w, h), tuple([min(x+y, 255) for x, y in zip(surface.get_at((w, h)), color)]))
    return surface
