from kivy.app import App
from kivy.clock import Clock

from game import PongGame
from kivy.config import Config
from kivy.core.window import Window


Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '360')
Config.write()
Window.size = (640, 360)


class PongApp(App):
    def build(self):
        game = PongGame()
        # Zahájí hru
        game.serve_ball()
        # Spouští smyčku, frekvence 60Hz
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


PongApp().run()
