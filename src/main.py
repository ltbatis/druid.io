import pygame
import random
import sys
from player import Player
from monster import Monster
from pygame.math import Vector2
from projectile import Projectile
from settings import *
from experience_point import ExperiencePoint
from rotating_projectile import RotatingProjectile

def initialize_pygame():
    pygame.init()
    pygame.font.init()
    return pygame.font.SysFont(None, 36)

def create_game_objects():
    player = Player()
    player_group = pygame.sprite.Group(player)

    projectile_group = pygame.sprite.Group()
    monster_group = pygame.sprite.Group()
    experience_points_group = pygame.sprite.Group()
    rotating_projectile = RotatingProjectile(player)
    all_sprites = pygame.sprite.Group(player, rotating_projectile)

    for _ in range(5):
        monster_group.add(Monster(player))

    return player, player_group, projectile_group, monster_group, experience_points_group, rotating_projectile, all_sprites

def handle_events(player, projectile_group):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_projectiles(player, projectile_group)
            elif event.key == pygame.K_ESCAPE:  # Detecta se ESC foi pressionado
                return True  # Indica que o jogo deve pausar
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    return False

def pause_game(screen, font):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Retoma o jogo
                    paused = False
                elif event.key == pygame.K_ESCAPE:  # Sai do jogo
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        pause_text = font.render("Jogo Pausado", True, WHITE)
        resume_text = font.render("Pressione ESPAÇO para continuar", True, WHITE)
        screen.blit(pause_text, (100, 100))
        screen.blit(resume_text, (100, 150))
        pygame.display.flip()

def fire_projectiles(player, projectile_group):
    direction = Vector2(1, 0)
    for _ in range(player.number_of_projectiles):
        projectile = Projectile(player.rect.center, direction)
        projectile_group.add(projectile)

def update_game_objects(player, keys, groups):
    player.update(keys)
    for group in groups:
        group.update()

def update_all_sprites(all_sprites, player, keys):
    for sprite in all_sprites:
        if isinstance(sprite, Player):
            sprite.update(keys)
        else:
            sprite.update()

def collision_detection(player, monster_group, projectile_group, experience_points_group, rotating_projectile, score):
    hits = pygame.sprite.groupcollide(monster_group, projectile_group, True, True)
    score = update_score_and_experience(hits, experience_points_group, score)
    hits = pygame.sprite.spritecollide(player, experience_points_group, True)
    update_player_experience(player, hits)
    detect_rotating_projectile_hits(monster_group, rotating_projectile, experience_points_group)  
    return score

def update_score_and_experience(hits, experience_points_group, score):
    for hit in hits:
        score += 10
        experience_points_group.add(ExperiencePoint(hit.rect.center))
    return score

def update_player_experience(player, hits):
    for hit in hits:
        player.experience += 1
        if player.experience % 2 == 0:
            player.number_of_projectiles += 1

def detect_rotating_projectile_hits(monster_group, rotating_projectile, experience_points_group):
    for monster in monster_group:
        if pygame.sprite.collide_rect(rotating_projectile, monster):
            monster.kill()  
            experience_points_group.add(ExperiencePoint(monster.rect.center))  


def render(screen, font, groups, player, start_ticks, score):
    screen.fill(BLACK)
    for group in groups:
        group.draw(screen)
    render_experience_bar(screen, player)
    render_score_and_time(screen, font, start_ticks, score)
    render_health_bar(screen, player)
    pygame.display.flip()

def render_experience_bar(screen, player):
    experience_bar_length = 100
    experience_bar_height = 10
    experience_ratio = player.experience / player.experience_needed_for_next_level
    bar_length = experience_ratio * experience_bar_length
    experience_bar = pygame.Rect(10, 10, bar_length, experience_bar_height)
    pygame.draw.rect(screen, PINK, experience_bar)

def render_health_bar(screen, player):
    health_bar_length = 100
    health_bar_height = 10
    health_ratio = player.health / 10
    bar_length = health_ratio * health_bar_length
    health_bar = pygame.Rect(10, SCREEN_HEIGHT - 20, bar_length, health_bar_height)
    pygame.draw.rect(screen, GREEN, health_bar)

def render_score_and_time(screen, font, start_ticks, score):
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 30))
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_text = font.render(f'Time: {seconds} sec', True, WHITE)
    screen.blit(time_text, (10, 50))

