import os
import pygame
from player import Player, Direction
from platforms_handler import PlatformsHandler


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 450, 800
WORLD_BOUNDINGS = (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
FPS = 60

LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

DATA_DIR = "./data"
IMAGES_DIR = os.path.join(DATA_DIR, "images")


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    platforms_handler = PlatformsHandler(WORLD_BOUNDINGS)

    player = Player((300, 650),
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

            if event.type == pygame.KEYUP and\
               event.key in (LEFT_KEY, RIGHT_KEY):
                player.horizontal_direction = Direction.STALL

        screen.fill(pygame.Color("white"))
        platforms_handler.draw(screen)
        player.draw(screen)

        pygame.display.flip()

        platforms_handler.move(1)
        player.update(platforms_handler, FPS)

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
