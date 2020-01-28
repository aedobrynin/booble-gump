import os
import random
import pygame
from sprite import MaskedSprite
from config import *


class BaseMonster(MaskedSprite):
    def __init__(self, platform, image, mask=None,
                 fall_down_sound=None, shoot_down_sound=None):

        self.platform = platform
        super().__init__((0, 0), image, mask)

        self.rect.midbottom = self.platform.rect.midtop

        self.dead = False
        self.jump_force = MONSTER_JUMP_FORCE

        self.fall_down_sound = fall_down_sound
        self.shoot_down_sound = shoot_down_sound

    @property
    def jump_force(self):
        return self._jump_force

    @jump_force.setter
    def jump_force(self, val):
        self._jump_force = val

    def fall_down(self):
        self.dead = True

        if self.fall_down_sound is not None:
            self.fall_down_sound.play()

    def shoot_down(self):
        self.dead = True

        if self.shoot_down_sound is not None:
            self.shoot_down_sound.play()

        self.kill()

    def update(self, fps):
        if self.dead:
            self.rect.move_ip((0, MONSTER_FALL_SPEED / fps))
            return

        self.rect.left = self.platform.rect.left


"""(Class, monster name, fall down sound name, shoot down sound name)"""
MONSTER_TYPES = ((BaseMonster, "long", "fall_down", "shoot_down"),
                 (BaseMonster, "clumsy", "fall_down", "shoot_down"),
                 (BaseMonster, "hare", "fall_down", "shoot_down"),
                 (BaseMonster, "kind", "fall_down", "shoot_down"),
                 (BaseMonster, "rabbit", "fall_down", "shoot_down"),
                 (BaseMonster, "robot", "fall_down", "shoot_down"),
                 (BaseMonster, "toothy", "fall_down", "shoot_down"),
                 (BaseMonster, "triangle", "fall_down", "shoot_down"),
                 (BaseMonster, "zombie", "fall_down", "shoot_down"))


class WeightBasedMonsterGenerator:
    def __init__(self, images_dir, sounds_dir, weights):
        self.weights = weights

        self.load_images(images_dir)
        self.load_masks()
        self.load_sounds(sounds_dir)

    def load_images(self, images_dir):
        self.images = dict()

        for file in os.listdir(images_dir):
            monster_name = file.rsplit('.')[0]
            image = pygame.image.load(os.path.join(images_dir, file))
            self.images[monster_name] = image

    def load_masks(self):
        self.masks = dict()

        for monster_name, image in self.images.items():
            mask = pygame.mask.from_surface(image)
            self.masks[monster_name] = mask

    def load_sounds(self, sounds_dir):
        self.sounds = dict()
        for file in os.listdir(sounds_dir):
            sound_name = file.rsplit('.')[0]
            sound = pygame.mixer.Sound(os.path.join(sounds_dir, file))
            self.sounds[sound_name] = sound

    def reset(self):
        pass

    def generate(self, platform):
        m_class, m_name, m_fall_down_sound_name, m_shoot_down_sound_name = \
            random.choices(MONSTER_TYPES, weights=self.weights)[0]

        return m_class(platform,
                       self.images[m_name],
                       self.masks[m_name],
                       self.sounds[m_fall_down_sound_name],
                       self.sounds[m_shoot_down_sound_name])
