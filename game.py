from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.core.window import Window
from kivy.vector import Vector
from random import randint
from kivy.clock import Clock

from paddle import PongPaddle
from ball import PongBall


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    width = NumericProperty(640)
    height = NumericProperty(360)

    def __init__(self, models, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.player2.x = 624
        self.player1_ai = None if models[0] is None else models[0]
        self.player2_ai = None if models[1] is None else models[1]

    def start(self):
        self.serve_ball()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    # Metoda pro umístění míčku na střed a zahájení hry
    def serve_ball(self):
        # Nastavení rychlosti míčku na 4
        self.ball.speed = self.ball.min_speed
        # Umístění míčku na střed
        self.ball.x = (self.width - self.ball.width) / 2
        self.ball.y = (self.height - self.ball.height) / 2
        # Nastavení směru míčku
        self.ball.velocity = Vector(self.ball.speed, 0).rotate(randint(-45, 45) + 180 * randint(0, 1))
        self.ball.last_velocity_x = self.ball.velocity_x
        # self.ball.velocity = Vector(self.ball.speed, 0)
        self.player1.y = (self.height - self.player1.height) / 2
        self.player2.y = (self.height - self.player2.height) / 2

        if self.player1_ai is not None:
            self.player1_ai.episode_start(self.observation())
        if self.player2_ai is not None:
            self.player2_ai.episode_start(self.observation())

    # Hlavní smyčka
    def update(self, dt):
        self.step()

        self.player1.last_score = self.player1.score
        self.player2.last_score = self.player2.score
        self.ball.last_velocity_x = self.ball.velocity_x

        # Volám metodu ball.move(), která pohybuje s míčem a zjišťuje kolize s pádly
        players = [self.player1, self.player2]
        self.ball.move(players, self.width)

        for player in players:
            player.move(self.height)

        # Pokuď se míč dotkne horního nebo dolního okraje, odrazí se
        if self.ball.y <= 0 and self.ball.velocity_y < 0:
            self.ball.velocity_y *= -1

        if self.ball.y >= self.height - self.ball.height and self.ball.velocity_y > 0:
            self.ball.velocity_y *= -1

        # Pokuď se míček dotkne levého okraje
        if self.ball.x < 0:
            # Přičte bod hráči na pravo
            self.player2.score += 1

        # Pokuď se míček dotkne pravého okraje
        if self.ball.x > self.width - self.ball.width:
            # Přičte bod hráči na levo
            self.player1.score += 1

        rewards, done = self.rewards_done()
        if self.player1_ai is not None:
            self.player1_ai.step(self.observation(), rewards[0], done)
        if self.player2_ai is not None:
            self.player2_ai.step(self.observation(), rewards[1], done)

        if done:
            if self.player1_ai is not None:
                self.player1_ai.episode_end()
            if self.player2_ai is not None:
                self.player2_ai.episode_end()
            self.serve_ball()

    # Ovládání pádel pomocí klávesnice, stisknutí tlačítka
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode)
        # Testy pro tlačítka, která nás zajímají
        if keycode[1] == 'w':
            self.player1.up = True
            self.player1.down = False
        if keycode[1] == 'up':
            self.player2.up = True
            self.player2.down = False
        if keycode[1] == 's':
            self.player1.down = True
            self.player1.up = False
        if keycode[1] == 'down':
            self.player2.down = True
            self.player2.up = False

    # Ovládání pádel pomocí klávesnice, puštění tlačítka
    def _on_keyboard_up(self, keyboard, keycode):
        # print("---------")
        # print(keycode)
        # Testy pro tlačítka, která nás zajímají
        if keycode[1] == 'w':
            self.player1.up = False
        if keycode[1] == 'up':
            self.player2.up = False
        if keycode[1] == 's':
            self.player1.down = False
        if keycode[1] == 'down':
            self.player2.down = False

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def observation(self):
        obs = [(self.player1.y + self.player1.height / 2) / (self.height - self.player1.height),
               (self.player2.y + self.player2.height / 2) / (self.height - self.player2.height),
               round((self.ball.x + self.ball.width / 2) / (self.width - self.ball.width), 3),
               round((self.ball.y + self.ball.height / 2) / (self.height - self.ball.height), 3),
               round((self.ball.velocity_x + self.ball.max_speed) / (2 * self.ball.max_speed), 3),
               round((self.ball.velocity_y + self.ball.max_speed) / (2 * self.ball.max_speed), 3)]
        return obs

    def test_bounce(self):
        return False if self.ball.last_velocity_x * self.ball.velocity_x > 0 else True

    def rewards_done(self):
        rewards = [0, 0]
        done = False
        if self.test_bounce():
            if self.ball.x < self.width / 2:
                rewards = [1, 0]
            else:
                rewards = [0, 1]
        if self.player1.last_score != self.player1.score:
            rewards = [0, -1]
            done = True
        if self.player2.last_score != self.player2.score:
            rewards = [-1, 0]
            done = True
        return rewards, done

    def step(self):
        if self.player1_ai is not None:
            action = self.player1_ai.choose_action()
            self.player1.up = False
            self.player1.down = False
            if action == 0:
                self.player1.up = True
            if action == 1:
                self.player1.down = True
        if self.player2_ai is not None:
            action = self.player2_ai.choose_action()
            self.player2.up = False
            self.player2.down = False
            if action == 0:
                self.player2.up = True
            if action == 1:
                self.player2.down = True
