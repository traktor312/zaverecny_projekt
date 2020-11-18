from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.vector import Vector
from random import randint

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

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    # Metoda pro umístění míčku na střed a zahájení hry
    def serve_ball(self):
        # Nastavení rychlosti míčku na 4
        self.ball.speed = 4
        # Umístění míčku na střed
        self.ball.center_x = self.width / 2
        self.ball.center_y = self.height / 2
        # Nastavení směru míčku
        self.ball.velocity = Vector(self.ball.speed, 0).rotate(randint(-45, 45) + 180 * randint(0, 1))
        # self.ball.velocity = Vector(self.ball.speed, 0)

    # Hlavní smyčka
    def update(self, dt):
        players = [self.player1, self.player2]

        # Volám metodu ball.move(), která pohybuje s míčem a zjišťuje kolize s pádly
        self.ball.move(players, self.width)

        for player in players:
            player.move()

        # Pokuď se míč dotkne horního nebo dolního okraje, odrazí se
        if (self.ball.y < 0) or (self.ball.y > self.height - 50):
            self.ball.velocity_y *= -1

        # Pokuď se míček dotkne levého okraje
        if self.ball.x < 0:
            # Umístí míček na střed a zahájí hru
            self.serve_ball()
            # Přičte bod hráči na pravo
            self.player2.score += 1

        # Pokuď se míček dotkne pravého okraje
        if self.ball.x > self.width - 50:
            # Umístí míček na střed a zahájí hru
            self.serve_ball()
            # Přičte bod hráči na levo
            self.player1.score += 1

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
