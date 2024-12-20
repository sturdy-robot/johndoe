import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self, pos: tuple[int, int], angle, *groups: pygame.sprite.AbstractGroup
    ) -> None:
        super().__init__(*groups)
        self.time_alive = 1500
        self.time_started = pygame.time.get_ticks()
        self.image = pygame.image.load("assets/bullet.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_frect(center=pos)
        self.angle = math.radians(angle)
        self.vel_x = math.cos(self.angle) * 200
        self.vel_y = -math.sin(self.angle) * 200

    def update(self, dt: float):
        self.rect.x += self.vel_x * dt
        self.rect.y += self.vel_y * dt

        if pygame.time.get_ticks() - self.time_started > self.time_alive:
            self.kill()


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load("assets/johndoespr.png").convert_alpha()
        self.rect = self.image.get_frect()
        self.original_image = self.image
        self.rect.center = pos
        self.pos = pygame.math.Vector2(pos)


class Player:
    def __init__(self, pos: tuple[int, int]):
        self.player_sprite = PlayerSprite(pos)
        self.direction = pygame.math.Vector2()
        self.speed = 150
        self.target_direction = pygame.math.Vector2()
        self.bullets = pygame.sprite.Group()

    def update(self, dt: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.player_sprite.rect.x += self.direction.x * self.speed * dt
        self.player_sprite.rect.y += self.direction.y * self.speed * dt

        self.player_sprite.pos.x = self.player_sprite.rect.x
        self.player_sprite.pos.y = self.player_sprite.rect.y

        self.bullets.update(dt)

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
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        direction = pygame.mouse.get_pos() - self.player_sprite.pos
        _, angle = direction.as_polar()
        self.player_sprite.image = pygame.transform.rotate(
            self.player_sprite.original_image, -angle
        )
        self.player_sprite.rect = self.player_sprite.image.get_frect(
            center=self.player_sprite.rect.center
        )
        mouse_key = pygame.mouse.get_just_pressed()
        if mouse_key[0]:
            bullet = Bullet(self.player_sprite.rect.center, -angle)
            self.bullets.add(bullet)

    def draw(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()

        surface.blit(self.player_sprite.image, self.player_sprite.rect)
        pygame.draw.circle(surface, "red", mouse_pos, 2)
        if self.bullets.sprites():
            self.bullets.draw(surface)
        self.player_sprite.rect.clamp_ip(surface.get_rect())