def random_spawn_position():
    # Retorna uma posição aleatória ao redor das bordas do mapa
    x = random.choice([0, SCREEN_WIDTH])
    y = random.choice([0, SCREEN_HEIGHT])
    return x, y

def show_start_screen(screen, font):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Começa o jogo
                    return True
                elif event.key == pygame.K_ESCAPE:  # Sai do jogo
                    return False

        screen.fill(BLACK)
        title_text = font.render("Bem-vindo ao Druid.io", True, WHITE)
        start_text = font.render("Pressione ESPAÇO para começar", True, WHITE)
        exit_text = font.render("Pressione ESC para sair", True, WHITE)

        screen.blit(title_text, (100, 100))
        screen.blit(start_text, (100, 200))
        screen.blit(exit_text, (100, 300))

        pygame.display.flip()

def start_countdown(screen, font):
    for i in range(5, 0, -1):
        screen.fill(BLACK)
        countdown_text = font.render(str(i), True, WHITE)
        screen.blit(countdown_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(1000)  # Espera 1 segundo

def show_game_over_screen(screen, font, survival_time):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Começa um novo jogo
                    return True
                elif event.key == pygame.K_ESCAPE:  # Sai do jogo
                    return False

        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        survival_text = font.render(f"Você sobreviveu por {survival_time} segundos", True, WHITE)
        restart_text = font.render("Pressione ESPAÇO para jogar novamente", True, WHITE)
        exit_text = font.render("Pressione ESC para sair", True, WHITE)

        screen.blit(game_over_text, (100, 100))
        screen.blit(survival_text, (100, 200))
        screen.blit(restart_text, (100, 300))
        screen.blit(exit_text, (100, 400))

        pygame.display.flip()


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Druid.io")
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    player, player_group, projectile_group, monster_group, experience_points_group, rotating_projectile, all_sprites = create_game_objects()
    monster_spawn_timer = 0
    current_monster_spawn_rate = 3000  # Começa com 3 segundos
    min_monster_spawn_rate = 500  # Mínimo de 0,5 segundos
    spawn_rate_decrease = 500  # Diminui a taxa de spawn em 500 ms a cada 30 segundos
    last_spawn_rate_change = pygame.time.get_ticks()
    last_speed_increase = pygame.time.get_ticks()
    score = 0
    start_ticks = pygame.time.get_ticks()

    if show_start_screen(screen, font):
        start_countdown(screen, font)
        while True:
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()

            if handle_events(player, projectile_group):
                pause_game(screen, font)
                    # Continuação da função run_game
            handle_events(player, projectile_group)

            update_game_objects(player, keys, [monster_group, projectile_group, experience_points_group])
            update_all_sprites(all_sprites, player, keys)

            score = collision_detection(player, monster_group, projectile_group, experience_points_group, rotating_projectile, score)
            detect_rotating_projectile_hits(monster_group, rotating_projectile, experience_points_group)

            if pygame.sprite.spritecollideany(player, monster_group):
                player.take_damage(current_time)

            if not player.alive:
                survival_time = (pygame.time.get_ticks() - start_ticks) // 1000
                if show_game_over_screen(screen, font, survival_time):
                    run_game()  # Reinicia o jogo
                else:
                    break

            # Atualiza a taxa de spawn mais rapidamente
            if current_time - last_spawn_rate_change > 30000:  # A cada 30 segundos
                current_monster_spawn_rate = max(min_monster_spawn_rate, current_monster_spawn_rate - spawn_rate_decrease)
                last_spawn_rate_change = current_time

            # Verifica se é hora de aumentar a velocidade dos monstros
            if current_time - last_speed_increase > 100000:  # 100 segundos
                for monster in monster_group:
                    monster.speed *= 1.09  # Aumenta a velocidade em 9%
                last_speed_increase = current_time

            # Gerar monstros
            monster_spawn_timer += clock.get_time()
            if monster_spawn_timer >= current_monster_spawn_rate:
                num_monsters_to_spawn = 1 + (current_time // 60000)  # Aumenta a cada minuto
                for _ in range(num_monsters_to_spawn):
                    spawn_pos = random_spawn_position()  # Certifique-se de que essa função retorna uma tupla (x, y)
                    monster_group.add(Monster(player, spawn_pos))
                monster_spawn_timer = 0

            render(screen, font, [player_group, monster_group, projectile_group, experience_points_group, all_sprites], player, start_ticks, score)

            clock.tick(60)
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    run_game()

