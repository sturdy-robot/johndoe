import pygame
from pygame.freetype import Font
from .scene import Scene
from .definitions import WIDTH, HEIGHT
from .scores import ScoreKeeper
from .scene_manager import SceneManager


class HighScoreScene(Scene):
    def __init__(self) -> None:
        self.surface = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.font = Font("assets/Silver.ttf", size=30)
        self.font.antialiased = False
        self.score_keeper = ScoreKeeper()
        self.scene_manager = SceneManager()
        self.surfaces = []

    def setup(self):
        high_score_title_surf, high_score_title_rect = self.font.render(
            "High Scores", (255, 255, 255)
        )
        high_score_title_rect.center = self.surface.get_rect().midtop
        high_score_title_rect.y += high_score_title_rect.height + 5

        self.surfaces.append((high_score_title_surf, high_score_title_rect))
        scores = self.score_keeper.read_scores()
        if not scores:
            no_scores_surf, no_scores_rect = self.font.render(
                "No scores found", (255, 255, 255), size=20
            )
            no_scores_rect.center = self.surface.get_rect().center
            self.surfaces.append((no_scores_surf, no_scores_rect))
        else:
            scores = sorted(scores, key=lambda score: score["score"], reverse=True)
            if len(scores) > 5:
                scores = scores[:5]
            for index, score in enumerate(scores):
                score_surf, score_rect = self.font.render(
                    f"{index + 1}. {score['created_time']} - {score['game_time']} seconds - {score['score']} points",
                    (255, 255, 255),
                    size=20,
                )
                score_rect.center = self.surface.get_rect().center
                score_rect.y += 15 * index + 5
                self.surfaces.append((score_surf, score_rect))

        return_surf, return_rect = self.font.render(
            "Press ESC to return", (255, 255, 255), size=20
        )
        return_rect.center = self.surface.get_rect().midbottom
        return_rect.y -= return_rect.height + 5
        self.surfaces.append((return_surf, return_rect))

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.surface.Surface):
        self.surface.fill("darkorchid4")
        for surf in self.surfaces:
            sur, rect = surf
            self.surface.blit(sur, rect)
        surface.blit(self.surface, (0, 0))

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.change_scene("title")
