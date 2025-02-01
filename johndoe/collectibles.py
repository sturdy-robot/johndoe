import pygame
from enum import Enum, auto

from pygame.sprite import AbstractGroup


class CollectibleType(Enum):
    HEALTH = auto()
    GUN = auto()
    FIRE = auto()
    BULLET = auto()
    GAS = auto()


def get_collectible_probability() -> dict[CollectibleType, float]:
    return {
        CollectibleType.HEALTH: 0.10,
        CollectibleType.GUN: 0.005,
        CollectibleType.BULLET: 0.005,
        CollectibleType.FIRE: 0.005,
        CollectibleType.GAS: 0.005,
    }


class CollectibleSprite(pygame.sprite.Sprite):
    collectible_sprites = {
        CollectibleType.HEALTH: pygame.image.load("assets/health_spr.png"),
        CollectibleType.GUN: pygame.image.load("assets/gun_spr.png"),
        CollectibleType.FIRE: pygame.image.load("assets/fire_spr.png"),
        CollectibleType.BULLET: pygame.image.load("assets/bullet_spr.png"),
        CollectibleType.GAS: pygame.image.load("assets/gas_spr.png"),
    }

    def __init__(
        self,
        pos: tuple[float, float],
        c_type: CollectibleType,
        *groups: list[AbstractGroup],
    ):
        super().__init__(*groups)
        self.image = self.collectible_sprites[c_type].convert_alpha()
        self.c_type = c_type
        self.rect = self.image.get_frect(center=pos)
