import pygame
from snake import Snake
from food import Food, Spawner
import colors
import inputhandler

from sprites import SnakeSprite, FoodSprite
from common import Directions


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

    food_spawner = Spawner()
    FOOD_AMOUNT = 2
    food = Food(stop_width=WIDTH, stop_height=HEIGHT)
    foods = [food_spawner.spawn_food(food) for _ in range(FOOD_AMOUNT)]

    all_sprites = pygame.sprite.Group()
    [all_sprites.add(SnakeSprite(snake, WIDTH, HEIGHT, SCALE)) for snake in snakes]
    [all_sprites.add(FoodSprite(food, WIDTH, HEIGHT, SCALE)) for food in foods]

    score1 = pygame.font.Font(None, 28)

    eat_sound = pygame.mixer.Sound("eat_sound.wav")
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)

    bg = pygame.image.load("background.png")
    bg = pygame.transform.scale(bg, (WIDTH*SCALE, HEIGHT*SCALE))
    # bg = colors.change_color(bg, colors.RED, WIDTH*SCALE, HEIGHT*SCALE)

    key_pressed = inputhandler.InputHandler()

    game_paused = True
    while not (sum(dead_list := [snake.dead for snake in snakes]) == len(dead_list)):
        if pygame.event.get(pygame.QUIT):
            [snake.kill() for snake in snakes]

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key, direction = key_pressed.handleInput(event.key)
                if event.key == pygame.K_ESCAPE:
                    [snake.kill() for snake in snakes]
                elif event.key == pygame.K_SPACE:
                    game_paused = not game_paused

        if not game_paused:
            for snake in snakes:
                if snake.dead:
                    continue

                if isinstance(direction, Directions) and snake.confirm_key_input(key) and snake.check_movement(direction):
                    snake.move(direction)
                else:
                    snake.move()

                snake.crashed_into_wall(WIDTH, HEIGHT)
                snake.crashed_into_itself()

                for food in foods:
                    if snake.eat(food.get_pos()):
                        eat_sound.play()
                        # loop until food spawns away from snake body
                        while (food.spawn() in snake.snake_body):
                            pass

        display.fill("white")
        display.blit(bg, (0, 0))
        all_sprites.update()
        all_sprites.draw(display)

        pygame.draw.rect(display, colors.GRAY, pygame.Rect(0, SCALE*HEIGHT, SCALE*WIDTH, SCALE))
        for pos, snake in enumerate(snakes):
            display.blit(score1.render("Snake" + str(pos) + ": " + str(snake.get_score()), True, colors.GREEN), (pos*150, SCALE*HEIGHT))

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    # main(80, 60, 10)
    main(40, 30, 20)
    # main(20,15,40)
