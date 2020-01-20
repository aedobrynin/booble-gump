import os
import pygame
from player import Player, Direction
from platforms_handler import PlatformsHandler


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 400, 600
WORLD_BOUNDINGS = (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
LEVEL_LINE = WINDOW_HEIGHT // 2
FPS = 60

LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

DATA_DIR = "./data"
IMAGES_DIR = os.path.join(DATA_DIR, "images")


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    platforms_handler = PlatformsHandler(WORLD_BOUNDINGS)

    player = Player((300, 500),
                    os.path.join(IMAGES_DIR, "player", "blue"),
                    WORLD_BOUNDINGS)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == LEFT_KEY:
                    player.horizontal_direction = Direction.LEFT
                elif event.key == RIGHT_KEY:
                    player.horizontal_direction = Direction.RIGHT

            if event.type == pygame.KEYUP:
                if (event.key == LEFT_KEY and
                     player.horizontal_direction == Direction.LEFT) or\
                   (event.key == RIGHT_KEY and
                     player.horizontal_direction == Direction.RIGHT):
                    player.horizontal_direction = Direction.STALL

        screen.fill(pygame.Color("white"))
        platforms_handler.draw(screen)
        player.draw(screen)

        pygame.display.flip()

        player.update(platforms_handler, FPS)

        scroll_value = 0
        if player.pos[1] < LEVEL_LINE:
            scroll_value = abs(player.pos[1] - LEVEL_LINE)
            player.pos = player.pos[0], LEVEL_LINE

        platforms_handler.update(scroll_value, FPS)

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
