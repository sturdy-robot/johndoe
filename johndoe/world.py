import pygame
import random

from johndoe.enemy import Enemy
from johndoe.game_clock import GameClock
from .scene import Scene
from .definitions import WIDTH, HEIGHT
from .player import Player
from .camera import Camera


class WorldScene(Scene):
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.player = Player((WIDTH // 2, HEIGHT // 2))
        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        self.camera = Camera(
            self.player_sprite_group, self.player_sprite_group, self.enemies
        )
        self.game_clock = GameClock()

    def setup(self):
        enemies_spr = [
            pygame.image.load("assets/enemy1_spr.png").convert_alpha(),
            pygame.image.load("assets/vindoe_spr.png").convert_alpha(),
        ]
        enemies = []
        for _ in range(50):
            sprite = random.choice(enemies_spr)
            pos = (random.randint(0, 1000), random.randint(0, 1000))
            enemies.append(Enemy(sprite, 50, self.player_sprite_group, pos))
        en_spr = [enemy.sprite for enemy in enemies]
        self.enemies.add(en_spr)
        self.player_sprite_group.add(self.player.player_sprite)
        self.camera.setup()

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.game_clock.toggle_pause()

        if self.game_clock.paused:
            return

        self.player.handle_events(event)
        self.camera.handle_events(event)

    def handle_enemy_collisions(self, dt):
        for i, enemy1 in enumerate(self.enemies.sprites()):
            for j, enemy2 in enumerate(self.enemies.sprites()):
                if i != j and enemy1.rect.colliderect(enemy2.rect):
                    overlap_x = min(
                        enemy1.rect.right - enemy2.rect.left,
                        enemy2.rect.right - enemy1.rect.left,
                    )
                    overlap_y = min(
                        enemy1.rect.bottom - enemy2.rect.top,
                        enemy2.rect.bottom - enemy1.rect.top,
                    )

                    if overlap_x < overlap_y:
                        if enemy1.rect.centerx < enemy2.rect.centerx:
                            enemy1.rect.x -= overlap_x / 2
                            enemy2.rect.x += overlap_x / 2
                        else:
                            enemy1.rect.x += overlap_x / 2
                            enemy2.rect.x -= overlap_x / 2
                    else:
                        if enemy1.rect.centery < enemy2.rect.centery:
                            enemy1.rect.y -= overlap_y / 2
                            enemy2.rect.y += overlap_y / 2
                        else:
                            enemy1.rect.y += overlap_y / 2
                            enemy2.rect.y -= overlap_y / 2

    def handle_player_collisions(self):
        for enemy in self.enemies.sprites():
            if self.player_sprite_group.sprite.rect.colliderect(enemy.rect):
                pass

    def handle_collisions(self, dt: float):
        self.handle_enemy_collisions(dt)
        self.handle_player_collisions()

    def update(self, dt: float):
        self.game_clock.update()
        if self.game_clock.paused:
            return
        self.player.update(dt)
        self.camera.update(dt)
        self.handle_collisions(dt)

    def draw(self, surface: pygame.Surface):
        self.surface.fill("aquamarine4")
        self.camera.draw(self.surface)
        surface.blit(self.surface, (0, 0))
