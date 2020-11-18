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
    speed = NumericProperty(4)

    # Metoda pro pohyb a test kolize s pádly
    def move(self, players, width):
        s = self.speed
        # Pohybuje s míčkem po malých částech aby neproletěl pádly
        while s > 0:
            # Pohne míčkem
            self.pos = Vector(self.velocity_x / self.speed, self.velocity_y / self.speed) + self.pos
            # Pro oba hráče
            for player in players:
                # Testuje kolizi s hráčem
                player.bounce_ball(self, width)
            s -= 1
