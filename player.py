import os
import pygame
from sprite import MaskedSprite
from shells import BaseShell
from config import PLAYER_HORIZONTAL_FORCE, Direction, PLAYER_WEIGHT
from config import GRAVITATION, PLAYER_BOUNCE_ANIMATION_STEPS
from config import PLAYER_SHOOT_ANIMATION_STEPS, LEFT_NOSE_POS
from config import RIGHT_NOSE_POS, SHOOT_SOUND_NAME, WORLD_BOUNDINGS
from config import PLAYER_LEGS_LENGTH, DEATH_SOUND_NAME, FALL_DOWN_SOUND_NAME


class Player(MaskedSprite):
    def __init__(self, pos, images_dir, sounds_dir):
        self.load_images_and_masks(images_dir)
        self.load_sounds(sounds_dir)

        self.vertical_speed = 0

        self.horizontal_speed = 0
        self.horizontal_force = PLAYER_HORIZONTAL_FORCE
        self.horizontal_direction = Direction.STALL

        self.weight = PLAYER_WEIGHT

        self.gravitation = GRAVITATION
        self.acceleration = 0
        self.image_code = "right"

        self.bounce_step = -1

        self.shoot_step = -1
        self.shells = pygame.sprite.Group()

        self.dead = False

        super().__init__(pos,
                         self.images[self.image_code],
                         self.masks[self.image_code])

    def load_images_and_masks(self, images_dir):
        self.images = dict()
        self.masks = dict()
        for filename in os.listdir(images_dir):
            state_name = filename.rsplit('.')[0]
            image = pygame.image.load(os.path.join(images_dir, filename))
            mask = pygame.mask.from_surface(image)
            self.images[state_name] = image
            self.masks[state_name] = mask

    def load_sounds(self, sounds_dir):
        self.sounds = dict()
        for file in os.listdir(sounds_dir):
            sound_name = file.rsplit(".")[0]
            sound = pygame.mixer.Sound(os.path.join(sounds_dir, file))
            self.sounds[sound_name] = sound

    @property
    def horizontal_direction(self):
        return self._horizontal_direction

    @horizontal_direction.setter
    def horizontal_direction(self, value):
        self._horizontal_direction = value

    def update_image(self):
        if self.horizontal_direction == Direction.LEFT:
            self.image_code = "left"

        elif self.horizontal_direction == Direction.RIGHT:
            self.image_code = "right"

        if self.bounce_step == PLAYER_BOUNCE_ANIMATION_STEPS:
            self.bounce_step = -1

        if self.shoot_step == PLAYER_SHOOT_ANIMATION_STEPS:
            self.shoot_step = -1

        cur_image_code = self.image_code
        if self.shoot_step != -1:
            cur_image_code += "-shoot"
            self.shoot_step += 1

        if self.bounce_step != -1:
            cur_image_code += "-bounce"
            self.bounce_step += 1

        self.image = self.images[cur_image_code]
        self.mask = self.masks[cur_image_code]

    def bounce(self):
        self.bounce_step = 0

    def shoot(self):
        if self.shoot_step != -1:
            return

        self.shoot_step = 0

        shell_image = self.images["shell"]
        shell_mask = self.masks["shell"]
        shell = BaseShell((0, 0), shell_image, shell_mask)

        shell.pos = self.pos
        if self.image_code == "left":
            shift = list(LEFT_NOSE_POS)
            shift[0] -= shell.rect.width // 2
            shell.rect.move_ip(shift)
        else:
            shift = list(RIGHT_NOSE_POS)
            shift[0] -= shell.rect.width // 2
            shell.rect.move_ip(shift)

        self.shells.add(shell)
        self.sounds[SHOOT_SOUND_NAME].play()

    def update_horizontal_speed(self):
        if self.horizontal_direction == Direction.STALL:
            self.horizontal_speed = 0
        elif self.horizontal_direction == Direction.LEFT:
            self.horizontal_speed = -self.horizontal_force / self.weight
        elif self.horizontal_direction == Direction.RIGHT:
            self.horizontal_speed = self.horizontal_force / self.weight

    def update_vertical_speed(self, fps):
        acceleration = self.gravitation
        self.vertical_speed += acceleration / fps

    def __check_boundings(self):
        if self.rect.left + self.rect.width // 2 < WORLD_BOUNDINGS[0]:
            self.rect.right = WORLD_BOUNDINGS[2] + self.rect.width // 2

        if self.rect.left + self.rect.width // 2 > WORLD_BOUNDINGS[2]:
            self.rect.left = WORLD_BOUNDINGS[0] - self.rect.width // 20

    def check_collisions_with_monsters(self, monsters):
        collision = \
            pygame.sprite.spritecollideany(self,
                                           monsters,
                                           collided=pygame.sprite.collide_mask)

        if collision is None or collision.dead:
            return

        collision_point = pygame.sprite.collide_mask(self, collision)

        if collision_point[1] >= self.image.get_height() - PLAYER_LEGS_LENGTH:
            self.vertical_speed = -collision.jump_force / self.weight
            self.rect.bottom = collision.rect.top
            collision.fall_down()
            return

        self.die()

    def check_collisions_with_platforms(self, platforms):
        collision = \
            pygame.sprite.spritecollideany(self,
                                           platforms,
                                           collided=pygame.sprite.collide_mask)

        if collision is None:
            return

        collision_point = pygame.sprite.collide_mask(self, collision)

        if collision_point[1] < self.image.get_height() - PLAYER_LEGS_LENGTH:
            return

        self.vertical_speed = -collision.jump_force / self.weight
        self.rect.bottom = collision.rect.top
        self.bounce()
        collision.collision_react()

    def check_shells_collisions(self, monsters):
        killed_monsters = \
            pygame.sprite.groupcollide(self.shells,
                                       monsters, True, False,
                                       collided=pygame.sprite.collide_mask)

        for monster in killed_monsters.values():
            monster[0].shoot_down()

    def die(self):
        self.dead = True
        self.shells.empty()
        self.sounds[DEATH_SOUND_NAME].play()
        self.sounds[FALL_DOWN_SOUND_NAME].play()

    def update(self, platforms, monsters, fps):
        self.update_image()

        self.update_vertical_speed(fps)
        self.update_horizontal_speed()

        self.__check_boundings()

        self.rect.move_ip((self.horizontal_speed / fps,
                           self.vertical_speed / fps))

        self.check_collisions_with_monsters(monsters)

        if self.dead is False:
            self.shells.update(fps)
            self.check_shells_collisions(monsters)

            if self.vertical_speed <= 0:
                return

            self.check_collisions_with_platforms(platforms)

        if self.rect.bottom > WORLD_BOUNDINGS[3]:
            self.dead = True
            self.sounds[FALL_DOWN_SOUND_NAME].play()
            self.shells.empty()

        if self.rect.top > WORLD_BOUNDINGS[3]:
            self.kill()

    def draw(self, surface):
        super().draw(surface)
        self.shells.draw(surface)
