import pygame
from pygame.sprite import GroupSingle
from .player import Player


class EnemySprite(pygame.sprite.Sprite):
    def __init__(
        self,
        enemy_sprite: pygame.Surface,
        speed: int,
        player: GroupSingle,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup
    ):
        super().__init__(*groups)
        self.image = enemy_sprite
        self.rect = self.image.get_frect()
        self.hitbox = self.rect.inflate(-5, -5)
        self.direction = pygame.math.Vector2()
        self.speed = speed
        self.rect.center = pos
        self.player = player

    def get_player_direction(self):
        player = self.player.sprite
        self.direction.x = player.rect.centerx - self.rect.centerx
        self.direction.y = player.rect.centery - self.rect.centery

    def update(self, dt: float):
        self.get_player_direction()
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.speed * self.direction.x * dt
        self.rect.y += self.speed * self.direction.y * dt
        self.hitbox.center = self.rect.center


class Enemy:
    def __init__(
        self,
        enemy_sprite: pygame.Surface,
        speed: int,
        player: GroupSingle,
        pos: tuple[int, int],
    ):
        self.sprite = EnemySprite(enemy_sprite, speed, player, pos)

    def update(self, dt: float):
        self.sprite.update(dt)
