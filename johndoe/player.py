import pygame
import math
from .game_clock import GameClock


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.images = {
            "right": pygame.image.load("assets/johndoe_spr.png").convert_alpha(),
            "left": pygame.transform.flip(
                pygame.image.load("assets/johndoe_spr.png"), True, False
            ),
        }
        self.image = pygame.image.load("assets/johndoe_spr.png").convert_alpha()
        self.rect = self.image.get_frect()
        self.hitbox = self.rect.inflate(-5, -5)
        self.original_image = self.image
        self.rect.center = pos
        self.facing = "right"

    def get_image(self):
        self.image = self.images[self.facing]


class PlayerStats:
    def __init__(self):
        self._health = 100
        self.max_health = 100

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int):
        value = min(value, self.max_health)
        value = max(0, value)
        self._health = value


class Player:
    def __init__(self, pos: tuple[int, int]):
        self.player_sprite = PlayerSprite(pos)
        self.direction = pygame.math.Vector2()
        self.speed = 150.0
        self.target_direction = pygame.math.Vector2()
        self.stats = PlayerStats()

    def update(self, dt: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.player_sprite.rect.x += self.direction.x * self.speed * dt
        self.player_sprite.rect.y += self.direction.y * self.speed * dt
        self.player_sprite.hitbox.center = self.player_sprite.rect.center

    def handle_events(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.player_sprite.facing = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.player_sprite.facing = "right"
        else:
            self.direction.x = 0

        self.player_sprite.get_image()
