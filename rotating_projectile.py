# rotating_projectile.py - Classe para o projétil giratório

import pygame
from math import sin, cos, radians
from settings import *

class RotatingProjectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Tamanho do projétil
        self.image.fill(BLUE)  # Cor visível
        self.rect = self.image.get_rect()
        self.player = player
        self.angle = 0
        self.radius = 50  # Distância adequada para garantir visibilidade

        # Posição inicial baseada na do jogador
        self.rect.centerx = player.rect.centerx + self.radius
        self.rect.centery = player.rect.centery

    def update(self, **kwargs):
        self.angle += 5
        if self.angle >= 360:
            self.angle = 0

        # Atualiza posição para girar em torno do jogador
        self.rect.x = self.player.rect.centerx + self.radius * cos(radians(self.angle)) - self.rect.width / 2
        self.rect.y = self.player.rect.centery + self.radius * sin(radians(self.angle)) - self.rect.height / 2
