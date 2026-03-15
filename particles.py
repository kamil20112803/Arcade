import arcade
import random
import math


class TeleportParticle(arcade.SpriteCircle):
    def __init__(self, x, y):
        color = random.choice([
            (100, 200, 255, 255),
            (150, 100, 255, 255),
            (200, 150, 255, 255),
            (255, 100, 150, 255)
        ])
        size = random.randint(4, 8)
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        self.alpha = 255
        self.lifetime = random.uniform(0.5, 1.0)
        self.time_alive = 0
        self.scale = 1.0

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.alpha -= 4
        self.scale_x *= 0.97
        self.scale_y *= 0.97
        self.time_alive += delta_time
        if self.time_alive >= self.lifetime or self.alpha <= 0:
            self.alpha = 0
            return True
        return False


def spawn_teleport_particles(x, y, count=30):
    particles = arcade.SpriteList()
    for _ in range(count):
        particle = TeleportParticle(x, y)
        particles.append(particle)
    return particles