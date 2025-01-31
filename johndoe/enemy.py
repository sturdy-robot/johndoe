import pygame
from pygame.sprite import GroupSingle


class EnemyStats:
    def __init__(self, max_health: int, damage: int, shield: int):
        self._health = max_health
        self._shield = shield
        self.damage = damage
        self.max_health = max_health
        self.max_shield = shield

    @property
    def shield(self):
        return self._shield

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int):
        value = min(value, self.max_health)
        value = max(0, value)
        self._health = value

    @shield.setter
    def shield(self, value: int):
        value = min(value, self.max_shield)
        value = max(0, value)
        self._shield = value

    def apply_damage(self, damage: int):
        if self.shield > 0:
            self.shield -= damage
        else:
            self.health -= damage


class EnemySprite(pygame.sprite.Sprite):
    def __init__(
        self,
        enemy_sprite: pygame.Surface,
        stats: EnemyStats,
        speed: int,
        player: GroupSingle,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup
    ):
        super().__init__(*groups)
        self.images = {
            "right": pygame.transform.flip(enemy_sprite, True, False),
            "left": enemy_sprite,
        }
        self.stats = stats
        self.image = self.images["right"]
        self.rect = self.image.get_frect()
        self.hitbox = self.rect.inflate(-2, -2)
        self.direction = pygame.math.Vector2()
        self.speed = speed
        self.rect.center = pos
        self.player = player

    def get_player_direction(self):
        if self.direction.x > 0:
            self.image = self.images["right"]
        else:
            self.image = self.images["left"]
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
        health: int,
        shield: int,
        damage: int,
        score: int = 1,
    ):
        self.stats = EnemyStats(health, damage, shield)
        self.sprite = EnemySprite(enemy_sprite, self.stats, speed, player, pos)
        self.damage = damage
        self.score = score

    def update(self, dt: float):
        self.sprite.update(dt)
