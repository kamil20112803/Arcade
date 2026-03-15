import arcade
import random
import math
import time
from player import Hero
from monstr import Monster
from vistrel import Bullet
from coin_rew import Coin

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CAMERA_LERP = 0.12


class UltraBullet(arcade.Sprite):
    def __init__(self, start_x, start_y, angle_deg):
        super().__init__("images/bullet.png", scale=2.0)
        self.center_x = start_x
        self.center_y = start_y
        angle_rad = math.radians(angle_deg)
        self.change_x = math.cos(angle_rad) * 800
        self.change_y = math.sin(angle_rad) * 800
        self.angle = angle_deg
        self.distance_traveled = 0
        self.max_distance = 300

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.distance_traveled += math.hypot(self.change_x * delta_time, self.change_y * delta_time)
        if self.distance_traveled >= self.max_distance:
            self.remove_from_sprite_lists()


class Level3(arcade.View):
    def __init__(self):
        super().__init__()
        self.hero = None
        self.ground = None
        self.walls = None
        self.doors = None
        self.monsters = None
        self.bullets = None
        self.coins = None
        self.all_sprites = None
        self.physics_engine = None
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.spawn_timer = 0
        self.map_width = 0
        self.map_height = 0
        self.ultra_shots = 3
        self.last_ultra_time = 0
        self.ultra_cooldown = 30

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self, previous_hero):
        self.hero = previous_hero
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.hero)
        self.monsters = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        tile_map = arcade.load_tilemap("map_lvl3.tmx", scaling=3.0)
        self.ground = tile_map.sprite_lists["пол"]
        self.walls = tile_map.sprite_lists["стены"]
        self.doors = tile_map.sprite_lists["дверь"]
        self.map_width = tile_map.width * tile_map.tile_width * 3
        self.map_height = tile_map.height * tile_map.tile_height * 3
        self.hero.center_x = (tile_map.width // 2) * tile_map.tile_width * 3 + (tile_map.tile_width * 3 // 2)
        self.hero.center_y = (tile_map.height // 2) * tile_map.tile_height * 3 + (tile_map.tile_height * 3 // 2)
        self.ultra_shots = 3
        self.last_ultra_time = time.time()

    def spawn_monster(self):
        if len(self.ground) == 0:
            return
        attempts = 0
        while attempts < 50:
            ground = random.choice(self.ground)
            wall_collision = False
            for wall in self.walls:
                if abs(ground.center_x - wall.center_x) < 10 and abs(ground.center_y - wall.center_y) < 10:
                    wall_collision = True
                    break
            if not wall_collision:
                monster = Monster(ground.center_x, ground.center_y, self.walls)
                self.monsters.append(monster)
                return
            attempts += 1

    def spawn_ultra_shot(self, x, y):
        for i in range(9):
            angle = i * 45
            bullet = UltraBullet(x, y, angle)
            self.bullets.append(bullet)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.ground.draw()
        self.walls.draw()
        self.doors.draw()
        self.all_sprites.draw()
        self.monsters.draw()
        self.bullets.draw()
        self.coins.draw()
        self.gui_camera.use()
        arcade.draw_text(f"Coins: {self.hero.coins}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Health: {self.hero.health}", 10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 20)
        arcade.draw_text(f"Ultra shots: {self.ultra_shots}", 10, SCREEN_HEIGHT - 90, arcade.color.GOLD, 20)
        current_time = time.time()
        if self.ultra_shots < 3 and current_time - self.last_ultra_time >= self.ultra_cooldown:
            arcade.draw_text("ULTRA READY!", SCREEN_WIDTH // 2, 50, arcade.color.GREEN, 24, anchor_x="center")

    def on_update(self, delta_time):
        self.hero.update(delta_time)
        self.physics_engine = arcade.PhysicsEngineSimple(self.hero, self.walls)
        self.physics_engine.update()
        self.spawn_timer += delta_time
        if self.spawn_timer >= 3.0:
            self.spawn_monster()
            self.spawn_timer = 0
        for monster in self.monsters:
            monster.update(delta_time, self.hero.center_x, self.hero.center_y, self.bullets)
            if monster.dead:
                coin = Coin(monster.center_x, monster.center_y)
                self.coins.append(coin)
            monster.try_hit_player(self.hero)
            if self.hero.health <= 0:
                from gameover import GameOverView
                self.window.show_view(GameOverView(self.hero.coins))
        self.bullets.update()
        self.coins.update(delta_time)
        for coin in self.coins:
            if arcade.check_for_collision(self.hero, coin):
                self.hero.coins += 10
                coin.remove_from_sprite_lists()
        self.world_camera.position = self.hero.center_x, self.hero.center_y
        current_time = time.time()
        if self.ultra_shots < 3 and current_time - self.last_ultra_time >= self.ultra_cooldown:
            self.ultra_shots += 1
            self.last_ultra_time = current_time
        door_hit = arcade.check_for_collision_with_list(self.hero, self.doors)
        if door_hit:
            from victory import VictoryView
            self.window.show_view(VictoryView(self.hero.coins))

    def on_key_press(self, key, modifiers):
        self.hero.on_key_press(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.ultra_shots > 0:
            self.spawn_ultra_shot(self.hero.center_x, self.hero.center_y)
            self.ultra_shots -= 1
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            world_x, world_y = self._get_mouse_coordinates(x, y)
            bullet = self.hero.shoot(world_x, world_y)
            if bullet:
                self.bullets.append(bullet)

    def on_key_release(self, key, modifiers):
        self.hero.on_key_release(key, modifiers)

    def _get_mouse_coordinates(self, x, y):
        x += self.world_camera.position[0] - SCREEN_WIDTH // 2
        y += self.world_camera.position[1] - SCREEN_HEIGHT // 2
        return x, y