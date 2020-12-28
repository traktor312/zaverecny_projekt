from random import randint
from kivy.vector import Vector

import tensorflow as tf
import numpy as np

# input player y, ball x, ball y, ball v_x, ball v_y, player id (max 35, 78, 43, 2.5, 2.5, (0, 1))
# ai_input = [game.player1.game_y, game.ball.game_x, game.ball.game_y, game.ball.velocity_x, game.ball.velocity_y]
# output nahoru, dolu, zustan

# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))


class AI:
    def __init__(self):
        self.model = self.create_model()
        self.train_data = self.create_data(200000)
        self.train_model(self.train_data)
        # self.test_data = self.create_data(1, 0)
        # self.predict_test_data(self.test_data)

    @staticmethod
    def create_inputs(number):
        data = []
        velocity_x = 0
        velocity_y = 0
        speeds = []
        s = 0.5
        while s < 2.5:
            speeds.append(s)
            s *= 1.1
        speeds.append(2.5)
        ball_velocity = [velocity_x, velocity_y]
        for j in range(number):
            ball_velocity = Vector(speeds[randint(0, len(speeds) - 1)], 0).rotate(randint(-80, 80) + 180 * randint(0, 1))
            data.append([randint(0, 35) / 35.0, randint(0, 78) / 78.0, randint(0, 43) / 43.0,
                         (ball_velocity[0] + 2.5) / 5.0, (ball_velocity[1] + 2.5) / 5.0, randint(0, 1)])
        return data

    @staticmethod
    def create_expected_outputs(inputs):
        data = []
        for i in inputs:
            if i[5] == 0:
                if i[3] > 0.5:
                    y = i[0] * 35 - 17.5
                    if abs(y) < 1:
                        data.append([0, 0, 1])
                    elif y < 0:
                        data.append([1, 0, 0])
                    else:
                        data.append([0, 1, 0])
                else:
                    time = i[1] * 78 / ((i[3] - 0.5) * 5) * -1
                    if (i[2] * 43 + (i[4] - 0.5) * 5 * time - (
                            i[2] * 43 + (i[4] - 0.5) * 5 * time) % 43) % 2 == 0:
                        y = (i[2] * 43 + (i[4] - 0.5) * 5 * time) % 43
                    else:
                        y = 43 - (i[2] * 43 + (i[4] - 0.5) * 5 * time) % 43
                    y = y - (i[0] * 35 + 5)
                    if abs(y) < 1:
                        data.append([0, 0, 1])
                    elif y > 0:
                        data.append([1, 0, 0])
                    else:
                        data.append([0, 1, 0])
            else:
                if i[3] < 0.5:
                    y = i[0] * 35 - 17.5
                    if abs(y) < 1:
                        data.append([0, 0, 1])
                    elif y < 0:
                        data.append([1, 0, 0])
                    else:
                        data.append([0, 1, 0])
                else:
                    time = (78 - i[1] * 78) / ((i[3] - 0.5) * 5)
                    if (i[2] * 43 + (i[4] - 0.5) * 5 * time - (
                            i[2] * 43 + (i[4] - 0.5) * 5 * time) % 43) % 2 == 0:
                        y = (i[2] * 43 + (i[4] - 0.5) * 5 * time) % 43
                    else:
                        y = 43 - (i[2] * 43 + (i[4] - 0.5) * 5 * time) % 43
                    y = y - (i[0] * 35 + 5)
                    if abs(y) < 1:
                        data.append([0, 0, 1])
                    elif y > 0:
                        data.append([1, 0, 0])
                    else:
                        data.append([0, 1, 0])
        return data

    def create_data(self, number):
        inputs = self.create_inputs(number)
        outputs = self.create_expected_outputs(inputs)

        inputs = np.array(inputs).reshape(number, 6)
        outputs = np.array(outputs).reshape(number, 3)
        return [inputs, outputs]

    @staticmethod
    def validate_data(data):
        data = [data[0] / 35, data[1] / 78, data[2] / 43, (data[3] + 2.5) / 5, (data[4] + 2.5) / 5, data[5] / 78]
        data = np.array(data).reshape(1, 6)
        return data

    @staticmethod
    def create_model():
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(3, activation=tf.nn.softmax))

        model.compile(optimizer='adam',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
        return model

    def train_model(self, data):
        self.model.fit(data[0], data[1], epochs=10, batch_size=32, shuffle=True)

    def predict_test_data(self, data):
        predictions = self.model.predict([data[0]])
        print(np.argmax(predictions[0]))
        print(predictions[0])
        print(data[1])
        return np.argmax(predictions[0])

    def predict(self, data):
        prediction = self.model(data)
        return np.argmax(prediction[0])
