import os
import pygame
import random
from sprite import MaskedSprite
from config import *


class BasePlatform(MaskedSprite):
    def __init__(self, pos, image, mask=None, sound=None):
        super().__init__(pos, image, mask)
        self.sound = sound

        self.jump_force = PLATFORMS_JUMP_FORCE

    @property
    def jump_force(self):
        return self._jump_force

    @jump_force.setter
    def jump_force(self, value):
        self._jump_force = value

    def collision_react(self):
        if self.sound is not None:
            self.sound.play()


class StaticPlatform(BasePlatform):
    def __init__(self, pos, image, mask=None, sound=None):
        super().__init__(pos, image, mask, sound)


class HorizontalMovingPlatform(BasePlatform):
    def __init__(self, pos, image, mask=None, sound=None):
        super().__init__(pos, image, mask, sound)
        self.speed = PLATFORM_MOVE_SPEED

        self.left_lim = WORLD_BOUNDINGS[0] + 15

        self.right_lim = WORLD_BOUNDINGS[2] - 70

        self.direction = random.choice((Direction.LEFT, Direction.RIGHT))

    def update(self, fps):
        if self.direction == Direction.LEFT:
            self.rect.left = self.pos[0] - round(self.speed / fps)
            if self.pos[0] <= self.left_lim:
                self.direction = Direction.RIGHT
                self.rect.left = self.left_lim
        else:
            self.rect.left = self.pos[0] + round(self.speed / fps)
            if self.pos[0] >= self.right_lim:
                self.direction = Direction.LEFT
                self.rect.left = self.right_lim


class VanishPlatform(BasePlatform):
    def __init__(self, pos, image, mask=None, sound=None):
        super().__init__(pos, image, mask, sound)

    def collision_react(self):
        super().collision_react()
        self.kill()


class HorizontalMovingVanishPlatform(HorizontalMovingPlatform, VanishPlatform):
    def __init__(self, pos, image, mask=None, sound=None):
        super().__init__(pos, image, mask, sound)


"""(Class, image name, sound name)"""
PLATFORM_TYPES = ((StaticPlatform, "static", "pop"),
                  (HorizontalMovingPlatform, "moving", "pop"),
                  (VanishPlatform, "vanish", "vanish"),
                  (HorizontalMovingVanishPlatform, "vanish", "vanish"))


class WeightBasedPlatformGenerator:
    def __init__(self, images_dir, sounds_dir, weights):
        self.weights = weights

        self.load_images(images_dir)
        self.load_masks()
        self.load_sounds(sounds_dir)

    def load_images(self, images_dir):
        self.images = dict()
        for filename in os.listdir(images_dir):
            class_name = filename.rsplit('.')[0]
            self.images[class_name] = \
                pygame.image.load(os.path.join(images_dir, filename))

    def load_masks(self):
        self.masks = dict()
        for class_name, image in self.images.items():
            self.masks[class_name] = pygame.mask.from_surface(image)

    def load_sounds(self, sounds_dir):
        self.sounds = dict()
        for _, _, filename in PLATFORM_TYPES:
            self.sounds[filename] = \
                pygame.mixer.Sound(os.path.join(sounds_dir, f"{filename}.wav"))

    def make_harder(self):
        for i in range(len(self.weights) - 2, -1, -1):
            if self.weights[i] < max(self.weights[:-1]) or self.weights[i] < 9:
                continue

            taken = 9
            self.weights[i] -= taken
            add = 5
            for j in range(i + 1, min(i + 3, len(self.weights))):
                self.weights[j] += add
                taken -= add
                add -= 1
            if taken > 0:
                self.weights[i + 1] += taken

    def reset(self):
        self.weights = P_INITIAL_WEIGHTS

    def generate(self, platform_pos):
        platform_class, platform_image_name, platform_sound_name = \
            random.choices(PLATFORM_TYPES, weights=self.weights)[0]

        return platform_class(platform_pos,
                              self.images[platform_image_name],
                              self.masks[platform_image_name],
                              self.sounds[platform_sound_name])
