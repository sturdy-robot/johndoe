import pygame
import sys
from .definitions import PROJECT_NAME, VERSION, WIDTH, HEIGHT, FPS
from .scene_manager import SceneManager
from .title_scene import TitleScene
from .level_scene import LevelScene


class Game:
    def __init__(self):
        pygame.init()
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), self.flags)
        self.screen_rect = self.screen.get_rect()
        self.main_surface = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption(f"{PROJECT_NAME} {VERSION}")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene_manager = SceneManager()
        self.fps = FPS
        self.setup()

    def setup(self):
        self.scene_manager.add_scene("title", TitleScene())
        self.scene_manager.add_scene("level", LevelScene())
        self.scene_manager.change_scene("title")

    def update(self, dt: float):
        self.scene_manager.update(dt)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.scene_manager.handle_events(event)

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
        self.main_surface.fill((75, 89, 69))
        self.scene_manager.draw(self.main_surface)
        self.screen.blit(
            pygame.transform.scale(self.main_surface, self.screen_rect.size), (0, 0)
        )
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()
