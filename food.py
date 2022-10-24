import random


class Food():
    def __init__(self, start_width=0, stop_width=0, start_height=0, stop_height=0):
        self.start_width = start_width
        self.stop_width = stop_width
        self.start_height = start_height
        self.stop_height = stop_height

        self.spawn()

    def spawn(self):
        self.pos = (
            random.randrange(self.start_width, self.stop_width),
            random.randrange(self.start_height, self.stop_height),
        )
        return self.pos

    def get_pos(self):
        return self.pos

    def clone(self):
        return Food(self.start_width, self.stop_width, self.start_height, self.stop_height)


class Spawner:
    def spawn_food(self, prototype) -> Food:
        return prototype.clone()
