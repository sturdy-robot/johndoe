import pygame
from .scene import Scene
from .definitions import WIDTH, HEIGHT
from pygame.freetype import Font
from .scene_manager import SceneManager


class TitleScene(Scene):
    def __init__(self):
        self.surface = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.title_surface = None
        self.title_rect = None
        self.start_game_label = None
        self.start_game_rect = None
        self.font = Font("assets/Silver.ttf", size=30)
        self.font.antialiased = False
        self.scene_manager = SceneManager()

    def setup(self):
        self.title_surface = pygame.image.load(
            "assets/title_screen.png"
        ).convert_alpha()
        self.title_surface = pygame.transform.scale(self.title_surface, (WIDTH, HEIGHT))
        self.title_rect = self.title_surface.get_frect(center=(WIDTH // 2, HEIGHT // 2))
        self.start_game_label, self.start_game_rect = self.font.render(
            "Press Enter to start", fgcolor=(255, 255, 255)
        )
        self.start_game_rect.bottomright = self.title_rect.bottomright
        self.start_game_rect.x -= 65
        self.start_game_rect.y -= 100
        pygame.mixer.music.load("assets/title_music.mp3")
        pygame.mixer.music.play(loops=-1)

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.title_surface, self.title_rect)
        self.surface.blit(self.start_game_label, self.start_game_rect)
        surface.blit(self.surface, (0, 0))

    def handle_events(self, event: pygame.event.Event):
        keys = pygame.key.get_just_pressed()
        mouse_key = pygame.mouse.get_pressed()

        if keys[pygame.K_RETURN] or mouse_key[0]:
            self.scene_manager.change_scene("level")
