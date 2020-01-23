import os
from enum import Enum
import pygame
from sprite import MaskedSprite
from config import *


class Player(MaskedSprite):
    def __init__(self, pos, images_dir, world_boundings):
        self.load_images_and_masks(images_dir)

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

        super().__init__(pos, self.images[self.image_code], self.masks[self.image_code])

    def load_images_and_masks(self, images_dir):
        self.images = dict()
        self.masks = dict()
        for filename in os.listdir(images_dir):
            state_name = filename.rsplit('.')[0]
            image = pygame.image.load(os.path.join(images_dir, filename))
            mask = pygame.mask.from_surface(image)
            self.images[state_name] = image
            self.masks[state_name] = mask

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

        if self.bounce_step == PLAYER_BOUNCE_ANIMATION_STEPS:
            self.bounce_step = -1

        if self.bounce_step != -1:
            self.image = self.images[self.image_code + "-bounce"]
            self.bounce_step += 1
        else:
            self.image = self.images[self.image_code]
            self.mask = self.masks[self.image_code]

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
        collision = \
            pygame.sprite.spritecollideany(self,
                                           monsters,
                                           collided=pygame.sprite.collide_mask)

        if collision is None or collision.dead:
            return

        collision_point = pygame.sprite.collide_mask(self, collision)
        print(collision_point)
        if collision_point[1] > PLAYER_LEGS_LEVEL:
            print("kill")
            self.vertical_speed = -collision.jump_force / self.weight
            self.rect.bottom = collision.rect.top
            collision.die()
            return

        print("game over")
        exit(0)

    def check_collisions_with_platforms(self, platforms):
        collision = \
            pygame.sprite.spritecollideany(self,
                                           platforms,
                                           collided=pygame.sprite.collide_mask)

        if collision is None:
            return

        collision_point = pygame.sprite.collide_mask(self, collision)

        if collision_point[1] < PLAYER_LEGS_LEVEL:
            return

        self.vertical_speed = -collision.jump_force / self.weight
        self.rect.bottom = collision.rect.top
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
