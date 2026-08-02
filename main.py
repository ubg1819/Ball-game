import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_w, self.player_h = 150, 30
        self.player_x = Window.width / 2 - self.player_w / 2
        self.player_y = 40
        self.player_speed = 15

        self.star_size = 40
        self.star_x = random.randint(0, int(Window.width - self.star_size))
        self.star_y = Window.height
        self.star_speed = 6

        self.score = 0

        self.score_label = Label(
            text="Score: 0",
            font_size=30,
            pos=(10, Window.height - 60),
            size_hint=(None, None),
        )
        self.add_widget(self.score_label)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_touch_move(self, touch):
        # Move the player (basket) horizontally based on touch/drag position
        self.player_x = touch.x - self.player_w / 2
        if self.player_x < 0:
            self.player_x = 0
        if self.player_x > Window.width - self.player_w:
            self.player_x = Window.width - self.player_w

    def update(self, dt):
        self.star_y -= self.star_speed
        if self.star_y < 0:
            self.star_x = random.randint(0, int(Window.width - self.star_size))
            self.star_y = Window.height

        # collision check
        if (
            self.player_x < self.star_x + self.star_size
            and self.player_x + self.player_w > self.star_x
            and self.player_y < self.star_y + self.star_size
            and self.player_y + self.player_h > self.star_y
        ):
            self.score += 1
            self.star_x = random.randint(0, int(Window.width - self.star_size))
            self.star_y = Window.height
            self.star_speed += 0.3
            self.score_label.text = f"Score: {self.score}"

        self.canvas.clear()
        with self.canvas:
            Color(0.08, 0.08, 0.12)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))
            Color(0.27, 0.51, 0.86)
            Rectangle(
                pos=(self.player_x, self.player_y),
                size=(self.player_w, self.player_h),
            )
            Color(1, 0.86, 0.24)
            Rectangle(
                pos=(self.star_x, self.star_y),
                size=(self.star_size, self.star_size),
            )


class CatchStarsApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    CatchStarsApp().run()
