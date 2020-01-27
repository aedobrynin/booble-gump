import os
import pygame
from player import Player, Direction
from platforms import StaticPlatform
from entities_handler import EntitiesHandler
from config import *


def run_start_menu(player, entities_handler):
    player.pos = (150, MENU_PLATFORM_HEIGHT - PLAYER_HEIGHT - 5)

    pos_x = -11
    pos_y = MENU_PLATFORM_HEIGHT

    while pos_x <= WORLD_BOUNDINGS[2]:
        platform = StaticPlatform((pos_x, pos_y),
                                  entities_handler.platform_generator.images["static"],
                                  entities_handler.platform_generator.masks["static"],
                                  entities_handler.platform_generator.sounds["pop"])

        if pos_x // PLATFORM_WIDTH == 3:
            platform.jump_force = 1500

        entities_handler.platforms.add(platform)

        pos_x += PLATFORM_WIDTH

    dummy = StaticPlatform((150, WORLD_BOUNDINGS[0] - 100),
                            entities_handler.platform_generator.images["static"],
                            entities_handler.platform_generator.masks["static"],
                            entities_handler.platform_generator.sounds["pop"])


    entities_handler.platforms.add(dummy)
    entities_handler.last_platform = dummy


def run_game_lost_menu(screen, player, entities_handler, score):
    entities_handler.generate = False

    clock = pygame.time.Clock()
    while entities_handler.platforms:
        draw(screen, player, entities_handler)
        scroll_value = P_FALL_SPEED / FPS
        if player.pos[1] > MENU_PLATFORM_HEIGHT // 2:
            player.rect.move_ip((0, scroll_value))
        entities_handler.update(scroll_value, FPS)

        clock.tick(FPS)

    entities_handler.reset(reset_platforms=False)

    pos_x = -11
    pos_y = WORLD_BOUNDINGS[3]

    while pos_x <= WORLD_BOUNDINGS[2]:
        platform = StaticPlatform((pos_x, pos_y),
                                  entities_handler.platform_generator.images["static"],
                                  entities_handler.platform_generator.masks["static"],
                                  entities_handler.platform_generator.sounds["pop"])

        if pos_x // PLATFORM_WIDTH == 3:
            platform.jump_force = 1800

        entities_handler.platforms.add(platform)
        pos_x += PLATFORM_WIDTH

    while entities_handler.platforms.sprites()[0].pos[1] > MENU_PLATFORM_HEIGHT:
        draw(screen, player, entities_handler)
        scroll_value = \
            max(MENU_PLATFORM_HEIGHT - entities_handler.platforms.sprites()[0].pos[1],
                P_FALL_SPEED / FPS)
        entities_handler.update(scroll_value, FPS)
        player.rect.move_ip((0, -scroll_value))
        clock.tick(FPS)

    dummy = StaticPlatform((230, WORLD_BOUNDINGS[0] - 100),
                           entities_handler.platform_generator.images["static"],
                           entities_handler.platform_generator.masks["static"],
                           entities_handler.platform_generator.sounds["pop"])

    entities_handler.platforms.add(dummy)
    entities_handler.last_platform = dummy

    """
    while player.rect.bottom < MENU_PLATFORM_HEIGHT - 10:
        val = min(MENU_PLATFORM_HEIGHT - 10 - player.rect.bottom,
                  -P_FALL_SPEED / FPS)
        player.rect.move_ip((0, val))
        clock.tick(FPS)
    """
    player.vertical_speed = -P_FALL_SPEED
    player.dead = False
    entities_handler.generate = True


def draw(screen, player, entities_handler):
        screen.blit(BACKGROUND, (0, 0))
        entities_handler.draw(screen)
        player.draw(screen)

        pygame.display.flip()


def update(screen, player, entities_handler, score):
        if player.dead is True:
            run_game_lost_menu(screen, player, entities_handler, score)
            score = 0
        else:
            player.update(entities_handler.platforms,
                          entities_handler.monsters,
                          FPS)

        scroll_value = 0
        if player.pos[1] < LEVEL_LINE:
            scroll_value = LEVEL_LINE - player.pos[1]
            player.rect.top = LEVEL_LINE
            if score // 2000 < (score + scroll_value) // 2000:
                entities_handler.make_harder()
            score += scroll_value
            #print(score)

        entities_handler.update(scroll_value, FPS)

        return score


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    entities_handler = EntitiesHandler(P_IMAGES_DIR,
                                       P_SOUNDS_DIR,
                                       M_IMAGES_DIR,
                                       M_SOUNDS_DIR)

    player_shoot_sound = pygame.mixer.Sound(PLAYER_SHOOT_SOUND_PATH)
    player_death_sound = pygame.mixer.Sound(PLAYER_DEATH_SOUND_PATH)

    player = Player((150, 480),
                    PLAYER_IMAGES_DIR,
                    player_shoot_sound,
                    player_death_sound)


    run_start_menu(player, entities_handler)

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

        draw(screen, player, entities_handler)
        score = update(screen, player, entities_handler, score)

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
