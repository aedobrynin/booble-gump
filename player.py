import os
from enum import Enum
import pygame
from Sprite import Sprite



class Direction(Enum):
    LEFT = -1
    STALL = 0
    RIGHT = 1


class Player(Sprite):
    def __init__(self, pos, images_dir, world_boundings):
        self.load_images(images_dir)
        self.vertical_speed = 0

        self.horizontal_speed = 0
        self.horizontal_force = 60
        self.horizontal_direction = Direction.STALL

        #  self.mask = None
        #  TODO

        self.weight = 10

        self.gravitation = 9.8
        self.acceleration = 0
        self.image_code = "right"

        self.bounce_step = -1

        self.world_boundings = world_boundings

        super().__init__(pos, self.images[self.image_code])

    def load_images(self, images_dir):
        self.images = dict()
        for filename in os.listdir(images_dir):
            state_name = filename.rsplit('.')[0]
            self.images[state_name] = \
                pygame.image.load(os.path.join(images_dir, filename))

    @property
    def horizontal_direction(self):
        return self._horizontal_direction

    @horizontal_direction.setter
    def horizontal_direction(self, value):
        self._horizontal_direction = value

    def __update_image(self):
        if self.horizontal_direction == Direction.LEFT:
            self.image_code = "left"
        elif self.horizontal_direction == Direction.RIGHT:
            self.image_code = "right"

        if self.bounce_step == 15:
            self.bounce_step = -1

        if self.bounce_step != -1:
            self.image = self.images[self.image_code + "-bounce"]
            self.bounce_step += 1
        else:
            self.image = self.images[self.image_code]

    def bounce(self):
        self.bounce_step = 0

    def __update_horizontal_speed(self):
        if self.horizontal_direction == Direction.STALL:
            self.horizontal_speed = 0
        elif self.horizontal_direction == Direction.LEFT:
            self.horizontal_speed = -self.horizontal_force / self.weight
        elif self.horizontal_direction == Direction.RIGHT:
            self.horizontal_speed = self.horizontal_force / self.weight

    def __update_vertical_speed(self, fps):
        self.acceleration += self.gravitation / self.weight * (1 / fps)
        self.vertical_speed += self.acceleration

    def __check_boundings(self):
        if self.rect.left + self.rect.width // 2 < self.world_boundings[0]:
            self.rect.right = self.world_boundings[2] + self.rect.width // 2

        if self.rect.left + self.rect.width // 2 > self.world_boundings[2]:
            self.rect.left = self.world_boundings[0] - self.rect.width // 2

        if self.rect.bottom > self.world_boundings[3]:
            self.rect.bottom = self.world_boundings[0]
            self.acceleration = 0
            self.vertical_speed = 0

    def update(self, platforms, fps):
        self.__update_image()

        self.__update_vertical_speed(fps)
        self.__update_horizontal_speed()

        self.rect.move_ip((self.horizontal_speed, self.vertical_speed))

        self.__check_boundings()

        if self.vertical_speed <= 0:
            return

        collision = None
        for platform in platforms:
            if pygame.sprite.collide_mask(self, platform) is not None:
                collision = platform
                break

        if collision is None:
            return

        self.acceleration = 0
        self.vertical_speed = -collision.jump_force / self.weight
        self.rect.bottom = collision.top
        self.bounce()
