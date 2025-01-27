import pygame

from johndoe.player import Player
from .scene import Scene
from .definitions import WIDTH, HEIGHT


class UI(Scene):
    def __init__(self, player: Player):
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.player = player
        self.healthbar_rect = pygame.Rect(0, 0, 150, 10)
        self.energybar_rect = pygame.Rect(0, 0, 150, 10)
        self.expbar_rect = pygame.Rect(0, 0, 150, 8)

    def setup_bars(self):
        corner = self.surface.get_rect().topleft
        self.healthbar_rect.topleft = corner[0] + 20, corner[1] + 10
        self.energybar_rect.topleft = (
            self.healthbar_rect.bottomleft[0],
            self.healthbar_rect.bottomleft[1] + 5,
        )
        self.expbar_rect.topleft = (
            self.energybar_rect.bottomleft[0],
            self.energybar_rect.bottomleft[1] + 5,
        )

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

    def draw_energybar(self):
        current_value = self.player.stats.energy
        max_value = self.player.stats.max_energy
        pygame.draw.rect(self.surface, (34, 34, 34), self.energybar_rect.inflate(6, 5))
        ratio = current_value / max_value
        bar_width = self.energybar_rect.width * ratio
        pygame.draw.rect(
            self.surface,
            "cyan3",
            (
                self.energybar_rect.x,
                self.energybar_rect.y,
                bar_width,
                self.energybar_rect.height,
            ),
        )

    def draw_expbar(self):
        current_value = self.player.exp.exp
        max_value = self.player.exp.exp_to_next_level
        pygame.draw.rect(self.surface, (34, 34, 34), self.expbar_rect.inflate(6, 5))
        ratio = current_value / max_value
        bar_width = self.expbar_rect.width * ratio
        pygame.draw.rect(
            self.surface,
            "yellow",
            (
                self.expbar_rect.x,
                self.expbar_rect.y,
                bar_width,
                self.expbar_rect.height,
            ),
        )

    def draw_bars(self):
        self.draw_healthbar()
        self.draw_energybar()
        self.draw_expbar()

    def draw(self, surface: pygame.Surface):
        self.draw_bars()
        surface.blit(self.surface, (0, 0))
