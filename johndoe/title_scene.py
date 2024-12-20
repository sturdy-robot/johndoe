import pygame
from .scene import Scene
from .definitions import WIDTH, HEIGHT
from pygame.freetype import Font
from .scene_manager import SceneManager


class TitleScene(Scene):
    def __init__(self):
        self.title_surface = None
        self.title_rect = None
        self.start_game_label = None
        self.start_game_rect = None
        self.font = Font("assets/Silver.ttf", size=20)
        self.scene_manager = SceneManager()

    def setup(self):
        self.title_surface = pygame.image.load(
            "assets/title_screen.png"
        ).convert_alpha()
        self.title_rect = self.title_surface.get_frect(center=(WIDTH // 2, HEIGHT // 2))
        self.start_game_label, self.start_game_rect = self.font.render(
            "Press enter to start", fgcolor=(255, 255, 255)
        )
        self.start_game_rect.bottomright = self.title_rect.bottomright
        self.start_game_rect.x -= 15
        self.start_game_rect.y -= 50

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.title_surface, self.title_rect)
        surface.blit(self.start_game_label, self.start_game_rect)

    def handle_events(self, event: pygame.event.Event):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_RETURN]:
            self.scene_manager.change_scene("level")
