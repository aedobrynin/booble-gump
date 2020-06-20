import os
import pygame
from sprite import Sprite
from player import Player
from platforms import StaticPlatform, VanishPlatform
from entities_handler import EntitiesHandler
from score_bar import ScoreBar
from config import HIGH_SCORE_PATH, MAIN_FONT_PATH, MENU_PLATFORM_HEIGHT
from config import PLAYER_HEIGHT, INVITATION, START_PLATFORM_JUMP_FORCE
from config import WORLD_BOUNDINGS, P_FALL_SPEED, FPS, LAST_SCORE_COLOR
from config import BACKGROUND, LEVEL_LINE, WINDOW_SIZE, P_IMAGES_DIR
from config import P_SOUNDS_DIR, M_IMAGES_DIR, M_SOUNDS_DIR, PLAYER_IMAGES_DIR
from config import PLAYER_SOUNDS_DIR, SCORE_BAR, LEFT_KEY, SHOOT_KEYS
from config import RIGHT_KEY, Direction, PLATFORM_WIDTH, PLATFORM_HEIGHT
from config import HIGH_SCORE_COLOR, WINDOW_WIDTH


def get_high_score():
    high_score = 0
    if os.path.exists(HIGH_SCORE_PATH):
        with open(HIGH_SCORE_PATH, "r") as file:
            try:
                high_score = int(file.readline().strip())
            except ValueError:
                print(f"Warning! Bad data at {HIGH_SCORE_PATH}")
    return high_score


def update_high_score(score):
    if score > get_high_score():
        with open(HIGH_SCORE_PATH, "w") as file:
            file.write(str(score))


def render_text(value_name, value, color):
    font = pygame.font.Font(MAIN_FONT_PATH, 32)
    text = font.render(f"{value_name}: {value}",
                       1,
                       pygame.Color(color))
    return text


def run_start_menu(player, entities_handler):
    player.pos = (150, MENU_PLATFORM_HEIGHT - PLAYER_HEIGHT - 5)

    entities_handler.extras.add(Sprite((30, MENU_PLATFORM_HEIGHT - 70),
                                       INVITATION))

    high_score_text = render_text("High score",
                                  get_high_score(),
                                  HIGH_SCORE_COLOR)
    pos_x = WINDOW_WIDTH // 2 - high_score_text.get_width() // 2
    entities_handler.extras.add(Sprite((pos_x, MENU_PLATFORM_HEIGHT - 200),
                                       high_score_text))

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
        scroll_value = P_FALL_SPEED // FPS
        if player.pos[1] + scroll_value >= MENU_PLATFORM_HEIGHT - 100:
            player.rect.move_ip((0, scroll_value))
        player.update_image()
        entities_handler.update(scroll_value, FPS)

        clock.tick(FPS)

    entities_handler.reset(reset_platforms=False)

    entities_handler.extras.add(Sprite((30, 2 * WORLD_BOUNDINGS[3] - 70),
                                       INVITATION))

    last_game_score_text = render_text("Last game score",
                                       score,
                                       LAST_SCORE_COLOR)
    pos_x = WINDOW_WIDTH // 2 - last_game_score_text.get_width() // 2
    entities_handler.extras.add(Sprite((pos_x, 2 * WORLD_BOUNDINGS[3] - 250),
                                       last_game_score_text))

    high_score_text = render_text("High score",
                                  get_high_score(),
                                  HIGH_SCORE_COLOR)
    pos_x = WINDOW_WIDTH // 2 - high_score_text.get_width() // 2
    entities_handler.extras.add(Sprite((pos_x, 2 * WORLD_BOUNDINGS[3] - 200),
                                       high_score_text))

    pos_x = -11
    pos_y = 2 * WORLD_BOUNDINGS[3]

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
        update_high_score(score)
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
    pygame.display.set_caption("Booble Gump")

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
