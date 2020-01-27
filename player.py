import os
from enum import Enum
import pygame
from sprite import MaskedSprite
from shells import BaseShell
from config import *


class Player(MaskedSprite):
    def __init__(self, pos, images_dir, shoot_sound=None):
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

        self.shoot_step = -1
        self.shoot_sound = shoot_sound
        self.shells = pygame.sprite.Group()

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

        if self.shoot_step == PLAYER_SHOOT_ANIMATION_STEPS:
            self.shoot_step = -1

        cur_image_code = self.image_code
        if self.shoot_step != -1:
            cur_image_code += "-shoot"
            self.shoot_step += 1

        if self.bounce_step != -1:
            cur_image_code += "-bounce"
            self.bounce_step += 1

        self.image = self.images[cur_image_code]
        self.mask = self.masks[cur_image_code]

    def bounce(self):
        self.bounce_step = 0

    def shoot(self):
        if self.shoot_step != -1:
            return

        self.shoot_step = 0

        shell_image = self.images["shell"]
        shell_mask = self.masks["shell"]
        shell = BaseShell((0, 0), shell_image, shell_mask)

        shell.pos = self.pos
        if self.image_code == "left":
            shift = list(LEFT_NOSE_POS)
            shift[0] -= shell.rect.width // 2
            shell.rect.move_ip(shift)
        else:
            shift = list(RIGHT_NOSE_POS)
            shift[0] -= shell.rect.width // 2
            shell.rect.move_ip(shift)

        self.shells.add(shell)

        if self.shoot_sound is not None:
            self.shoot_sound.play()

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
        if self.rect.left + self.rect.width // 2 < WORLD_BOUNDINGS[0]:
            self.rect.right = WORLD_BOUNDINGS[2] + self.rect.width // 2

        if self.rect.left + self.rect.width // 2 > WORLD_BOUNDINGS[2]:
            self.rect.left = WORLD_BOUNDINGS[0] - self.rect.width // 20

    def check_collisions_with_monsters(self, monsters):
        collision = \
            pygame.sprite.spritecollideany(self,
                                           monsters,
                                           collided=pygame.sprite.collide_mask)

        if collision is None or collision.dead:
            return

        collision_point = pygame.sprite.collide_mask(self, collision)

        if collision_point[1] >= self.image.get_height() - PLAYER_LEGS_LENGTH:
            print("kill")
            self.vertical_speed = -collision.jump_force / self.weight
            self.rect.bottom = collision.rect.top
            collision.fall_down()
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

        if collision_point[1] < self.image.get_height() - PLAYER_LEGS_LENGTH:
            return

        self.vertical_speed = -collision.jump_force / self.weight
        self.rect.bottom = collision.rect.top
        self.bounce()
        collision.collision_react()

    def check_shells_collisions(self, monsters):
        killed_monsters = pygame.sprite.groupcollide(self.shells,
                                   monsters, True, False,
                                   collided=pygame.sprite.collide_mask).values()

        for monster in killed_monsters:
            monster[0].shoot_down()


    def update(self, platforms, monsters, fps):
        self.__update_image()

        self.__update_vertical_speed(fps)
        self.__update_horizontal_speed()

        self.__check_boundings()

        self.rect.move_ip((self.horizontal_speed / fps,
                           self.vertical_speed / fps))


        self.check_collisions_with_monsters(monsters)
        self.shells.update(fps)
        self.check_shells_collisions(monsters)

        if self.vertical_speed <= 0:
            return

        self.check_collisions_with_platforms(platforms)

    def draw(self, surface):
        super().draw(surface)
        self.shells.draw(surface)
