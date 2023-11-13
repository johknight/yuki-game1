#!/usr/bin/env python3

import pygame
from enemy import Enemy
from resource_manager import load_images
from player import Player
from bullet import Bullet
from config import *
from game_functions import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Yukinator")
clock = pygame.time.Clock()
   
def main():
    global ENEMY_SPEED, score, kill_counter, speed_level, last_bullet_fire_time, BULLET_COOLDOWN
    images = load_images()
    player = Player(images["player"], SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, 10)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    last_enemy_spawn_time = pygame.time.get_ticks()
    last_speed_increase = pygame.time.get_ticks()
    game_over = False

    running = True
    while running:
        draw_background(screen)

        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increase > SPEED_LEVEL_UPDATE_TIME:
            speed_level += 1
            ENEMY_SPEED += ENEMY_SPEED_INCREMENT
            last_speed_increase = current_time
            for enemy in enemies:
                enemy.speed = ENEMY_SPEED
            print(f"{speed_level}, {ENEMY_SPEED}") #debuggings
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move('left')
        if keys[pygame.K_d]:
            player.move('right')
        if keys[pygame.K_s] and current_time - last_bullet_fire_time > BULLET_COOLDOWN:
            new_bullet = Bullet(player.rect.centerx, player.rect.top, 20, images["bullet"])
            bullets.add(new_bullet)
            last_bullet_fire_time = current_time

        bullets.update()
        bullets.draw(screen)

        if pygame.time.get_ticks() - last_enemy_spawn_time > 1000:
            enemy = Enemy.spawn_enemy(images["enemy"])
            enemies.add(enemy)
            last_enemy_spawn_time = pygame.time.get_ticks()

        enemies.update()
        enemies.draw(screen)

        for enemy in list(enemies):
            if enemy.update():
                enemies.remove(enemy)
                game_over = reduce_player_health(player, 1)

        collisions = pygame.sprite.groupcollide(bullets, enemies, False, True)
        for collision in collisions:
            kill_counter += len(collisions[collision])
            score += POINTS_PER_ENEMY * len(collisions[collision])
            
        if pygame.sprite.spritecollide(player, enemies, dokill=True):
            game_over = reduce_player_health(player, 1)

        if game_over:
            running = False
            main_menu(images, screen, clock, start_game= lambda: start_game(main))

        player.draw(screen)
        player.display_health(screen)

        speed_level_text = pygame.font.SysFont(None, 36).render(f'Speed Level: {speed_level}', True, WHITE)
        screen.blit(speed_level_text, (10, 50))

        kill_text = pygame.font.SysFont(None, 36).render(f"Kills: {score}", True, WHITE)
        text_rect = kill_text.get_rect()
        text_rect.topright = (SCREEN_WIDTH - 100, 15)
        screen.blit(kill_text, text_rect.topright)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    images = load_images()
    main_menu(images, screen, clock, start_game= lambda: start_game(main))