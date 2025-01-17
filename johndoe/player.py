import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        angle,
        direction,
        *groups: pygame.sprite.AbstractGroup
    ) -> None:
        super().__init__(*groups)
        self.time_alive = 1500
        self.time_started = pygame.time.get_ticks()
        self.image = pygame.image.load("assets/bullet.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_frect(center=pos)
        self.angle = math.radians(angle)
        self.speed = 350
        self.direction = direction

    def update(self, dt: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

        if pygame.time.get_ticks() - self.time_started > self.time_alive:
            self.kill()


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
        self.original_image = self.image
        self.rect.center = pos
        self.facing = "right"

    def get_image(self):
        self.image = self.images[self.facing]


class PlayerStats:
    def __init__(self):
        self._health = 100
        self._energy = 100
        self.max_health = 100
        self.max_energy = 100

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int):
        value = min(value, self.max_health)
        value = max(0, value)
        self._health = value

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value: int):
        value = min(value, self.max_energy)
        value = max(0, value)
        self._energy = value


class Player:
    def __init__(self, pos: tuple[int, int]):
        self.player_sprite = PlayerSprite(pos)
        self.direction = pygame.math.Vector2()
        self.speed = 150
        self.target_direction = pygame.math.Vector2()

    def update(self, dt: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.player_sprite.rect.x += self.direction.x * self.speed * dt
        self.player_sprite.rect.y += self.direction.y * self.speed * dt

    def handle_events(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.player_sprite.facing = "left"
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.player_sprite.facing = "right"
        else:
            self.direction.x = 0

        self.player_sprite.get_image()
