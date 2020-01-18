import pygame
from Sprite import Sprite


class Platform(Sprite):
    def __init__(self, pos, image_path):
        super().__init__(pos, pygame.image.load(image_path))
        self.mask = pygame.mask.from_surface(self.image)
        self.top = None
        for j in range(self.image.get_height()):
            for i in range(self.image.get_width()):
                if self.mask.get_at((i, j)):
                    self.top = j
                    break

            if self.top is not None:
                break

        self.top += self.rect.top
        self.jump_force = 130

    @property
    def jump_force(self):
        return self._jump_force

    @jump_force.setter
    def jump_force(self, value):
        self._jump_force = value
