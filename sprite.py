import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()

        self.rect = None
        self.image = image
        self.rect.topleft = pos

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        if self.rect is None:
            self.rect = self.image.get_rect()
        else:
            self.rect.size = self.image.get_size()

    @property
    def pos(self):
        return self.rect.topleft

    @pos.setter
    def pos(self, value):
        self.rect.topleft = value

    def draw(self, surface):
        surface.blit(self.image, self.pos)


class MaskedSprite(Sprite):
    def __init__(self, pos, image, mask=None):
        super().__init__(pos, image)

        if mask is None:
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.mask = mask
