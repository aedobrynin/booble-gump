from sprite import MaskedSprite
from config import SHELLS_SPEED, WORLD_BOUNDINGS


class BaseShell(MaskedSprite):
    def __init__(self, pos, image, mask=None):
        super().__init__(pos, image, mask)

        self.speed = SHELLS_SPEED

    def update(self, fps):
        self.rect.move_ip((0, self.speed / fps))

        if self.rect.bottom < WORLD_BOUNDINGS[1]:
            self.kill()
