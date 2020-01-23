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

        
class AnimatedSprite(Sprite):
    def __init__(self, pos, frames):
        self.frames = frames
        self.masks = list()
        for frame in frames:
            self.masks.append(pygame.mask.from_surface(frame))

        self.animation_frame = 0
        self.paused = False

        super().__init__(pos, frames[0])
        self.mask = self.masks[0]

    def update(self):
        if self.paused is True:
            return

        self.animation_frame += 1
        if self.animation_frame == len(self.frames):
            self.animation_frame = 0

        self.image = self.frames[animation_frame]
        self.mask = self.masks[animation_frame]