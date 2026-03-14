import arcade
import math
from vistrel import Bullet


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__("images/hero.png", scale=3.0)
        self.center_x = 100
        self.center_y = 200
        self.change_x = 0
        self.change_y = 0
        self.coins = 0
        self.health = 20
        self.health_regen_timer = 0

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.health_regen_timer += delta_time
        if self.health_regen_timer >= 5.0 and self.health < 20:
            self.health = min(20, self.health + 1)
            self.health_regen_timer = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.change_y = 10
        elif key == arcade.key.S:
            self.change_y = -10
        elif key == arcade.key.A:
            self.change_x = -10
        elif key == arcade.key.D:
            self.change_x = 1ы0

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.S]:
            self.change_y = 0
        if key in [arcade.key.A, arcade.key.D]:
            self.change_x = 0

    def shoot(self, target_x, target_y):
        from vistrel import Bullet
        return Bullet(self.center_x, self.center_y, target_x, target_y)