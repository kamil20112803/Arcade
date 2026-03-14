import arcade
import random
from player import Hero
from monstr import Monster
from vistrel import Bullet
from coin_rew import Coin

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Dungeon Grind"
CAMERA_LERP = 0.12


class Level1(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.hero = None
        self.walls = None
        self.doors = None
        self.roads = None
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

    def setup(self):
        self.hero = Hero()
        self.hero.center_x = 49 * 48
        self.hero.center_y = 4 * 48
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.hero)
        self.monsters = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        tile_map = arcade.load_tilemap("map_lvl1.tmx", scaling=3.0)
        self.walls = tile_map.sprite_lists["стены"]
        self.doors = tile_map.sprite_lists["дверь"]
        self.roads = tile_map.sprite_lists["дорога"]
        self.map_width = tile_map.width * tile_map.tile_width * 3
        self.map_height = tile_map.height * tile_map.tile_height * 3

    def spawn_monster(self):
        if len(self.roads) == 0:
            return
        road = random.choice(self.roads)
        monster = Monster(road.center_x, road.center_y, self.walls)
        self.monsters.append(monster)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.roads.draw()
        self.walls.draw()
        self.doors.draw()
        self.all_sprites.draw()
        self.monsters.draw()
        self.bullets.draw()
        self.coins.draw()
        self.gui_camera.use()
        arcade.draw_text(f"Coins: {self.hero.coins}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Health: {self.hero.health}", 10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 20)

    def on_update(self, delta_time):
        self.hero.update(delta_time)
        self.physics_engine = arcade.PhysicsEngineSimple(self.hero, self.walls)
        self.physics_engine.update()
        self.spawn_timer += delta_time
        if self.spawn_timer >= 10.0:
            self.spawn_monster()
            self.spawn_timer = 0
        for monster in self.monsters:
            monster.update(delta_time, self.hero.center_x, self.hero.center_y, self.bullets)
            if monster.dead:
                coin = Coin(monster.center_x, monster.center_y)
                self.coins.append(coin)
            monster.try_hit_player(self.hero)
        self.bullets.update()
        self.coins.update(delta_time)
        for coin in self.coins:
            if arcade.check_for_collision(self.hero, coin):
                self.hero.coins += 1
                coin.remove_from_sprite_lists()
        self.world_camera.position = self.hero.center_x, self.hero.center_y
        door_hit = arcade.check_for_collision_with_list(self.hero, self.doors)
        if door_hit and self.hero.coins >= 100:
            print("Переход на уровень 2 (заглушка)")

    def on_key_press(self, key, modifiers):
        self.hero.on_key_press(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            world_x, world_y = self._get_mouse_coordinates()
            bullet = self.hero.shoot(world_x, world_y)
            if bullet:
                self.bullets.append(bullet)

    def on_key_release(self, key, modifiers):
        self.hero.on_key_release(key, modifiers)

    def _get_mouse_coordinates(self):
        x, y = self._mouse_x, self._mouse_y
        x += self.world_camera.position[0] - SCREEN_WIDTH // 2
        y += self.world_camera.position[1] - SCREEN_HEIGHT // 2
        return x, y


def main():
    game = Level1()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()