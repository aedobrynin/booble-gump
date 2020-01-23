import pygame
from monsters import WeightsBasedMonsterGenerator
from config import *


class MonstersHandler(pygame.sprite.Group):
    def __init__(self, world_boundings, images_dir, sounds_dir):
        super().__init__()

        self.world_boundings = world_boundings

        self.monster_generator = \
            WeightsBasedMonsterGenerator(world_boundings,
                                         images_dir,
                                         sounds_dir,
                                         START_MONSTERS_WEIGHTS)

    def make_harder(self):
        #  TODO
        pass

    def update(self, scroll_value, fps):
        if scroll_value:
            for monster in self.sprites():
                monster.rect.move_ip((0, scroll_value))
                if monster.pos[1] > self.world_boundings[3]:
                    self.remove(monster)

        super().update(fps)
