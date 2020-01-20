import os
import pygame
import random
from sprite import Sprite
from config import *


class BasePlatform(Sprite):
    def __init__(self, pos, image_path):
        super().__init__(pos, pygame.image.load(image_path))
        self.mask = pygame.mask.from_surface(self.image)
        self.top = 0
        for j in range(self.image.get_height()):
            for i in range(self.image.get_width()):
                if self.mask.get_at((i, j)):
                    self.top = j
                    break

            if self.top != 0:
                break

        self.jump_force = PLATFORMS_JUMP_FORCE

    @property
    def top(self):
        return self._top + self.rect.top

    """This function sets only mask top,
        not the whole platform"""
    @top.setter
    def top(self, value):
        self._top = value

    @property
    def jump_force(self):
        return self._jump_force

    @jump_force.setter
    def jump_force(self, value):
        self._jump_force = value


class StaticPlatform(BasePlatform):
    def __init__(self, pos, image_path):
        super().__init__(pos, image_path)


class HorizontalMovingPlatform(BasePlatform):
    def __init__(self, pos, image_path):
        super().__init__(pos, image_path)
        self.speed = PLATFORM_MOVE_SPEED

        self.left_lim = random.randrange(WORLD_BOUNDINGS[0],
                                         WORLD_BOUNDINGS[2] // 2 - 50)
        self.right_lim = random.randrange(WORLD_BOUNDINGS[2] // 2,
                                          WORLD_BOUNDINGS[2] - 50)

        self.direction = random.choice((Direction.LEFT, Direction.RIGHT))

        if self.direction == Direction.LEFT:
            self.pos = self.left_lim, self.pos[1]
        else:
            self.pos = self.right_lim, self.pos[1]

    def update(self, fps):
        if self.direction == Direction.LEFT:
            self.pos = self.pos[0] - round(self.speed / fps), self.pos[1]
            if self.pos[0] <= self.left_lim:
                self.direction = Direction.RIGHT
                self.pos = self.left_lim, self.pos[1]
        else:
            self.pos = self.pos[0] + round(self.speed / fps), self.pos[1]
            if self.pos[0] >= self.right_lim:
                self.direction = Direction.LEFT
                self.pos = self.right_lim, self.pos[1]

PLATFORM_TYPES = ((StaticPlatform, "static"),
                  (HorizontalMovingPlatform, "moving"), )
CHOICE_WEIGHTS = (0.8, 0.2)


class RandomPlatformGenerator:
    def __init__(self, world_boundings, images_dir):
        self.world_boundings = world_boundings
        self.images_dir = images_dir

    def generate(self, platform_pos):
        platform_class, platform_class_name = random.choices(PLATFORM_TYPES,
                                                             weights=CHOICE_WEIGHTS)[0]

        if platform_pos is None:
            platform_x = random.randrange(self.world_boundings[0],
                                          self.world_boundings[2] - 40)
            platform_y = random.randrange(-MAX_PLAYER_JUMP_HEIGHT,
                                          self.world_boundings[1])
            platform_pos = (platform_x, platform_y)

        platform_image_path = os.path.join(self.images_dir,
                                           f"{platform_class_name}.png")
        return platform_class(platform_pos, platform_image_path)
