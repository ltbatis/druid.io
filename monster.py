import pygame
from settings import *
from random import randint

class Monster(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))
        self.speed = MONSTER_SPEED
        self.health = MONSTER_HEALTH
        self.player = player

    def update(self):
        # Movimentação em direção ao jogador
        if self.rect.x < self.player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > self.player.rect.x:
            self.rect.x -= self.speed
        
        if self.rect.y < self.player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > self.player.rect.y:
            self.rect.y -= self.speed
