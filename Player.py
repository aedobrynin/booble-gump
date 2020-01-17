import os
import pygame
from Sprite import Sprite
from enum import Enum




class Direction(Enum):
    LEFT = -1
    STALL = 0
    RIGHT = 1


class Direction_by_key(Enum):
    pygame.K_A = Direction.LEFT
    pygame.K_D = Direction.RIGHT


class Player(Sprite):
    def __init__(self, pos, images_dir):
        self.load_images(images_dir)
        self.vertical_speed = 0
        self.horizontal_speed = 10
        self.horizontal_direction = Direction.STALL

        self.mask = None
        # TODO

        self.weight = 10
        self.gravitation = 9.8
        self.acceleration = 0

        self.right = True
        super().__init__(pos, self.images['right'])

    def load_images(self, images_dir):
        self.images = dict()
        for filename in os.listdir(images_dir):
           state_name = filename.rsplit('.')[0]
           self.images[state_name] = pygame.image.load(os.path.join(images_dir, filename))

    def move_horizontal(self, direction):
        self.horizontal_direction = direction

    def __update_image(self):
        if self.horizontal_direction == Direction.LEFT:
            self.image = self.images['left']
        elif self.horizontal_direction == Direction.RIGHT:
            self.image = self.images['right']

    def update(self, platforms, fps):
        self.__update_image()

        self.acceleration += self.gravitation / self.weight * (1 / fps)
        self.vertical_speed += self.acceleration

        self.rect.move_ip((0, self.vertical_speed))

        if self.vertical_speed > 0:
            return

        collision = pygame.sprite.spritecollideany(self.rect, platforms)
        if collision is None:
            return

        self.acceleration = 0
        self.vertical_speed = 0
        self.rect.bottom = collision.rect.top
