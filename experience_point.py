# experience_point.py - Classe para os pontos de experiência

import pygame
from settings import PINK

class ExperiencePoint(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(PINK)  
        self.rect = self.image.get_rect(center=pos)
