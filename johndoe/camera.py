import pygame

from johndoe.player import Player, PlayerSprite
from .scene import Scene
from .definitions import WIDTH, HEIGHT


class Camera(Scene):
    def __init__(
        self,
        player_sprite: pygame.sprite.GroupSingle,
        *groups: pygame.sprite.AbstractGroup
    ):
        self.groups = groups
        self.player_sprite = player_sprite
        self.surface = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.surface.get_frect()
        self.offset = pygame.math.Vector2()

    def setup(self):
        pass

    def handle_events(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def sprites(self) -> list[pygame.sprite.Sprite]:
        sprites = []
        for group in self.groups:
            sprites.extend(group.sprites())

        sprites.extend(self.player_sprite.sprites())

        return sprites

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0, 0, 0, 0))
        player_spr = self.player_sprite.sprites()[0]
        half_width, half_height = surface.get_frect().center
        self.offset.x, self.offset.y = (
            player_spr.rect.centerx - half_width,
            player_spr.rect.centery - half_height,
        )

        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.surface.blit(sprite.image, offset_pos)

        surface.blit(self.surface, self.rect)
