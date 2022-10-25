import pygame
from scoreboard import Scoreboard
from snake import Snake
from food import Food, FoodSpawner
import colors
import inputhandler

from sprites import SnakeSprite, FoodSprite
from common import Directions

# States: START, STOP, MOVE, EAT, GROW, DEAD, END
FSM_START = 0
FSM_STOP = 1
FSM_MOVE = 2
FSM_EAT = 3
FSM_GROW = 4
FSM_DEAD = 5
FSM_END = 6


def main(WIDTH, HEIGHT, SCALE):
    pygame.init()
    pygame.mixer.init()

    display = pygame.display.set_mode((SCALE * WIDTH, SCALE * (HEIGHT+1)))
    clock = pygame.time.Clock()

    INITIAL_SNAKE_SIZE = 3
    # snakes = [Snake([(WIDTH // 2 - x, HEIGHT // 2) for x in range(INITIAL_SNAKE_SIZE)], controls=1, color=colors.RED)]
    # snakes = [Snake([(WIDTH // 2 - x, HEIGHT // 2) for x in range(INITIAL_SNAKE_SIZE)], controls=2, color=colors.GREEN)]
    snakes = [Snake([(WIDTH // 2 - x, HEIGHT // 2 + 1) for x in range(INITIAL_SNAKE_SIZE)], controls=1, color=colors.BLUE),
              Snake([(WIDTH // 2 - x, HEIGHT // 2 - 1) for x in range(INITIAL_SNAKE_SIZE)], controls=2, color=colors.RED)]
    [snake.set_id(pos) for pos, snake in enumerate(snakes)]

    food_spawner = FoodSpawner()
    FOOD_AMOUNT = 4
    food = Food(stop_width=WIDTH, stop_height=HEIGHT)
    foods = [food_spawner.spawn_food(food) for _ in range(FOOD_AMOUNT)]

    all_sprites = pygame.sprite.Group()
    [all_sprites.add(SnakeSprite(snake, WIDTH, HEIGHT, SCALE)) for snake in snakes]
    [all_sprites.add(FoodSprite(food, WIDTH, HEIGHT, SCALE)) for food in foods]

    score = pygame.font.Font(None, 28)
    scoreboard = Scoreboard(len(snakes))

    eat_sound = pygame.mixer.Sound("eat_sound.wav")
    # pygame.mixer.music.load("background_music.mp3")
    # pygame.mixer.music.set_volume(0.1)
    # pygame.mixer.music.play(loops=-1)

    bg = pygame.image.load("background.png")
    bg = pygame.transform.scale(bg, (WIDTH*SCALE, HEIGHT*SCALE))
    # bg = colors.change_color(bg, colors.RED, WIDTH*SCALE, HEIGHT*SCALE)

    key_pressed = inputhandler.InputHandler()
    key = 0
    direction = Directions.RIGHT

    game_paused = False
    while not (sum([snake.dead for snake in snakes]) == len(snakes)):
        if pygame.event.get(pygame.QUIT):
            [snake.kill() for snake in snakes]

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key, direction = key_pressed.handleInput(event.key)
                if event.key == pygame.K_ESCAPE:
                    [snake.kill() for snake in snakes]
                # elif event.key == pygame.K_SPACE:
                #     game_paused = not game_paused

        if not game_paused:
            for snake in snakes:
                current_state = snake.get_current_state()
                if current_state == FSM_START:  # Starting the game
                    snake.set_current_state(FSM_STOP)
                elif current_state == FSM_STOP:  # Snakes are in standby, not moving
                    if snake.confirm_key_input(key):
                        snake.set_current_state(FSM_MOVE)
                elif current_state == FSM_MOVE:  # Snakes are moving
                    snake.move(key, direction)
                    snake.crashed_into_wall(WIDTH, HEIGHT)
                    if key == pygame.K_SPACE:
                        snake.set_current_state(FSM_STOP)
                    if snake.crashed_into_itself():
                        snake.set_current_state(FSM_DEAD)
                    if snake.check_food(foods):
                        snake.set_current_state(FSM_EAT)
                elif current_state == FSM_EAT:
                    eat_sound.play()
                    snake_body_coords = []
                    for s in snakes:
                        snake_body_coords += s.snake_body
                    while (foods[snake.food_to_eat].spawn() in snake_body_coords):
                        pass
                    scoreboard.update(snake.id)
                    snake.set_current_state(FSM_GROW)
                elif current_state == FSM_GROW:
                    snake.grow()
                    snake.set_current_state(FSM_MOVE)
                elif current_state == FSM_DEAD:
                    snake.kill()
                    snake.set_current_state(FSM_END)
                elif current_state == FSM_END:
                    continue

        display.fill("white")
        display.blit(bg, (0, 0))
        all_sprites.update()
        all_sprites.draw(display)

        pygame.draw.rect(display, colors.GRAY, pygame.Rect(0, SCALE*HEIGHT, SCALE*WIDTH, SCALE))
        for pos, snake in enumerate(snakes):
            display.blit(score.render("Snake" + str(pos) + ": " + str(scoreboard.get_score(pos)), True, colors.GREEN), (pos*150, SCALE*HEIGHT))

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    # main(80, 60, 10)
    main(40, 30, 20)
    # main(20,15,40)
