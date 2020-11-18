from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.vector import Vector

"""
    Třída PongPaddle - skóre hráče a detekte kolize s míčem
    Atributy:
        score - skóre hráče
    Metody:
        bouce_ball(self, ball, width) - detekce kolize s míčkem, 
            width - šířka okna pro zjišnění, na které straně je míček 
            a na kterou stranu se má odrazit
        move(self) - pohyb pádlem pomocí klávesnice
"""


class PongPaddle(Widget):
    score = NumericProperty(0)
    up = False
    down = False

    # Metoda pro odražení míčku
    def bounce_ball(self, ball, width):
        # Pokuď mířek narazí do pádla
        if self.collide_widget(ball):
            # Zjistí, kterým směrem má míček odrazit podle toho na jaké straně se nachází míček (pomocí width)
            direction = -1
            if self.x < width / 4:
                direction = 1
            # Zvýší rychlost tak, aby nebyla vyšší než 35
            ball.speed *= 1.1
            if ball.speed > 35:
                ball.speed = 35
            # Odrazí míček od pádla a to až o 60° (ze středu pádla 0°, z kraje pádla 60°)
            ball.velocity = Vector(direction * ball.speed, 0).rotate(
                (ball.center_y - self.center_y)/100 * (60 * direction))

    # Metoda pro pohyb pádlem
    def move(self):
        if self.up:
            self.y += 3
        if self.down:
            self.y -= 3
