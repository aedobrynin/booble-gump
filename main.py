import os
import pygame
from player import Player, Direction
from entities_handler import EntitiesHandler
from config import *


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    entities_handler = EntitiesHandler(P_IMAGES_DIR,
                                       P_SOUNDS_DIR,
                                       M_IMAGES_DIR,
                                       M_SOUNDS_DIR)

    player_shoot_sound = pygame.mixer.Sound(PLAYER_SHOOT_SOUND_PATH)
    player = Player((150, 480),
                    PLAYER_IMAGES_DIR,
                    player_shoot_sound)

    player.vertical_speed = -835

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
                elif event.key in SHOOT_KEYS:
                    player.shoot()

            if event.type == pygame.KEYUP:
                if (event.key == LEFT_KEY and
                    player.horizontal_direction == Direction.LEFT) or\
                   (event.key == RIGHT_KEY and
                        player.horizontal_direction == Direction.RIGHT):
                    player.horizontal_direction = Direction.STALL

        screen.blit(BACKGROUND, (0, 0))
        entities_handler.draw(screen)
        player.draw(screen)

        pygame.display.flip()

        player.update(entities_handler.platforms,
                      entities_handler.monsters,
                      FPS)

        if player.pos[1] + PLAYER_HEIGHT > WORLD_BOUNDINGS[3]:
            print("game_over")
            running = False

        scroll_value = 0
        if player.pos[1] < LEVEL_LINE:
            scroll_value = LEVEL_LINE - player.pos[1]
            player.pos = player.pos[0], LEVEL_LINE
            if score // 2000 < (score + scroll_value) // 2000:
                entities_handler.make_harder()
            score += scroll_value
            print(score)

        entities_handler.update(scroll_value, FPS)

        # import time
        # time.sleep(0.1)

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
