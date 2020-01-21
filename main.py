import os
import pygame
from player import Player, Direction
from platforms_handler import PlatformsHandler
from config import *


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    platforms_handler = PlatformsHandler(WORLD_BOUNDINGS,
                                         PLATFORMS_DIR)

    player = Player((150, 500),
                    PLAYER_DIR,
                    WORLD_BOUNDINGS)
    player.vertical_speed = -800

    clock = pygame.time.Clock()
    running = True
    score = 0

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

        screen.blit(BACKGROUND, (0, 0))
        platforms_handler.draw(screen)
        player.draw(screen)

        pygame.display.flip()

        player.update(platforms_handler, FPS)

        if player.pos[1] > WORLD_BOUNDINGS[3]:
            print("game_over")
            running = False

        scroll_value = 0
        if player.pos[1] < LEVEL_LINE:
            scroll_value = LEVEL_LINE - player.pos[1]
            player.pos = player.pos[0], LEVEL_LINE
            if score % 1000 < scroll_value:
                platforms_handler.difficult += 5

                print("DIFFICULT UPDATE")
            score += scroll_value
            print(score)

        platforms_handler.update(scroll_value, FPS)

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
