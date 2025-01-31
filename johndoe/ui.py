import pygame

from johndoe.player import Player
from .scene import Scene
from .definitions import WIDTH, HEIGHT


class UI(Scene):
    def __init__(self, player: Player):
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.player = player
        self.healthbar_rect = pygame.Rect(0, 0, 150, 10)

    def setup_bars(self):
        corner = self.surface.get_rect().topleft
        self.healthbar_rect.topleft = corner[0] + 5, corner[1] + 5

    def setup(self):
        self.setup_bars()

    def update(self, dt: float):
        pass

    def handle_events(self, event: pygame.event.Event):
        pass

    def draw_healthbar(self):
        current_value = self.player.stats.health
        max_value = self.player.stats.max_health
        pygame.draw.rect(self.surface, (34, 34, 34), self.healthbar_rect.inflate(6, 5))
        ratio = current_value / max_value
        bar_width = self.healthbar_rect.width * ratio
        pygame.draw.rect(
            self.surface,
            "crimson",
            (
                self.healthbar_rect.x,
                self.healthbar_rect.y,
                bar_width,
                self.healthbar_rect.height,
            ),
        )

    def draw_bars(self):
        self.draw_healthbar()

    def draw(self, surface: pygame.Surface):
        self.draw_bars()
        surface.blit(self.surface, (0, 0))
