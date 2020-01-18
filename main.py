import os
import pygame
from player import Player, Direction
from platform import Platform


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 450, 800
FPS = 60

LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

DATA_DIR = "./data"
IMAGES_DIR = os.path.join(DATA_DIR, "images")


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    for coord in ((0, 500), (100, 200), (300, 700)):
        platform = Platform(coord,
                            os.path.join(IMAGES_DIR, "platforms", "solid.png"))
        platforms.add(platform)
        all_sprites.add(platform)

    player = Player((0, 0),
                    os.path.join(IMAGES_DIR, "player", "blue"),
                    (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    all_sprites.add(player)
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
        all_sprites.draw(screen)
        pygame.display.flip()

        platforms.update(FPS)
        player.update(platforms, FPS)

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
