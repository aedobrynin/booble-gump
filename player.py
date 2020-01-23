import os
from enum import Enum
import pygame
from sprite import Sprite

from config import *



class Player(Sprite):
    def __init__(self, pos, images_dir, world_boundings):
        self.load_images(images_dir)
        self.vertical_speed = 0

        self.horizontal_speed = 0

        self.horizontal_force = PLAYER_HORIZONTAL_FORCE
        self.horizontal_direction = Direction.STALL

        self.weight = PLAYER_WEIGHT

        self.gravitation = GRAVITATION

        self.acceleration = 0
        self.image_code = "right"

        self.bounce_step = -1

        self.world_boundings = world_boundings

        super().__init__(pos, self.images[self.image_code])

        self.left_mask = pygame.mask.Mask(self.rect.size)
        for i in range(14, 45):
            for j in range(30, self.rect.height):
                self.left_mask.set_at((i, j))

        self.right_mask = pygame.mask.Mask(self.rect.size)
        for i in range(31):

            for j in range(34, self.rect.height):
                self.right_mask.set_at((i, j))

        self.mask = self.right_mask

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
            self.mask = self.left_mask
        elif self.horizontal_direction == Direction.RIGHT:
            self.image_code = "right"
            self.mask = self.right_mask

        if self.bounce_step == PLAYER_BOUNCE_ANIMATION_STEPS:
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
        acceleration = self.gravitation
        self.vertical_speed += acceleration / fps

    def __check_boundings(self):
        if self.rect.left + self.rect.width // 2 < self.world_boundings[0]:
            self.rect.right = self.world_boundings[2] + self.rect.width // 2

        if self.rect.left + self.rect.width // 2 > self.world_boundings[2]:
            self.rect.left = self.world_boundings[0] - self.rect.width // 20

    def check_collisions_with_monsters(self, monsters):
        pass

    def check_collisions_with_platforms(self, platforms):
        collision = \
            pygame.sprite.spritecollideany(self,
                                           platforms,
                                           collided=pygame.sprite.collide_mask)

        if collision is None:
            return

        self.vertical_speed = -collision.jump_force / self.weight
        self.rect.bottom = collision.top
        self.bounce()
        collision.collision_react()

    def update(self, platforms, monsters, fps):
        self.__update_image()

        self.__update_vertical_speed(fps)
        self.__update_horizontal_speed()

        self.__check_boundings()

        self.rect.move_ip((self.horizontal_speed / fps,
                           self.vertical_speed / fps))

        self.check_collisions_with_monsters(monsters)

        if self.vertical_speed <= 0:
            return

        self.check_collisions_with_platforms(platforms)
