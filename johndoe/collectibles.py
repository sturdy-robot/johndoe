import pygame
from enum import Enum, auto

from pygame.sprite import AbstractGroup

from johndoe.player import Player
from johndoe.weapon import WeaponManager, WeaponType


class CollectibleType(Enum):
    HEALTH = auto()
    GUN = auto()
    FIRE = auto()
    BULLET = auto()
    GAS = auto()


def get_collectible_probability() -> dict[CollectibleType, float]:
    return {
        CollectibleType.HEALTH: 0.10,
        CollectibleType.GUN: 0.05,
        CollectibleType.BULLET: 0.025,
        CollectibleType.FIRE: 0.05,
        CollectibleType.GAS: 0.025,
    }


class CollectibleSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[float, float],
        c_type: CollectibleType,
        *groups: list[AbstractGroup],
    ):
        super().__init__(*groups)
        self.image = pygame.surface.Surface((20, 20))
        self.c_type = c_type
        self.rect = self.image.get_frect(center=pos)
        match self.c_type:
            case CollectibleType.HEALTH:
                self.image.fill("chartreuse3")
            case CollectibleType.GUN:
                self.image.fill("gray25")
            case CollectibleType.FIRE:
                self.image.fill("crimson")
            case CollectibleType.BULLET:
                self.image.fill("khaki3")
            case CollectibleType.GAS:
                self.image.fill("lightpink2")
