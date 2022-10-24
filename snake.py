from common import Directions, Controls
from scoreboard import Scoreboard
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d
import logging


class Snake():
    def __init__(self, body=[], controls=1, color=None):
        self.snake_body = body  # List of coordinates of snake's body
        self.direction = Directions.RIGHT
        self.snake_length = len(body)
        self.dead = False

        self.color = color
        self.score = Scoreboard()
        self.controls = controls  # 1 - arrow keys, 2 - WASD

    def move(self, direction: Directions = None):
        """Add one piece, pop one out."""

        if direction:
            self.direction = direction

        # Sum current head position with direction vector
        new_head = tuple(sum(t) for t in zip(self.snake_body[0], self.direction.value))

        # Insert new head at the head of the list
        self.snake_body[0:0] = [new_head]

        # Remove snake_body tails
        while len(self.snake_body) > self.snake_length:
            self.snake_body.pop()

    def crashed_into_itself(self):
        # Check we didn't eat our selves
        if self.snake_body.count(self.snake_body[0]) > 1:
            logging.info("Snake eats self")
            self.dead = True

    def kill(self):
        logging.info("Snake died")
        self.dead = True

    def eat(self, food_position):
        if food_position == self.snake_body[0]:
            self.snake_length += 1
            self.score.update()
            return True
        return False

    def get_score(self):
        return self.score.get_score()

    def crashed_into_wall(self, width, height):
        for pos, snake_part in enumerate(self.snake_body):
            self.wall_interaction(pos, snake_part, width, height)

    def wall_interaction(self, pos, snake_part, width, height):
        if snake_part[0] > width-1:
            self.snake_body[pos] = (0, snake_part[1])

        elif snake_part[0] < 0:
            self.snake_body[pos] = (width-1, snake_part[1])

        elif snake_part[1] > height-1:
            self.snake_body[pos] = (snake_part[0], 0)

        elif snake_part[1] < 0:
            self.snake_body[pos] = (snake_part[0], height-1)

    def confirm_key_input(self, key):
        return (self.controls == 1 and key in Controls.KEYS) or \
            (self.controls == 2 and key in Controls.WASD)

    def check_movement(self, direction):
        return not ((self.direction == Directions.RIGHT and direction == Directions.LEFT) or
                    (self.direction == Directions.LEFT and direction == Directions.RIGHT) or
                    (self.direction == Directions.UP and direction == Directions.DOWN) or
                    (self.direction == Directions.DOWN and direction == Directions.UP))
