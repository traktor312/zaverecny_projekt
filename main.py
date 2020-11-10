from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball, width):
        if self.collide_widget(ball):
            direction = -1
            if self.x < width / 4:
                direction = 1
            ball.speed *= 1.1
            if ball.speed > 35:
                ball.speed = 35
            ball.velocity = Vector(direction * ball.speed, 0).rotate(
                (ball.center_y - self.center_y)/100 * (60 * direction))


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    speed = NumericProperty(4)
    direction = NumericProperty(1)

    def move(self, players, width):
        s = self.speed
        while s > 0:
            self.pos = Vector(self.velocity_x / self.speed, self.velocity_y / self.speed) + self.pos
            for player in players:
                player.bounce_ball(self, width)
            s -= 1


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.speed = 4
        self.ball.center_x = self.width / 2
        self.ball.center_y = self.height / 2
        self.ball.velocity = Vector(self.ball.speed, 0).rotate(randint(-45, 45) + 180 * randint(0, 1))
        #self.ball.velocity = Vector(self.ball.speed, 0)

    def update(self, dt):
        players = [self.player1, self.player2]

        self.ball.move(players, self.width)

        if (self.ball.y < 0) or (self.ball.y > self.height - 50):
            self.ball.velocity_y *= -1

        if self.ball.x < 0:
            self.serve_ball()
            self.player2.score += 1

        if self.ball.x > self.width - 50:
            self.serve_ball()
            self.player1.score += 1

    def on_touch_move(self, touch):
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3/4:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


PongApp().run()