import pygame
from .player import Player


class Weapon:
    def __init__(
        self, name: str, icon: str, damage: int, cooldown: float, player: Player
    ):
        self.name = name
        self.icon = icon
        self.damage = damage
        self.cooldown = cooldown
        self.player = player

    def update(self, dt: float):
        pass
