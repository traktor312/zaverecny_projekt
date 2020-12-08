from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector

"""
    Třída PongBall - míček
    Atributy:
        velocity - směr, kterým se míček pohybuje
        speed - rychlost míčku
    Metody:
        move(self, players, width) - pohyb míčkem a test kolize s pádly (players)
            - pohybuje s míčkem po částech aby neproletěl skrz pádlo
"""


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    speed = NumericProperty(1)

    def __init__(self, **kwargs):
        super(PongBall, self).__init__(**kwargs)
        self.game_y = 21.5
        self.game_x = 40
        self.game_height = 2
        self.game_width = 2

    # Metoda pro pohyb a test kolize s pádly
    def move(self, players, width):
        s = self.speed
        bounce = False
        # Pohybuje s míčkem po malých částech aby neproletěl pádly
        while s > 0:
            # Pohne míčkem
            self.game_x += self.velocity_x / self.speed / 10.0
            self.game_y += self.velocity_y / self.speed / 10.0
            # Pro oba hráče
            for player in players:
                # Testuje kolizi s hráčem
                if not bounce:
                    bounce = player.bounce_ball(self, width)
            s -= 0.1
