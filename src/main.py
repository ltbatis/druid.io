import pygame
import sys
from player import Player
from monster import Monster
from pygame.math import Vector2
from projectile import Projectile
from settings import *
from experience_point import ExperiencePoint
from rotating_projectile import RotatingProjectile  # Ajuste o import conforme a localização da sua classe

def run_game():
    # Inicializa o Pygame
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont(None, 36)
    start_ticks = pygame.time.get_ticks()
    monster_spawn_timer = 0
    monster_spawn_rate = 5000  # Tempo em milissegundos (5 segundos)
    score = 0

    # Configura a tela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Druid.io")

    # Controle de tempo
    clock = pygame.time.Clock()

    # Cria o jogador
    player = Player()
    # Cria um grupo de sprites para o jogador
    player_group = pygame.sprite.Group(player)

    # Grupos para projéteis, monstros e pontos de experiência
    projectile_group = pygame.sprite.Group()
    monster_group = pygame.sprite.Group()
    experience_points_group = pygame.sprite.Group()

    # Cria um projétil rotatório e adiciona ao grupo all_sprites
    rotating_projectile = RotatingProjectile(player)
    all_sprites = pygame.sprite.Group(player, rotating_projectile)  # Inclua outros sprites conforme necessário

    # Adiciona monstros ao grupo
    for _ in range(5):
        monster_group.add(Monster(player))

    # Loop principal do jogo
    running = True
    while running:
        # Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Dispara projéteis
                    direction = Vector2(1, 0)
                    for _ in range(player.number_of_projectiles):
                        projectile = Projectile(player.rect.center, direction)
                        projectile_group.add(projectile)
            if event.type == pygame.QUIT:
                running = False

        # Atualiza o jogador e grupos de sprites
        keys = pygame.key.get_pressed()
        player.update(keys)
        monster_group.update()
        projectile_group.update()
        experience_points_group.update()

        # Atualiza todos os sprites, passando 'keys' apenas para o 'Player'
        for sprite in all_sprites:
            if isinstance(sprite, Player):
                sprite.update(keys)
            else:
                sprite.update()


        # Detecção de colisões e lógica de jogo
        hits = pygame.sprite.groupcollide(monster_group, projectile_group, True, True)
        for hit in hits:
            score += 10  # Adiciona pontos ao score para cada monstro atingido
            experience_points_group.add(ExperiencePoint(hit.rect.center))

        # Lógica para pontos de experiência
        hits = pygame.sprite.spritecollide(player, experience_points_group, True)
        for hit in hits:
            player.experience += 1
            if player.experience % 2 == 0:
                player.number_of_projectiles += 1
        for hit in hits:
            experience_points_group.add(ExperiencePoint(hit.rect.center))

        # Detecção de colisão entre o projétil giratório e monstros
        for monster in monster_group:
            if pygame.sprite.collide_rect(rotating_projectile, monster):
                monster.kill()  # Remove o monstro acertado

        # Verifica se é hora de adicionar um novo monstro
        monster_spawn_timer += clock.get_time()
        if monster_spawn_timer >= monster_spawn_rate:
            monster_group.add(Monster(player))
            monster_spawn_timer = 0  # Reinicia o temporizador

        # Renderização
        screen.fill(BLACK)
        player_group.draw(screen)
        monster_group.draw(screen)
        projectile_group.draw(screen)
        experience_points_group.draw(screen)
        all_sprites.draw(screen)  # Desenha todos os sprites, incluindo o projétil rotatório

        # Renderiza a barra de experiência
        experience_bar_length = 100  # Comprimento máximo da barra
        experience_bar_height = 10
        experience_ratio = player.experience / player.experience_needed_for_next_level
        bar_length = experience_ratio * experience_bar_length
        experience_bar = pygame.Rect(10, 10, bar_length, experience_bar_height)
        pygame.draw.rect(screen, PINK, experience_bar)

        # Renderiza o contador de score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 30))  # Ajuste a posição conforme necessário

        # Renderiza o contador de tempo
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        time_text = font.render(f'Time: {seconds} sec', True, WHITE)
        screen.blit(time_text, (10, 50))  # Ajuste a posição conforme necessário


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.font.init()  # Inicializa o módulo de fontes
    font = pygame.font.SysFont(None, 36)
    run_game()
