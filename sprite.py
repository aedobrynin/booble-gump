import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    @property
    def pos(self):
        return self.rect.topleft

    @pos.setter
    def pos(self, value):
        self.rect.topleft = value

    def draw(self, surface):
        surface.blit(self.image, self.pos)
