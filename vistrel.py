import arcade
import math
import random


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__("images/bullet.png", scale=2.0)
        self.center_x = start_x
        self.center_y = start_y

        dx = target_x - start_x
        dy = target_y - start_y
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.change_x = (dx / dist) * 800
            self.change_y = (dy / dist) * 800
            self.angle = 270 - math.degrees(math.atan2(dy, dx))
            print(self.angle)
        else:
            self.change_x = 0
            self.change_y = 0
            self.angle = 0

        self.distance_traveled = 0
        self.max_distance = random.randint(400, 500)

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        step = math.hypot(self.change_x * delta_time, self.change_y * delta_time)
        self.distance_traveled += step
        if self.distance_traveled >= self.max_distance:
            self.remove_from_sprite_lists()