import pygame


class MaskedSprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, mask=None):
        super().__init__()
        self.image = image

        if mask is None:
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.mask = mask

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
