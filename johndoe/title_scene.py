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
        self.surfaces = []
        self.items = 0
        self.font = Font("assets/Silver.ttf", size=30)
        self.font.antialiased = False
        self.scene_manager = SceneManager()

    def setup(self):
        self.surfaces.clear()
        self.title_surface = pygame.image.load(
            "assets/title_screen.png"
        ).convert_alpha()
        self.title_surface = pygame.transform.scale(self.title_surface, (WIDTH, HEIGHT))
        self.title_rect = self.title_surface.get_frect(center=(WIDTH // 2, HEIGHT // 2))
        start_game_label, start_game_rect = self.font.render(
            "Start Game", fgcolor=(255, 255, 255)
        )
        start_game_rect.bottomright = self.title_rect.bottomright
        start_game_rect.x -= 65
        start_game_rect.y -= 100
        high_scores_surf, high_scores_rect = self.font.render(
            "High Scores", fgcolor=(255, 255, 255)
        )
        high_scores_rect.center = start_game_rect.center
        high_scores_rect.y += high_scores_rect.height + 15
        pygame.mixer.music.load("assets/title_music.mp3")
        pygame.mixer.music.play(loops=-1)
        self.surfaces.append((start_game_label, start_game_rect))
        self.surfaces.append((high_scores_surf, high_scores_rect))

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.title_surface, self.title_rect)
        for i, surf in enumerate(self.surfaces):
            sur, rect = surf
            if i == self.items:
                pygame.draw.rect(
                    self.surface, "darkorchid3", rect.inflate(20, 12), border_radius=15
                )
            self.surface.blit(sur, rect)
        surface.blit(self.surface, (0, 0))

    def handle_events(self, event: pygame.event.Event):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_DOWN]:
            self.items = (self.items + 1) % len(self.surfaces)
        elif keys[pygame.K_UP]:
            self.items = (self.items - 1) % len(self.surfaces)

        if keys[pygame.K_RETURN]:
            if self.items == 0:
                self.scene_manager.change_scene("level")
            elif self.items == 1:
                self.scene_manager.change_scene("high_score")
