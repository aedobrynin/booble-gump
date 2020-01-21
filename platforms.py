import os
import pygame
import random
from sprite import Sprite
from config import *


class BasePlatform(Sprite):
    def __init__(self, pos, image):
        super().__init__(pos, image)
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

    def collision_react(self):
        pass


class StaticPlatform(BasePlatform):
    def __init__(self, pos, image):
        super().__init__(pos, image)


class HorizontalMovingPlatform(BasePlatform):
    def __init__(self, pos, image):
        super().__init__(pos, image)
        self.speed = PLATFORM_MOVE_SPEED

        self.left_lim = WORLD_BOUNDINGS[0] + 15

        self.right_lim = WORLD_BOUNDINGS[2] - 70

        self.direction = random.choice((Direction.LEFT, Direction.RIGHT))

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


class VanishPlatform(BasePlatform):
    def __init__(self, pos, image):
        super().__init__(pos, image)

    def collision_react(self):
        self.kill()


PLATFORM_TYPES = ((StaticPlatform, "static"),
                  (HorizontalMovingPlatform, "moving"),
                  (VanishPlatform, "vanish"))
CHOICE_WEIGHTS = (0.5, 0.3, 0.2)


class RandomPlatformGenerator:
    def __init__(self, world_boundings, images_dir):
        self.world_boundings = world_boundings
        self.load_images(images_dir)

    def load_images(self, images_dir):
        self.images = dict()
        for filename in os.listdir(images_dir):
            class_name = filename.rsplit('.')[0]
            self.images[class_name] = \
                pygame.image.load(os.path.join(images_dir, filename))

    def generate(self, platform_pos):
        platform_class, platform_class_name = \
            random.choices(PLATFORM_TYPES, weights=CHOICE_WEIGHTS)[0]

        if platform_pos is None:
            platform_x = random.randrange(self.world_boundings[0],
                                          self.world_boundings[2] - 40)
            platform_y = random.randrange(-MAX_PLAYER_JUMP_HEIGHT,
                                          self.world_boundings[1])
            platform_pos = (platform_x, platform_y)

        return platform_class(platform_pos, self.images[platform_class_name])
