import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class VictoryView(arcade.View):
    def __init__(self, coins):
        super().__init__()
        self.coins = coins
        self.highscore = 0
        self.load_highscore()

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0
        if self.coins > self.highscore:
            self.highscore = self.coins
            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "VICTORY!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
            arcade.color.GOLD,
            72,
            anchor_x="center"
        )
        arcade.draw_text(
            f"Your score: {self.coins}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 20,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )
        arcade.draw_text(
            f"Highscore: {self.highscore}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 20,
            arcade.color.GOLD,
            24,
            anchor_x="center"
        )
        arcade.draw_text(
            "You have conquered the dungeon!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 70,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )
        arcade.draw_text(
            "Press any key to return to menu",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        from main import StartView
        self.window.show_view(StartView())