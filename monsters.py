import os
import pygame
from sprite import AnimatedSprite


class BaseMonster(AnimatedSprite):
    def __init__(self, pos, frames):
        super().__init__(self, pos, frames)


class WeightsBasedMonsterGenerator:
    def __init__(self, world_boundings, images_dir, sounds_dir, weights):
        self.world_boundings = world_boundings
        self.weights = weights

        self.load_images(images_dir)
        self.load_sounds(sounds_dir)

    def load_images(self, images_dir):
        self.images = dict()

        for file in os.listdir(images_dir):
            if os.path.isdir(os.path.join(images_dir, file)):
                print(file)
                monster_name = file.rsplit('/')[-1]
                self.images[monster_name] = list()

                for filename in sorted(os.listdir(os.path.join(images_dir, file))):
                    filepath = os.path.join(os.path.join(images_dir, file, filename))
                    self.images[monster_name].append(pygame.image.load(filepath))

    def load_sounds(self, sounds_dir):
        #  TODO
        pass

    def generate(self, monster_pos):
        #  TODO
        pass
