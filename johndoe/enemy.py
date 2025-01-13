import pygame


class EnemySprite(pygame.sprite.Sprite):
    def __init__(
        self,
        enemy_sprite: pygame.Surface,
        speed: int,
        pos: tuple[int, int],
        *groups: pygame.sprite.AbstractGroup
    ):
        super().__init__(*groups)
        self.image = enemy_sprite
        self.rect = self.image.get_frect()
        self.direction = pygame.math.Vector2()
        self.speed = speed
        self.rect.center = pos

    def update(self, dt: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.speed * self.direction.x * dt
        self.rect.y += self.speed * self.direction.y * dt


class Enemy:
    def __init__(self, enemy_sprite: pygame.Surface, speed: int, pos: tuple[int, int]):
        self.sprite = EnemySprite(enemy_sprite, speed, pos)

    def update(self, dt: float):
        self.sprite.update(dt)
