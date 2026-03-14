import arcade


class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/items/coinGold.png", scale=0.5)
        self.center_x = x
        self.center_y = y
        self.lifetime = 5.0
        self.time_alive = 0

    def update(self, delta_time):
        self.time_alive += delta_time
        if self.time_alive >= self.lifetime:
            self.remove_from_sprite_lists()