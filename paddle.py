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

    def __init__(self, **kwargs):
        super(PongPaddle, self).__init__(**kwargs)
        self.game_y = 17.5
        self.game_x = 0
        self.game_height = 10
        self.game_width = 2

    # Metoda pro odražení míčku
    def bounce_ball(self, ball, width):
        # Pokuď mířek narazí do pádla
        if ball.game_x <= self.game_x + self.game_width and ball.game_x + ball.game_width >= self.game_x and \
                ball.game_y <= self.game_y + self.game_height and ball.game_y + ball.game_height >= self.game_y:
            # Zjistí, kterým směrem má míček odrazit podle toho na jaké straně se nachází míček (pomocí width)
            direction = -1
            if self.game_x < width / 2:
                direction = 1
            # Zvýší rychlost tak, aby nebyla vyšší než 35
            ball.speed *= 1.1
            if ball.speed > 2.5:
                ball.speed = 2.5
            # Odrazí míček od pádla a to až o 60° (ze středu pádla 0°, z kraje pádla 60°)
            ball.velocity = Vector(direction * ball.speed, 0).rotate(
                (ball.game_y + ball.game_height / 2 - self.game_y - self.game_height / 2)/10 * (60 * direction))
            return True
        return False

    # Metoda pro pohyb pádlem
    def move(self):
        if self.up:
            self.game_y += 1
        if self.down:
            self.game_y -= 1
