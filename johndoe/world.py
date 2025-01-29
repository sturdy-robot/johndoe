import math
import pygame
from pygame.freetype import Font
import random

from johndoe.enemy import Enemy
from johndoe.game_clock import GameClock
from .scene import Scene
from .definitions import WIDTH, HEIGHT
from .player import Player
from .camera import Camera
from .ui import UI
from .scene_manager import SceneManager


class WorldScene(Scene):
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.player = Player((WIDTH // 2, HEIGHT // 2))
        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.enemies_spr = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.weapons_spr = pygame.sprite.Group()
        self.weapons = []
        self.font = Font("assets/Silver.ttf", size=30)
        self.font.antialiased = False
        self.enemies = []
        self.camera = Camera(
            self.player_sprite_group, self.player_sprite_group, self.enemies_spr
        )
        self.game_clock = GameClock()
        self.ui = None
        self.spr_enemies = [
            pygame.image.load("assets/enemy1_spr.png").convert_alpha(),
            pygame.image.load("assets/vindoe_spr.png").convert_alpha(),
        ]
        self.enemy_spawn_cooldown = 5000
        self.last_enemy_spawn = 0
        self.scene_manager = SceneManager()

    def setup(self):
        self.weapons.clear()
        self.enemies.clear()
        self.enemies_spr.empty()
        self.projectiles.empty()
        self.weapons_spr.empty()
        self.player_sprite_group.empty()
        self.game_clock.reset_clock()
        self.player = Player(self.surface.get_rect().center)
        self.player_sprite_group.add(self.player.player_sprite)
        self.spawn_enemies()
        en_spr = [enemy.sprite for enemy in self.enemies]
        self.last_time_dmg_applied = 0
        self.enemies_spr.add(en_spr)
        self.camera.setup()
        self.ui = UI(self.player)
        self.ui.setup()

    def check_is_game_over(self):
        if self.player.stats.health <= 0:
            self.scene_manager.change_scene("game_over")

    def check_enemy_spawn_time(self):
        now = self.game_clock.get_time()
        time = now - self.last_enemy_spawn
        if time > self.enemy_spawn_cooldown:
            self.spawn_enemies()

    def spawn_enemies(self):
        num_enemies = random.randint(5, 20)
        for _ in range(num_enemies):
            sprite = random.choice(self.spr_enemies)
            distance = random.randint(300, 500)
            angle = random.uniform(0, 2 * math.pi)
            pos_x = self.player_sprite_group.sprite.rect.x + math.cos(angle) * distance
            pos_y = self.player_sprite_group.sprite.rect.y + math.sin(angle) * distance
            pos = (pos_x, pos_y)
            health = random.randint(10, 20)
            damage = random.randint(1, 10)
            shield = random.randint(1, 10)
            self.enemies.append(
                Enemy(sprite, 50, self.player_sprite_group, pos, health, shield, damage)
            )
        self.enemies_spr.add([enemy.sprite for enemy in self.enemies])
        self.last_enemy_spawn = self.game_clock.get_time()
        print(f"{num_enemies} spawned")

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.game_clock.toggle_pause()

        if self.game_clock.paused:
            return

        self.player.handle_events(event)
        self.camera.handle_events(event)

    def handle_enemy_collisions(self, dt):
        for i, enemy1 in enumerate(self.enemies_spr.sprites()):
            for j, enemy2 in enumerate(self.enemies_spr.sprites()):
                if i != j and enemy1.rect.colliderect(enemy2.rect):
                    overlap_x = min(
                        enemy1.rect.right - enemy2.rect.left,
                        enemy2.rect.right - enemy1.rect.left,
                    )
                    overlap_y = min(
                        enemy1.rect.bottom - enemy2.rect.top,
                        enemy2.rect.bottom - enemy1.rect.top,
                    )

                    if overlap_x < overlap_y:
                        if enemy1.rect.centerx < enemy2.rect.centerx:
                            enemy1.rect.x -= overlap_x / 2
                            enemy2.rect.x += overlap_x / 2
                        else:
                            enemy1.rect.x += overlap_x / 2
                            enemy2.rect.x -= overlap_x / 2
                    else:
                        if enemy1.rect.centery < enemy2.rect.centery:
                            enemy1.rect.y -= overlap_y / 2
                            enemy2.rect.y += overlap_y / 2
                        else:
                            enemy1.rect.y += overlap_y / 2
                            enemy2.rect.y -= overlap_y / 2

    def handle_player_collisions(self, dt: float):
        damage = 0
        now = self.game_clock.get_time()
        for enemy in self.enemies:
            if enemy.sprite.hitbox.colliderect(self.player.player_sprite.hitbox):
                damage += enemy.damage

        if damage > 0:
            if now - self.last_time_dmg_applied > 500:
                self.player.stats.health -= damage
                self.last_time_dmg_applied = now

    def handle_collisions(self, dt: float):
        self.handle_enemy_collisions(dt)
        self.handle_player_collisions(dt)

    def check_enemy_death(self):
        enemies = self.enemies.copy()
        for enemy in enemies:
            if enemy.stats.health == 0:
                self.enemies.remove(enemy)
                enemy.sprite.kill()

    def update(self, dt: float):
        self.game_clock.update()
        if self.game_clock.paused:
            return
        self.player.update(dt)
        self.camera.update(dt)
        self.handle_collisions(dt)
        self.check_enemy_spawn_time()
        self.check_enemy_death()
        self.check_is_game_over()

    def draw_current_time(self):
        position = self.surface.get_rect().midtop
        total_seconds = int(self.game_clock.get_time() / 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        hours = total_seconds // 3600
        time_result = f"{minutes:02d}:{seconds:02d}"
        if hours > 0:
            time_result = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        surface, rect = self.font.render(
            "Time: " + time_result, fgcolor=(255, 255, 255)
        )
        rect.midtop = position
        self.surface.blit(surface, rect)

    def draw(self, surface: pygame.Surface):
        self.surface.fill("aquamarine4")
        self.camera.draw(self.surface)
        self.ui.draw(self.surface)
        self.draw_current_time()
        surface.blit(self.surface, (0, 0))
