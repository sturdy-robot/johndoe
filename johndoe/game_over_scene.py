import pygame
from pygame.freetype import Font
from .scene import Scene
from .definitions import WIDTH, HEIGHT
from .scene_manager import SceneManager


class GameOverScene(Scene):
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.font = Font("assets/Silver.ttf", size=50)
        self.font.antialiased = False
        self.surfaces: list[tuple[pygame.Surface, pygame.Rect]] = []
        self.scene_manager = SceneManager()

    def setup(self):
        self.surfaces.clear()
        game_over_surf, game_over_rect = self.font.render("Game Over", (255, 255, 255))
        game_over_rect.center = self.surface.get_rect().center
        self.surfaces.append((game_over_surf, game_over_rect))
        press_r_surf, press_r_rect = self.font.render(
            "Press R to restart", (255, 255, 255), size=20
        )
        press_r_rect.center = game_over_rect.center
        press_r_rect.centery += 15 + press_r_rect.height
        self.surfaces.append((press_r_surf, press_r_rect))

    def update(self, dt: float):
        pass

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                self.scene_manager.change_scene("level")

    def draw(self, surface: pygame.surface.Surface):
        self.surface.fill((175, 24, 13, 100))
        for surf in self.surfaces:
            surf, rect = surf
            self.surface.blit(surf, rect)
        surface.blit(self.surface, (0, 0))
