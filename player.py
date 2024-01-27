import pygame
from settings import *

from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH

    def update(self, keys):
        # Movimentação do jogador
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Mantém o jogador dentro da tela
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def attack(self):
        # Esta função cria um projétil direcionado ao monstro mais próximo ou numa direção fixa
        pass  # Substitua por lógica de criação de projéteis
