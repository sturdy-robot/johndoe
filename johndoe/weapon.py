from os import close
import random
import pygame
import math
from enum import Enum, auto
from .singleton import Singleton
from .player import Bullet, Player, PlayerStats
from .game_clock import GameClock


class WeaponType(Enum):
    GUN = auto()
    FIRE = auto()


class Weapon:
    def __init__(
        self,
        player: pygame.sprite.GroupSingle,
        enemies: pygame.sprite.AbstractGroup,
        damage: int,
        cooldown: int,
        speed: int,
        projectiles: pygame.sprite.AbstractGroup,
    ):
        self.player = player
        self.enemies = enemies
        self.damage = damage
        self.cooldown = cooldown
        self.game_clock = GameClock()
        self.speed = speed
        self.current_cooldown = self.cooldown
        self.num_projectiles = 1
        self.projectiles = projectiles
        self.last_used_time = self.game_clock.get_time()

    def update(self, dt: float):
        current_time = self.game_clock.get_time()
        if self.current_cooldown <= 0:
            self.last_used_time = current_time
            self.current_cooldown = self.cooldown
            self.attack(dt)
        else:
            self.current_cooldown -= current_time - self.last_used_time

    def attack(self, dt: float):
        pass


class GunWeapon(Weapon):
    def __init__(self, player, enemies, damage, cooldown, speed, projectiles):
        super().__init__(player, enemies, damage, cooldown, speed, projectiles)

    def update(self, dt: float):
        return super().update(dt)

    def attack(self, dt: float):
        player_pos = pygame.math.Vector2(self.player.sprite.rect.center)
        enemies = sorted(
            self.enemies,
            key=lambda enemy: pygame.math.Vector2(enemy.rect.center).distance_to(
                player_pos
            ),
        )
        for i in range(self.num_projectiles):
            closest_enemy = enemies[i]
            closest_enemy_rect = pygame.math.Vector2(closest_enemy.rect.center)
            direction = (
                (closest_enemy_rect - player_pos).normalize()
                if closest_enemy_rect != player_pos
                else pygame.math.Vector2(0, 0)
            )
            angle = player_pos.angle_to(closest_enemy_rect)
            Bullet(
                self.player.sprite.rect.center,
                angle,
                self.damage,
                direction,
                self.projectiles,
            )


class FireWeapon(Weapon):
    def __init__(
        self,
        player: pygame.sprite.GroupSingle,
        enemies: pygame.sprite.AbstractGroup,
        damage: int,
        cooldown: int,
        speed: int,
        projectiles: pygame.sprite.AbstractGroup,
    ):
        super().__init__(player, enemies, damage, cooldown, speed, projectiles)

    def update(self, dt: float):
        return super().update(dt)

    def attack(self, dt: float):
        return super().attack(dt)


WEAPON_FACTORY = {
    WeaponType.GUN: GunWeapon,
    WeaponType.FIRE: FireWeapon,
}


class WeaponManager(metaclass=Singleton):
    def __init__(
        self,
        player: pygame.sprite.GroupSingle,
        enemies: pygame.sprite.AbstractGroup,
        projectiles: pygame.sprite.AbstractGroup,
    ):
        self.weapons = {}
        self.player = player
        self.enemies = enemies
        self.projectiles = projectiles

    def add_weapon(self, weapon_type: WeaponType):
        if weapon_type not in self.weapons:
            self.weapons[weapon_type] = WEAPON_FACTORY[weapon_type](
                self.player, self.enemies, 10, 25000, 350, self.projectiles
            )
        else:
            self.weapons[weapon_type].num_projectiles += 1

    def add_projectiles(self, weapon_type):
        self.weapons[weapon_type].num_projectiles += 1

    def update(self, dt: float):
        for weapon in self.weapons.values():
            weapon.update(dt)

    def get_weapon_types(self):
        return self.weapons.keys()

    def reset(self):
        self.weapons.clear()
        self.add_weapon(WeaponType.GUN)
