import pygame
import random
from platforms import *


class PlatformsHandler(pygame.sprite.Group):
    def __init__(self, world_boundings, images_dir):
        super().__init__()
        self.world_boundings = world_boundings

        self.platforms_generator = \
            RandomPlatformGenerator(world_boundings, images_dir)

        self.last_height = world_boundings[3]
        self.difficult = 0

        while self.last_height > -MAX_PLAYER_JUMP_HEIGHT:
            pos = (random.randrange(world_boundings[0],
                                    world_boundings[2] - PLATFORM_WIDTH),
                   random.randrange(self.last_height - PLATFORM_HEIGHT - MAX_PLAYER_JUMP_HEIGHT,
                                    self.last_height - PLATFORM_HEIGHT - self.difficult))

            platform = self.platforms_generator.generate(pos)
            self.add(platform)
            self.last_height = pos[1]

    @property
    def difficult(self):
        return self._difficult

    @difficult.setter
    def difficult(self, value):
        value = min(MAX_PLAYER_JUMP_HEIGHT - 1, value)
        self._difficult = value

    def update(self, scroll_value, fps):
        if scroll_value:
            for platform in self.sprites():
                if platform.pos[1] > self.world_boundings[3]:
                    self.remove(platform)
            self.last_height += scroll_value

        while self.last_height > -MAX_PLAYER_JUMP_HEIGHT:
            pos = (random.randrange(self.world_boundings[0],
                                    self.world_boundings[2] - PLATFORM_WIDTH),
                   random.randrange(self.last_height - PLATFORM_HEIGHT - MAX_PLAYER_JUMP_HEIGHT,
                                    self.last_height - PLATFORM_HEIGHT - self.difficult))

            platform = self.platforms_generator.generate(pos)
            self.add(platform)
            self.last_height = pos[1]

        for platform in self.sprites():
            platform.rect.move_ip((0, scroll_value))

        super().update(fps)
