import os
import pygame
from enum import Enum


PACK_NAME = "blue"
DATA_DIR = "./data"
PACK_DIR = os.path.join(DATA_DIR, PACK_NAME)

PLAYER_DIR = os.path.join(PACK_DIR, "player")

PLATFORMS_DIR = os.path.join(PACK_DIR, "platforms")
P_SOUNDS_DIR = os.path.join(PLATFORMS_DIR, "sounds")
P_IMAGES_DIR = os.path.join(PLATFORMS_DIR, "images")

MONSTERS_DIR = os.path.join(PACK_DIR, "monsters")
M_SOUNDS_DIR = os.path.join(MONSTERS_DIR, "sounds")
M_IMAGES_DIR = os.path.join(MONSTERS_DIR, "images")

BACKGROUND = pygame.image.load(os.path.join(PACK_DIR, "background.png"))

FPS = 60

LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 320, 512
WORLD_BOUNDINGS = (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
LEVEL_LINE = WINDOW_HEIGHT // 2

GRAVITATION = 1300

PLATFORMS_JUMP_FORCE = 600
PLATFORM_MOVE_SPEED = 100
PLATFORM_SIZE = PLATFORM_WIDTH, PLATFORM_HEIGHT = 57, 15

PLAYER_WEIGHT = 1
PLAYER_HORIZONTAL_FORCE = 350
PLAYER_BOUNCE_ANIMATION_STEPS = 20
PLAYER_SIZE = PLAYER_WIDTH, PLAYER_HEIGHT = 46, 45
PLAYER_LEGS_LEVEL = 30

MAX_PLAYER_SPEED = PLATFORMS_JUMP_FORCE / PLAYER_WEIGHT
MAX_PLAYER_JUMP_HEIGHT = \
    int(MAX_PLAYER_SPEED ** 2 / (2 * GRAVITATION) - PLAYER_HEIGHT)

MAX_DIFFICULT = 21

START_PLATFORM_WEIGHTS = [80, 20, 0, 0]
START_MONSTERS_WEIGHTS = [20, 20, 20, 20, 20]

MONSTER_TOP_LEVEL = 5
MONSTER_FALL_SPEED = 300
MONSTER_JUMP_FORCE = 800


class Direction(Enum):
    STALL = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
