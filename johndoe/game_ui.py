import pygame

from johndoe.scene import Scene
from .player import Player


class GameUI(Scene):
    def __init__(self, player: Player):
        self.player = player
