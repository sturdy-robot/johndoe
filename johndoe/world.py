import pygame
import random

from johndoe.enemy import Enemy
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

    def setup(self):
        enemies_spr = [
            pygame.image.load("assets/enemy1_spr.png").convert_alpha(),
            pygame.image.load("assets/vindoe_spr.png").convert_alpha(),
        ]
        enemies = []
        for _ in range(50):
            sprite = random.choice(enemies_spr)
            pos = (random.randint(0, 1000), random.randint(0, 1000))
            enemies.append(Enemy(sprite, 50, pos))
        en_spr = [enemy.sprite for enemy in enemies]
        self.enemies.add(en_spr)
        self.player_sprite_group.add(self.player.player_sprite)
        self.camera.setup()

    def handle_events(self, event: pygame.event.Event):
        self.player.handle_events(event)
        self.camera.handle_events(event)

    def update(self, dt: float):
        self.player.update(dt)
        self.camera.update(dt)

    def draw(self, surface: pygame.Surface):
        self.surface.fill("aquamarine4")
        self.camera.draw(self.surface)
        surface.blit(self.surface, (0, 0))
