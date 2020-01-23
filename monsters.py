import os
import random
import pygame
from sprite import MaskedSprite
from config import *


class BaseMonster(MaskedSprite):
    def __init__(self, pos, images, masks=None, death_sound=None):
        self.images = images

        if masks is None:
            self.masks = list()
            for image in self.images:
                self.masks.append(pygame.mask.from_surface(image))
        else:
            self.masks = masks

        super().__init__(pos, self.images[0], self.masks[0])

        self.dead = False
        self.jump_force = MONSTER_JUMP_FORCE
        self.death_sound = death_sound

    @property
    def jump_force(self):
        return self._jump_force

    @jump_force.setter
    def jump_force(self, val):
        self._jump_force = val

    def die(self):
        self.dead = True
        self.image = self.images[1]
        self.mask = self.masks[1]

        if self.death_sound is not None:
            self.death_sound.play()

    def update(self, fps):
        if self.dead:
            self.rect.move_ip((0, MONSTER_FALL_SPEED / fps))
            return


"""(Class, monster name, death sound name)"""
MONSTER_TYPES = ((BaseMonster, "blue", "metal_hit"),
                 (BaseMonster, "pink", "metal_hit"),
                 (BaseMonster, "orange", "metal_hit"),
                 (BaseMonster, "green", "metal_hit"),
                 (BaseMonster, "yellow", "metal_hit"))


class WeightsBasedMonsterGenerator:
    def __init__(self, world_boundings, images_dir, sounds_dir, weights):
        self.world_boundings = world_boundings
        self.weights = weights

        self.load_images(images_dir)
        self.load_masks()
        self.load_sounds(sounds_dir)

    def load_images(self, images_dir):
        self.images = dict()

        for file in os.listdir(images_dir):
            dir_path = os.path.join(images_dir, file)
            if os.path.isdir(dir_path):
                monster_name = file.rsplit('/')[-1]
                self.images[monster_name] = list()

                for filename in sorted(os.listdir(dir_path)):
                    filepath = os.path.join(os.path.join(dir_path, filename))
                    image = pygame.image.load(filepath)
                    self.images[monster_name].append(image)

    def load_masks(self):
        self.masks = dict()

        for monster_name, images in self.images.items():
            self.masks[monster_name] = list()
            for image in images:
                mask = pygame.mask.from_surface(image)
                self.masks[monster_name].append(mask)

    def load_sounds(self, sounds_dir):
        self.sounds = dict()
        for file in os.listdir(sounds_dir):
            sound_name = file.rsplit('.')[0]
            sound = pygame.mixer.Sound(os.path.join(sounds_dir, file))
            self.sounds[sound_name] = sound

    def generate(self, monster_pos):
        monster_class, monster_name, monster_sound_name = \
            random.choices(MONSTER_TYPES, weights=self.weights)[0]

        return monster_class(monster_pos,
                             self.images[monster_name],
                             self.masks[monster_name],
                             self.sounds[monster_sound_name])
