import os
import pygame
from config import MAIN_FONT


class ScoreBar(pygame.Surface):
    def __init__(self, width, height, score, background=None):
        self.width = width
        self.height = height

        self.background = background

        super().__init__((width, height), pygame.SRCALPHA, 32)

        self.font = pygame.font.Font(MAIN_FONT, 24)
        self.font.set_bold(True)
        self.score = score

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

        self.fill(pygame.Color(0, 0, 0, 0))
        if self.background is not None:
            self.blit(self.background, (0, 0))

        score_text = self.font.render(str(self.score),
                                      1,
                                      pygame.Color("#2B2517"))
        self.blit(score_text, (10, 0))
