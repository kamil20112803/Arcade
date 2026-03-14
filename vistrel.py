import arcade


class Bullet(arcade.Sprite):
    def __init__(self, x, y, vel_x, vel_y):
        super().__init__("images/bullet.png", scale=1.0)
        self.center_x = x
        self.center_y = y
        self.change_x = vel_x
        self.change_y = vel_y

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y