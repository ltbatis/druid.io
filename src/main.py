import pygame
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            fire_projectiles(player, projectile_group)
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

def run_game():
    font = initialize_pygame()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Druid.io")
    clock = pygame.time.Clock()

    player, player_group, projectile_group, monster_group, experience_points_group, rotating_projectile, all_sprites = create_game_objects()
    monster_spawn_timer = 0
    monster_spawn_rate = 5000
    score = 0
    start_ticks = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
                # Continuação da função run_game
        handle_events(player, projectile_group)

        update_game_objects(player, keys, [monster_group, projectile_group, experience_points_group])
        update_all_sprites(all_sprites, player, keys)

        score = collision_detection(player, monster_group, projectile_group, experience_points_group, rotating_projectile, score)
        detect_rotating_projectile_hits(monster_group, rotating_projectile, experience_points_group)

        if pygame.sprite.spritecollideany(player, monster_group):
            player.take_damage(current_time)

        if not player.alive:
            break

        # Adiciona novos monstros com base no temporizador
        monster_spawn_timer += clock.get_time()
        if monster_spawn_timer >= monster_spawn_rate:
            monster_group.add(Monster(player))
            monster_spawn_timer = 0

        render(screen, font, [player_group, monster_group, projectile_group, experience_points_group, all_sprites], player, start_ticks, score)

        clock.tick(60)

if __name__ == "__main__":
    run_game()

