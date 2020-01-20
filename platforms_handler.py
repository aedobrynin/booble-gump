import pygame
import random
from platforms import Platform


class PlatformsHandler(pygame.sprite.Group):
    def __init__(self, world_boundings):
        super().__init__()
        self.world_boundings = world_boundings

        self.add(Platform((300, 520), "./data/images/platforms/solid.png"))

        while len(self) != 20:
            x = random.randrange(self.world_boundings[0] + 15,
                                 self.world_boundings[2] - 15)
            y = random.randrange(self.world_boundings[1],
                                 self.world_boundings[3])

            platform = Platform((x, y), "./data/images/platforms/solid.png")
            collision = \
                pygame.sprite.spritecollideany(platform,
                                               self,
                                               collided=pygame.sprite.collide_mask)
            if collision is None:
                 self.add(platform)

    def update(self, scroll_value, fps):
        if scroll_value:
            for platform in self.sprites():
                platform.rect.move_ip((0, scroll_value))
                if platform.pos[1] > self.world_boundings[3]:
                    self.remove(platform)

        while len(self) != 20:
            x = random.randrange(self.world_boundings[0],
                                 self.world_boundings[2])
            y = random.randrange(-self.world_boundings[3] // 4,
                                 self.world_boundings[0])
            platform = Platform((x, y), "./data/images/platforms/solid.png")

            collision = \
                pygame.sprite.spritecollideany(platform,
                                               self,
                                               collided=pygame.sprite.collide_mask)
            if collision is None:
                self.add(platform)
