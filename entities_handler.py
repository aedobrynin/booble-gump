import pygame
from random import randrange
from platforms import WeightBasedPlatformGenerator
from platforms import HorizontalMovingPlatform
from monsters import WeightBasedMonsterGenerator
from config import *


class EntitiesHandler:
    def __init__(self, p_images_dir, p_sounds_dir,
                 m_images_dir, m_sounds_dir):
        self.generate = True

        self.platforms = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.extras = pygame.sprite.Group()

        self.last_platform = None
        self.last_monster = None

        self.platform_generator = \
            WeightBasedPlatformGenerator(p_images_dir,
                                         p_sounds_dir,
                                         P_INITIAL_WEIGHTS)

        self.monster_generator = \
            WeightBasedMonsterGenerator(m_images_dir,
                                        m_sounds_dir,
                                        M_INITIAL_WEIGHTS)

        self.difficult = 0

    def make_harder(self):
        self.platform_generator.make_harder()
        self.spawn_monster()
        self.difficult = min(self.difficult + 1, MAX_DIFFICULT)

    def __func(self, difficult):
        if self.last_platform is None:
            last_platform_height = WORLD_BOUNDINGS[3]
        else:
            last_platform_height = self.last_platform.pos[1]

        return int(last_platform_height - PLATFORM_HEIGHT -
                   MAX_PLAYER_JUMP_HEIGHT * difficult / MAX_DIFFICULT)

    def __calc_next_pos(self):
        pos_x = randrange(WORLD_BOUNDINGS[0],
                          WORLD_BOUNDINGS[2] - PLATFORM_WIDTH)

        min_h = self.__func(min(self.difficult + 10, MAX_DIFFICULT))
        max_h = self.__func(self.difficult)

        if self.last_monster is not None and\
           isinstance(self.last_monster.platform, HorizontalMovingPlatform):
            max_h = min(max_h, self.last_monster.pos[1] - PLATFORM_HEIGHT)

        if max_h <= min_h:
            pos_y = max_h
        else:
            pos_y = randrange(min_h, max_h)

        return pos_x, pos_y

    def update_platforms(self, scroll_value, fps):
        if scroll_value:
            for platform in self.platforms:
                platform.rect.move_ip((0, scroll_value))
                if platform.pos[1] > P_ALIVE_COEFFICIENT * WORLD_BOUNDINGS[3] or\
                   platform.pos[1] < -200:
                    platform.kill()

        if not self.generate:
            self.platforms.update(fps)
            return

        while self.last_platform is None or\
                self.last_platform.pos[1] > -MAX_PLAYER_JUMP_HEIGHT:
            pos = self.__calc_next_pos()
            platform = self.platform_generator.generate(pos)

            if isinstance(platform, HorizontalMovingPlatform) and\
               (self.last_monster is not None and
                    self.last_monster.pos[1] <= platform.rect.bottom):
                continue

            collision = \
                pygame.sprite.spritecollideany(platform,
                                               self.monsters,
                                               collided=pygame.sprite.collide_mask)

            if collision is None:
                self.platforms.add(platform)
                self.last_platform = platform

        self.platforms.update(fps)

    def spawn_monster(self):
        if not self.generate:
            return

        monster = self.monster_generator.generate(self.last_platform)
        self.monsters.add(monster)
        self.last_monster = monster

    def update_monsters(self, scroll_value, fps):
        for monster in self.monsters:
            monster.rect.move_ip((0, scroll_value))
            if monster.pos[1] > WORLD_BOUNDINGS[3]:
                monster.kill()
                if self.last_monster == monster:
                    self.last_monster = None

        self.monsters.update(fps)

    def update_extras(self, scroll_value, fps):
        for extra in self.extras:
            extra.rect.move_ip((0, scroll_value))
            if extra.pos[1] > 2 * WORLD_BOUNDINGS[3]:
                extra.kill()

        self.extras.update(fps)

    def update(self, scroll_value, fps):
        self.update_platforms(scroll_value, fps)
        self.update_monsters(scroll_value, fps)
        self.update_extras(scroll_value, fps)

    def draw(self, surface):
        self.platforms.draw(surface)
        self.monsters.draw(surface)
        self.extras.draw(surface)

    def reset(self, reset_platforms=True):
        if reset_platforms:
            self.platforms.empty()
        self.platform_generator.reset()

        self.monsters.empty()
        self.monster_generator.reset()

        self.extras.empty()

        self.last_platform = None
        self.last_monster = None

        self.difficult = 0
