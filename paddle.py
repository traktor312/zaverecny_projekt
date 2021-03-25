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
    speed = NumericProperty(4)
    up = False
    down = False
    last_score = NumericProperty(0)

    # Metoda pro odražení míčku
    def bounce_ball(self, ball, width):
        # Pokuď mířek narazí do pádla
        if ball.x <= self.x + self.width and ball.x + ball.width >= self.x and \
                ball.y <= self.y + self.height and ball.y + ball.height >= self.y:
            # Zjistí, kterým směrem má míček odrazit podle toho na jaké straně se nachází míček (pomocí width)
            direction = -1
            if self.x < width / 2:
                direction = 1
            # Zvýší rychlost tak, aby nebyla vyšší než 35
            # ball.speed *= 1.1
            if ball.speed > ball.max_speed:
                ball.speed = ball.max_speed
            # Odrazí míček od pádla a to až o 60° (ze středu pádla 0°, z kraje pádla 60°)
            ball.velocity = Vector(direction * ball.speed, 0).rotate(
                (ball.y + ball.height / 2 - self.y - self.height / 2)/self.height * (60 * direction))
            return True
        return False

    # Metoda pro pohyb pádlem
    def move(self, height):
        if self.up:
            self.y += self.speed
            if self.y + self.height >= height:
                self.y = height - self.height
        if self.down:
            self.y -= self.speed
            if self.y <= 0:
                self.y = 0
