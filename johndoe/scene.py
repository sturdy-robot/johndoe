import pygame
from abc import ABC, abstractmethod


class Scene(ABC):
    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def handle_events(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass
