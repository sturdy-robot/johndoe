import pygame
from .player import Player
from .game_clock import GameClock


class Weapon:
    def __init__(
        self,
        name: str,
        icon: str,
        sprite: pygame.sprite.Sprite,
        damage: int,
        cooldown: float,
        player: Player,
    ):
        self.name = name
        self.icon = icon
        self.sprite = sprite
        self.damage = damage
        self.cooldown = cooldown
        self.player = player
        self.current_cooldown = 0
        self.game_clock = GameClock()
        self.last_used_time = self.game_clock.get_time()

    def attack(self):
        pass

    def update(self, dt: float):
        current_time = self.game_clock.get_time()
        if self.current_cooldown <= 0:
            self.last_used_time = current_time
            self.current_cooldown = self.cooldown
            self.attack()
        else:
            self.current_cooldown -= current_time - self.last_used_time
