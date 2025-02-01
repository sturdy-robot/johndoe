import math
import pygame
from pygame.freetype import Font
import random

from johndoe.enemy import Enemy
from johndoe.game_clock import GameClock
from johndoe.weapon import WeaponManager, WeaponType
from johndoe.collectibles import (
    CollectibleSprite,
    CollectibleType,
    get_collectible_probability,
)
from .scene import Scene
from .definitions import WIDTH, HEIGHT
from .player import Player
from .camera import Camera
from .ui import UI
from .scene_manager import SceneManager
from .scores import ScoreKeeper


class WorldScene(Scene):
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.player = Player((WIDTH // 2, HEIGHT // 2))
        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.enemies_spr = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.weapons = WeaponManager(
            self.player_sprite_group, self.enemies_spr, self.projectiles
        )
        self.active_collectibles = self.get_default_collectibles()
        self.collectibles_spr = pygame.sprite.Group()
        self.font = Font("assets/Silver.ttf", size=30)
        self.score_keeper = ScoreKeeper()
        self.font.antialiased = False
        self.game_clock = GameClock()
        self.player_score = 0
        self.min_enemies = 5
        self.max_enemies = 50
        self.min_health = 10
        self.max_health = 20
        self.update_enemy_max_count = 2 * 60 * 1000
        self.last_update_count = self.game_clock.get_time()
        self.enemies = []
        self.camera = Camera(
            self.player_sprite_group,
            self.player_sprite_group,
            self.enemies_spr,
            self.projectiles,
            self.collectibles_spr,
        )
        self.ui = None
        self.spr_enemies = [
            pygame.image.load("assets/enemy1_spr.png").convert_alpha(),
            pygame.image.load("assets/enemy2_spr.png").convert_alpha(),
            pygame.image.load("assets/enemy3_spr.png").convert_alpha(),
            pygame.image.load("assets/enemy4_spr.png").convert_alpha(),
            pygame.image.load("assets/enemy5_spr.png").convert_alpha(),
        ]
        self.enemy_spawn_cooldown = 5000
        self.last_enemy_spawn = 0
        self.scene_manager = SceneManager()

    def get_default_collectibles(self):
        return [
            None,
            CollectibleType.HEALTH,
            CollectibleType.BULLET,
            CollectibleType.GUN,
            CollectibleType.FIRE,
        ]

    def setup(self):
        self.enemies.clear()
        self.enemies_spr.empty()
        self.projectiles.empty()
        self.player_sprite_group.empty()
        self.collectibles_spr.empty()
        self.active_collectibles = self.get_default_collectibles()
        self.min_enemies = 5
        self.max_enemies = 20
        self.update_enemy_max_count = 2 * 60 * 1000
        self.last_update_count = self.game_clock.get_time()
        self.game_clock.reset_clock()
        self.player_score = 0
        self.player = Player(self.surface.get_rect().center)
        self.player_sprite_group.add(self.player.player_sprite)
        self.spawn_enemies()
        en_spr = [enemy.sprite for enemy in self.enemies]
        self.last_time_dmg_applied = 0
        self.enemies_spr.add(en_spr)
        self.weapons.reset()
        self.camera.setup()
        self.ui = UI(self.player)
        self.ui.setup()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/game_music.mp3")
        pygame.mixer.music.play(loops=-1)

    def check_is_game_over(self):
        if self.player.stats.health <= 0:
            self.score_keeper.write_scores(
                self.player_score, self.game_clock.get_time()
            )
            self.scene_manager.change_scene("game_over")

    def check_enemy_spawn_time(self):
        now = self.game_clock.get_time()
        time = now - self.last_enemy_spawn
        update_count = now - self.last_update_count

        if update_count > self.update_enemy_max_count:
            self.min_enemies *= 1.25
            self.min_enemies = int(self.min_enemies)
            self.max_enemies *= 1.25
            self.max_enemies = int(self.max_enemies)
            self.min_health *= 1.05
            self.min_health = int(self.min_health)
            self.max_health *= 1.05
            self.max_health = int(self.max_health)
            self.player.speed *= 1.10
            self.last_update_count = now

        if time > self.enemy_spawn_cooldown:
            self.spawn_enemies()

    def spawn_enemies(self):
        num_enemies = random.randint(self.min_enemies, self.max_enemies)
        for _ in range(num_enemies):
            sprite = random.choice(self.spr_enemies)
            distance = random.randint(300, 500)
            angle = random.uniform(0, 2 * math.pi)
            pos_x = self.player_sprite_group.sprite.rect.x + math.cos(angle) * distance
            pos_y = self.player_sprite_group.sprite.rect.y + math.sin(angle) * distance
            pos = (pos_x, pos_y)
            health = random.randint(self.min_health, self.max_health)
            damage = random.randint(1, 10)
            shield = random.randint(1, 10)
            speed = random.randint(20, 60)
            self.enemies.append(
                Enemy(
                    sprite, speed, self.player_sprite_group, pos, health, shield, damage
                )
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

        for enemy in self.enemies_spr.sprites():
            for projectile in self.projectiles.sprites():
                if enemy.hitbox.colliderect(projectile.rect):
                    enemy.stats.health -= projectile.damage
                    projectile.kill()

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

        for collectible in self.collectibles_spr.sprites():
            if self.player.player_sprite.hitbox.colliderect(collectible.rect):
                match collectible.c_type:
                    case CollectibleType.HEALTH:
                        self.player.stats.health += 10
                    case CollectibleType.GUN:
                        self.weapons.add_weapon(WeaponType.GUN)
                    case CollectibleType.BULLET:
                        self.weapons.add_projectiles(WeaponType.GUN)
                    case CollectibleType.FIRE:
                        self.weapons.add_weapon(WeaponType.FIRE)
                    case CollectibleType.GAS:
                        self.weapons.add_projectiles(WeaponType.FIRE)
                self.max_enemies *= 1.05
                self.min_enemies *= 1.05
                self.max_enemies = int(self.max_enemies)
                self.min_enemies = int(self.min_enemies)
                self.max_health *= 1.15
                self.max_health = int(self.max_health)
                self.min_health *= 1.15
                self.min_health = int(self.min_health)

                collectible.kill()

    def handle_collisions(self, dt: float):
        self.handle_enemy_collisions(dt)
        self.handle_player_collisions(dt)

    def get_collectible(self, pos: tuple[float, float]):
        probabilities = get_collectible_probability()
        collectible_types = list(probabilities.keys())
        for collectible in collectible_types:
            if collectible not in self.active_collectibles:
                del probabilities[collectible]

        all_types = list(probabilities.keys())
        probs = list(probabilities.values())

        all_types.append("None")
        probs.append(0.7)

        collectible = random.choices(all_types, probs)[0]
        if collectible != "None":
            collectible = CollectibleSprite(pos, collectible, self.collectibles_spr)

    def check_enemy_death(self):
        enemies = self.enemies.copy()
        for enemy in enemies:
            if enemy.stats.health == 0:
                self.get_collectible(enemy.sprite.rect.center)
                self.enemies.remove(enemy)
                enemy.sprite.kill()
                self.player_score += 10

    def update_player_collectibles(self):
        if (
            WeaponType.FIRE in self.weapons.get_weapon_types()
            and CollectibleType.GAS not in self.active_collectibles
        ):
            self.active_collectibles.append(CollectibleType.GAS)

    def update(self, dt: float):
        self.game_clock.update()
        if self.game_clock.paused:
            return
        if not self.enemies:
            self.spawn_enemies()

        self.update_player_collectibles()
        self.weapons.update(dt)
        self.player.update(dt)
        self.camera.update(dt)
        self.handle_collisions(dt)
        self.check_enemy_spawn_time()
        self.check_enemy_death()
        self.check_is_game_over()

    def draw_player_score(self):
        position = self.surface.get_rect().topright
        surface, rect = self.font.render(
            f"Score: {self.player_score}", fgcolor=(255, 255, 255), size=18
        )
        rect.topright = position
        rect.x -= 5
        rect.y += 5
        self.surface.blit(surface, rect)

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
        rect.y += 5
        self.surface.blit(surface, rect)

    def draw(self, surface: pygame.Surface):
        self.surface.fill("darkorchid4")
        self.camera.draw(self.surface)
        self.ui.draw(self.surface)
        self.draw_current_time()
        self.draw_player_score()
        surface.blit(self.surface, (0, 0))
