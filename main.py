import os
import pygame
from Player import Player
from Platform import Platform


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 450, 800
FPS = 60

DATA_DIR = "./data"
IMAGES_DIR = os.path.join(DATA_DIR, "images")


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    platforms.add(Platform((0, 500), os.path.join(IMAGES_DIR, "platforms", "solid.png")

    player = Player((0, 0), os.path.join(IMAGES_DIR, "player", "blue"))
    all_sprites.add(player)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color("white"))
        all_sprites.draw(screen)
        pygame.display.flip()

        platforms.update(FPS)
        player.update(platforms, FPS)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
