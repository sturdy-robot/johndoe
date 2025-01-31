import random
import pygame
import math
from .player import Bullet, Player, PlayerStats
from .game_clock import GameClock


class Weapon:
    def __init__(
        self,
        player: Player,
        enemies: pygame.sprite.AbstractGroup,
        damage: int,
        cooldown: int,
        speed: int,
        projectiles: pygame.sprite.AbstractGroup,
    ):
        self.player = player
        self.enemies = enemies
        self.damage = damage
        self.cooldown = cooldown
        self.game_clock = GameClock()
        self.speed = speed
        self.current_cooldown = self.cooldown
        self.num_projectiles = 1
        self.projectiles = projectiles
        self.last_used_time = self.game_clock.get_time()

    def update(self, dt: float):
        current_time = self.game_clock.get_time()
        print(self.current_cooldown)
        if self.current_cooldown <= 0:
            self.last_used_time = current_time
            self.current_cooldown = self.cooldown
            self.attack(dt)
        else:
            self.current_cooldown -= current_time - self.last_used_time

    def attack(self, dt: float):
        for _ in range(self.num_projectiles):
            closest_enemy = None
            min_distance = float("inf")
            for enemy in self.enemies.sprites():
                distance = math.sqrt(
                    (enemy.rect.x - self.player.player_sprite.rect.x) ** 2
                    + (enemy.rect.y - self.player.player_sprite.rect.y) ** 2
                )
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy

            player_rect = pygame.math.Vector2(self.player.player_sprite.rect.center)
            enemy_rect = pygame.math.Vector2(closest_enemy.rect.center)
            direction = player_rect - enemy_rect
            angle = player_rect.angle_to(enemy_rect)
            Bullet(
                self.player.player_sprite.rect.center,
                angle,
                self.damage,
                direction,
                self.projectiles,
            )
