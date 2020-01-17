import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
