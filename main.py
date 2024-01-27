import pygame
import sys
from player import Player
from monster import Monster
from pygame.math import Vector2
from projectile import Projectile
from settings import *


def run_game():
    # Inicializa o Pygame
    monster_spawn_timer = 0
    monster_spawn_rate = 5000  # Tempo em milissegundos (5 segundos)
    score = 0
    pygame.init()

    # Configura a tela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Druid.io")

    # Controle de tempo
    clock = pygame.time.Clock()

    # Cria o jogador
    player = Player()
    # Cria um grupo de sprites para o jogador
    player_group = pygame.sprite.Group(player)

    projectile_group = pygame.sprite.Group()

    # Cria um grupo de sprites para os monstros
    monster_group = pygame.sprite.Group()

    # Adiciona monstros ao grupo
    for _ in range(5):  # Começa com 5 monstros
        monster_group.add(Monster(player))

    # Loop principal do jogo
    running = True
    while running:
        # Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Assume que direction é a direção do projétil
                    direction = Vector2(1, 0)  # Exemplo: direita
                    projectile = Projectile(player.rect.center, direction)
                    projectile_group.add(projectile)
            if event.type == pygame.QUIT:
                running = False

        # Atualiza o estado do jogo aqui
        # ...

        # Atualiza o jogador
        keys = pygame.key.get_pressed()
        player.update(keys)
        
         # Atualiza os monstros
        monster_group.update()

        # Preenche a tela com preto
        screen.fill(BLACK)
        
        # Desenha o jogador
        player_group.draw(screen)

        projectile_group.update()
        projectile_group.draw(screen)

        # Desenha os monstros
        monster_group.draw(screen)

        # Verifica colisões entre projéteis e monstros
        hits = pygame.sprite.groupcollide(monster_group, projectile_group, True, True)
        
        # Atualiza o temporizador
        monster_spawn_timer += clock.get_time()

        # Verifica se é hora de adicionar um novo monstro
        if monster_spawn_timer >= monster_spawn_rate:
            monster_group.add(Monster(player))
            monster_spawn_timer = 0  # Reinicia o temporizador

        
        # Dentro do loop principal, após a detecção de colisão
        for hit in hits:
            score += 10  # Adiciona 10 pontos para cada monstro atingido

        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Atualiza a tela
        pygame.display.flip()

        # Limita o FPS
        clock.tick(60)

    # Finaliza o Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.font.init()  # Inicializa o módulo de fontes
    font = pygame.font.SysFont(None, 36)
    run_game()
