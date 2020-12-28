from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.vector import Vector
from random import randint
from ai2 import AI2
from kivy.clock import Clock

from paddle import PongPaddle
from ball import PongBall

"""
    Třída PongGame - tělo hry
    Atributy:
        ball - míček
        player1 - hráč na levo
        player2 - hráč na pravo
    Metody:
        serve_ball(self) - umístění míčku na střed, nastavení směru míčku a zahájení hry
        update(self, dt) - hlavní smyčka, veškerý pohyb, kolize a zvyšuje skóre
        on_touch_move(self, touch) - zaznamená kliknutí a pohyb kurzorem, pohybuje pádly
        _on_keyboard_down(self, keyboard, keycode, text, modifiers)
            - Ovládání pádel pomocí klávesnice, stisknutí tlačítka
        _on_keyboard_up(self, keyboard, keycode) - Ovládání pádel pomocí klávesnice, puštění tlačítka
"""


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    game_width = NumericProperty(80)
    game_height = NumericProperty(45)
    last_window_width = -1

    def __init__(self, models, players, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.player2.game_x = 78
        self.ai_players = [players[0], players[1]]
        self.player1_ai = None
        self.player2_ai = None
        self.set_ai(models[0], models[1])

    def start(self):
        self.serve_ball()
        Clock.schedule_interval(self.update, 1.0 / 50.0)

    def set_ai(self, model0, model1):
        if self.ai_players[0] == 1:
            self.player1_ai = model0
        if self.ai_players[1] == 1:
            self.player2_ai = model1

    # Metoda pro umístění míčku na střed a zahájení hry
    def serve_ball(self):
        # Nastavení rychlosti míčku na 4
        self.ball.speed = self.ball.min_speed
        # Umístění míčku na střed
        self.ball.game_x = (self.game_width - self.ball.game_width) / 2
        self.ball.game_y = (self.game_height - self.ball.game_height) / 2
        # Nastavení směru míčku
        self.ball.velocity = Vector(self.ball.speed, 0).rotate(randint(-45, 45) + 180 * randint(0, 1))
        # self.ball.velocity = Vector(self.ball.speed, 0)
        self.player1.game_y = (self.game_height - self.player1.game_height) / 2
        self.player2.game_y = (self.game_height - self.player2.game_height) / 2

        self.player1_ai.episode_start(self.observation(0))
        self.player2_ai.episode_start(self.observation(1))

    def update_window(self):
        self.ball.width = self.width / self.game_width * self.ball.game_width
        self.ball.height = self.height / self.game_height * self.ball.game_height
        self.player1.width = self.player2.width = self.width / self.game_width * self.player1.game_width
        self.player1.height = self.player2.height = self.height / self.game_height * self.player1.game_height
        self.last_window_width = self.width

    # Hlavní smyčka
    def update(self, dt):
        if self.last_window_width != self.width:
            self.update_window()

        actions = [self.player1_ai.choose_action(), self.player2_ai.choose_action()]
        self.step(actions)

        self.player1.last_score = self.player1.score
        self.player2.last_score = self.player2.score
        players = [self.player1, self.player2]

        # Volám metodu ball.move(), která pohybuje s míčem a zjišťuje kolize s pádly
        self.ball.move(players, self.game_width)

        for player in players:
            player.move(self.game_height)

        # Pokuď se míč dotkne horního nebo dolního okraje, odrazí se
        if self.ball.game_y <= 0 and self.ball.velocity_y < 0:
            self.ball.velocity_y *= -1

        if self.ball.game_y >= self.game_height - self.ball.game_height and self.ball.velocity_y > 0:
            self.ball.velocity_y *= -1

        # Pokuď se míček dotkne levého okraje
        if self.ball.game_x < 0:
            # Umístí míček na střed a zahájí hru
            # self.serve_ball()
            # Přičte bod hráči na pravo
            self.player2.score += 1

        # Pokuď se míček dotkne pravého okraje
        if self.ball.game_x > self.game_width - self.ball.game_width:
            # Umístí míček na střed a zahájí hru
            # self.serve_ball()
            # Přičte bod hráči na levo
            self.player1.score += 1

        rewards, done = self.rewards_done()
        self.player1_ai.step(self.observation(0), rewards[0], done)
        self.player2_ai.step(self.observation(1), rewards[1], done)

        if done:
            self.player1_ai.episode_end()
            self.player2_ai.episode_end()
            self.serve_ball()

        self.update_canvas()

    def update_canvas(self):
        w = self.width / self.game_width
        h = self.height / self.game_height
        self.ball.x = self.ball.game_x * w
        self.ball.y = self.ball.game_y * h
        self.player1.x = self.player1.game_x * w
        self.player1.y = self.player1.game_y * h
        self.player2.x = self.player2.game_x * w
        self.player2.y = self.player2.game_y * h

    # Po kliknutí a pohybu kurzorem
    def on_touch_move(self, touch):
        # Na levé čtvrtině obrazovky
        if touch.x < self.width / 1/4:
            # Posouvám pádlem podle kurzoru
            self.player1.center_y = touch.y
        # Na pravé čtvrtině obrazovky
        if touch.x > self.width * 3/4:
            # Posouvám pádlem podle kurzoru
            self.player2.center_y = touch.y

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

    def game_ai(self):
        if self.ai_players[0]:
            data = [self.player1.game_y, self.ball.game_x, self.ball.game_y,
                    self.ball.velocity_x, self.ball.velocity_y, self.player1.game_x]
            data = self.ai.validate_data(data)
            prediction = self.ai.predict(data)
            if prediction == 0:
                self.player1.up = True
                self.player1.down = False
            if prediction == 1:
                self.player1.up = False
                self.player1.down = True
            if prediction == 2:
                self.player1.up = False
                self.player1.down = False
        if self.ai_players[1]:
            data = [self.player2.game_y, self.ball.game_x, self.ball.game_y,
                    self.ball.velocity_x, self.ball.velocity_y, self.player2.game_x]
            data = self.ai.validate_data(data)
            prediction = self.ai.predict(data)
            if prediction == 0:
                self.player2.up = True
                self.player2.down = False
            if prediction == 1:
                self.player2.up = False
                self.player2.down = True
            if prediction == 2:
                self.player2.up = False
                self.player2.down = False

    def observation(self, player):
        if player == 0:
            obs = [self.player1.game_y / 35, round(self.ball.game_x / 78, 3), round(self.ball.game_y / 43, 3),
                   round((self.ball.velocity_x + 2.5) / 5, 3), round((self.ball.velocity_y + 2.5) / 5, 3)]
        if player == 1:
            obs = [self.player2.game_y / 35, round(self.ball.game_x / 78, 3), round(self.ball.game_y / 43, 3),
                   round((self.ball.velocity_x + 2.5) / 5, 3), round((self.ball.velocity_y + 2.5) / 5, 3)]
        return obs

    def rewards_done(self):
        rewards = [0, 0]
        done = False
        if self.ball.bounce:
            if self.ball.game_x < self.game_width / 2:
                rewards[0] = 1
            else:
                rewards[1] = 1
        if self.player1.last_score != self.player1.score:
            rewards = [0, -100]
            done = True
        if self.player2.last_score != self.player2.score:
            rewards = [-100, 0]
            done = True
        return rewards, done

    def step(self, actions):
        self.player1.up = False
        self.player1.down = False
        if actions[0] == 0:
            self.player1.up = True
        if actions[0] == 1:
            self.player1.down = True
        self.player2.up = False
        self.player2.down = False
        if actions[1] == 0:
            self.player2.up = True
        if actions[1] == 1:
            self.player2.down = True



