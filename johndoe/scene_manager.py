import pygame

from .scene import Scene
from typing import Optional
from .singleton import Singleton


class SceneManager(metaclass=Singleton):
    def __init__(self):
        self.scenes: dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None

    def setup(self):
        if self.current_scene is not None:
            self.current_scene.setup()

    def update(self, dt: float):
        if self.current_scene is not None:
            self.current_scene.update(dt)

    def draw(self, surface: pygame.Surface):
        if self.current_scene is not None:
            self.current_scene.draw(surface)

    def handle_events(self, event: pygame.event.Event):
        if self.current_scene is not None:
            self.current_scene.handle_events(event)

    def change_scene(self, scene: str = "title"):
        self.current_scene = self.scenes[scene]
        self.setup()

    def add_scene(self, name: str, scene: Scene):
        self.scenes[name] = scene
