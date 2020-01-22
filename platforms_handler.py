import pygame
import random
from platforms import WeightsBasedPlatformGenerator
from config import *


class PlatformsHandler(pygame.sprite.Group):
    def __init__(self, world_boundings, images_dir, sounds_dir):
        super().__init__()

        self.world_boundings = world_boundings

        self.platform_generator = \
            WeightsBasedPlatformGenerator(world_boundings,
                                          images_dir,
                                          sounds_dir,
                                          START_PLATFORM_WEIGHTS)

        self.last_height = world_boundings[3]
        self.difficult = 0

        while self.last_height > -MAX_PLAYER_JUMP_HEIGHT:
            pos = (random.randrange(world_boundings[0],
                                    world_boundings[2] - PLATFORM_WIDTH),
                   self.__calc_next_height())

            platform = self.platform_generator.generate(pos)
            self.add(platform)
            self.last_height = pos[1]

    def __calc_next_height(self):
        min_h = int(self.last_height - PLATFORM_HEIGHT - MAX_PLAYER_JUMP_HEIGHT * self.difficult / MAX_DIFFICULT)
        max_h = int(self.last_height - PLATFORM_HEIGHT - MAX_PLAYER_JUMP_HEIGHT * min(self.difficult + 10, MAX_DIFFICULT) / MAX_DIFFICULT)

        if max_h == min_h:
            return max_h
        return random.randrange(max_h, min_h)

    @property
    def difficult(self):
        return self._difficult

    @difficult.setter
    def difficult(self, value):
        self._difficult = value

    def make_harder(self):
        if self._difficult == MAX_DIFFICULT:
            return
        self._difficult += 1
        self.platform_generator.make_harder()

    def update(self, scroll_value, fps):
        if scroll_value:
            for platform in self.sprites():
                platform.rect.move_ip((0, scroll_value))
                if platform.pos[1] > self.world_boundings[3]:
                    self.remove(platform)
            self.last_height += scroll_value

        while self.last_height > -MAX_PLAYER_JUMP_HEIGHT:
            pos_x = random.randrange(self.world_boundings[0],
                                     self.world_boundings[2] - PLATFORM_WIDTH)
            pos_y = self.__calc_next_height()

            platform = self.platform_generator.generate((pos_x, pos_y))
            self.add(platform)
            self.last_height = pos_y

        super().update(fps)
