import arcade
from pyglet.graphics import Batch

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class VictoryView(arcade.View):
    def __init__(self, coins):
        super().__init__()
        self.batch = Batch()
        self.coins = coins
        self.highscore = 0
        self.title_text = None
        self.score_text = None
        self.highscore_text = None
        self.message_text = None
        self.restart_text = None
        self.load_highscore()
        self.setup_text()

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

    def setup_text(self):
        self.title_text = arcade.Text(
            "VICTORY!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
            arcade.color.GOLD,
            72,
            anchor_x="center",
            batch=self.batch
        )
        self.score_text = arcade.Text(
            f"Your score: {self.coins}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 20,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            batch=self.batch
        )
        self.highscore_text = arcade.Text(
            f"Highscore: {self.highscore}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 20,
            arcade.color.GOLD,
            24,
            anchor_x="center",
            batch=self.batch
        )
        self.message_text = arcade.Text(
            "You have conquered the dungeon!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 70,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            batch=self.batch
        )
        self.restart_text = arcade.Text(
            "Press any key to return to menu",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            arcade.color.WHITE,
            18,
            anchor_x="center",
            batch=self.batch
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        from main import StartView
        self.window.show_view(StartView())