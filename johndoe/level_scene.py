import pygame
from .scene import Scene
from .definitions import WIDTH, HEIGHT
from .player import Player


class LevelScene(Scene):
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.player = Player((WIDTH // 2, HEIGHT // 2))

    def setup(self):
        pass

    def handle_events(self, event: pygame.event.Event):
        self.player.handle_events(event)

    def update(self, dt: float):
        self.player.update(dt)

    def draw(self, surface: pygame.Surface):
        self.surface.fill("aquamarine4")
        self.player.draw(self.surface)
        surface.blit(self.surface, (0, 0))
