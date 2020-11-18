from kivy.app import App
from kivy.clock import Clock

from game import PongGame


class PongApp(App):
    def build(self):
        game = PongGame()
        # Zahájí hru
        game.serve_ball()
        # Spouští smyčku, frekvence 60Hz
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


PongApp().run()
