import arcade
import random
import math


class Monster(arcade.Sprite):
    def __init__(self, x, y, walls_list):
        texture = random.choice(["m1", "m2"])
        super().__init__(f"images/{texture}.png", scale=3.0)
        self.center_x = x
        self.center_y = y
        self.speed = 65
        self.health = 5
        self.dead = False
        self.walls = walls_list
        self.damage_cooldown = 0

    def update(self, delta_time, player_x, player_y, bullet_list):
        dx = player_x - self.center_x
        dy = player_y - self.center_y
        dist = math.hypot(dx, dy)

        if dist > 0:
            new_x = self.center_x + (dx / dist) * self.speed * delta_time
            new_y = self.center_y + (dy / dist) * self.speed * delta_time

            old_x, old_y = self.center_x, self.center_y
            self.center_x, self.center_y = new_x, new_y

            if arcade.check_for_collision_with_list(self, self.walls):
                self.center_x, self.center_y = old_x, old_y

        for bullet in bullet_list:
            if arcade.check_for_collision(self, bullet):
                self.health -= 1
                bullet.remove_from_sprite_lists()
                if self.health <= 0:
                    self.dead = True
                    self.remove_from_sprite_lists()
                break

        self.damage_cooldown -= delta_time

    def try_hit_player(self, player):
        if self.damage_cooldown <= 0 and arcade.check_for_collision(self, player):
            player.health -= 1
            self.damage_cooldown = 1.0
            return True
        return False