import os
import pygame
from player import Player, Direction
from platforms import StaticPlatform, VanishPlatform
from entities_handler import EntitiesHandler
from score_bar import ScoreBar
from config import *


def run_start_menu(player, entities_handler):
    player.pos = (150, MENU_PLATFORM_HEIGHT - PLAYER_HEIGHT - 5)

    pos_x = -11
    pos_y = MENU_PLATFORM_HEIGHT

    pg = entities_handler.platform_generator

    while pos_x <= WORLD_BOUNDINGS[2]:
        if pos_x // PLATFORM_WIDTH == 3:
            platform = StaticPlatform((pos_x, pos_y),
                                      pg.images["start"],
                                      pg.masks["start"],
                                      pg.sounds["pop"])
            platform.jump_force = START_PLATFORM_JUMP_FORCE
        else:
            platform = StaticPlatform((pos_x, pos_y),
                                      pg.images["static"],
                                      pg.masks["static"],
                                      pg.sounds["pop"])

        entities_handler.platforms.add(platform)

        pos_x += PLATFORM_WIDTH

    dummy = StaticPlatform((150, WORLD_BOUNDINGS[0] - 100),
                           pg.images["static"],
                           pg.masks["static"],
                           pg.sounds["pop"])

    entities_handler.platforms.add(dummy)
    entities_handler.last_platform = dummy

    return -1090


def run_game_lost_menu(screen, player, entities_handler, score, score_bar):
    entities_handler.generate = False

    clock = pygame.time.Clock()
    while entities_handler.platforms:
        draw(screen, player, entities_handler, score_bar)
        scroll_value = P_FALL_SPEED / FPS
        if player.pos[1] + scroll_value >= MENU_PLATFORM_HEIGHT - 100:
            player.rect.move_ip((0, scroll_value))
        player.update_image()
        entities_handler.update(scroll_value, FPS)

        clock.tick(FPS)

    entities_handler.reset(reset_platforms=False)

    pos_x = -11
    pos_y = WORLD_BOUNDINGS[3]

    pg = entities_handler.platform_generator

    while pos_x <= WORLD_BOUNDINGS[2]:
        if pos_x // PLATFORM_WIDTH == 3:

            defence_platform = VanishPlatform((pos_x, pos_y - PLATFORM_HEIGHT),
                                              pg.images["vanish"],
                                              pg.masks["vanish"],
                                              pg.sounds["vanish"])

            entities_handler.platforms.add(defence_platform)

            platform = StaticPlatform((pos_x, pos_y),
                                      pg.images["start"],
                                      pg.masks["start"],
                                      pg.sounds["pop"])

            platform.jump_force = START_PLATFORM_JUMP_FORCE
        else:
            platform = StaticPlatform((pos_x, pos_y),
                                      pg.images["static"],
                                      pg.masks["static"],
                                      pg.sounds["pop"])

        entities_handler.platforms.add(platform)
        pos_x += PLATFORM_WIDTH

    while entities_handler.platforms.sprites()[0].pos[1] > MENU_PLATFORM_HEIGHT:
        draw(screen, player, entities_handler, score_bar)
        scroll_value = \
            max(MENU_PLATFORM_HEIGHT - entities_handler.platforms.sprites()[0].pos[1],
                P_FALL_SPEED / FPS)
        entities_handler.update(scroll_value, FPS)

        if player.rect.bottom - scroll_value < MENU_PLATFORM_HEIGHT - 10:
            player.rect.move_ip((0, -scroll_value))
        player.update_image()
        clock.tick(FPS)

    dummy = StaticPlatform((230, WORLD_BOUNDINGS[0] - 100),
                           pg.images["static"],
                           pg.masks["static"],
                           pg.sounds["pop"])

    entities_handler.platforms.add(dummy)
    entities_handler.last_platform = dummy

    player.vertical_speed = -P_FALL_SPEED * 0.3
    player.dead = False
    entities_handler.generate = True

    return -1090


def draw(screen, player, entities_handler, score_bar):
    screen.blit(BACKGROUND, (0, 0))

    entities_handler.draw(screen)
    player.draw(screen)

    screen.blit(score_bar, (0, 0))
    pygame.display.flip()


def update(screen, player, entities_handler, score, score_bar):
    if player.dead is True:
        score = run_game_lost_menu(screen,
                                   player,
                                   entities_handler,
                                   score,
                                   score_bar)
    else:
        player.update(entities_handler.platforms,
                      entities_handler.monsters,
                      FPS)

    scroll_value = 0
    if player.pos[1] < LEVEL_LINE:
        scroll_value = LEVEL_LINE - player.pos[1]
        player.rect.top = LEVEL_LINE
        if score > 0 and score // 2000 < (score + scroll_value) // 2000:
            entities_handler.make_harder()
        score += scroll_value

    entities_handler.update(scroll_value, FPS)

    score_bar.score = max(0, score)

    return score


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    entities_handler = EntitiesHandler(P_IMAGES_DIR,
                                       P_SOUNDS_DIR,
                                       M_IMAGES_DIR,
                                       M_SOUNDS_DIR)

    player = Player((150, 480),
                    PLAYER_IMAGES_DIR,
                    PLAYER_SOUNDS_DIR)

    score_bar = ScoreBar(320, 46, 0, SCORE_BAR)

    score = run_start_menu(player, entities_handler)
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
                elif event.key in SHOOT_KEYS:
                    player.shoot()

            if event.type == pygame.KEYUP:
                if (event.key == LEFT_KEY and
                    player.horizontal_direction == Direction.LEFT) or\
                   (event.key == RIGHT_KEY and
                        player.horizontal_direction == Direction.RIGHT):
                    player.horizontal_direction = Direction.STALL

        draw(screen, player, entities_handler, score_bar)
        score = update(screen, player, entities_handler, score, score_bar)

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
