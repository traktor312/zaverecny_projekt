from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty

import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

import sys, os
import tkinter as tk
from tkinter import filedialog
from keras.models import load_model

from game import PongGame
from ai import AI


Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '360')
Config.write()
Window.size = (640, 360)


class MenuScreen(Screen):
    pass


class SettingsScreen(Screen):
    NETWORK_TYPES = [("Hierarchical Data Format (*.h5)", "*.h5")]
    text0 = ObjectProperty(None)
    text1 = ObjectProperty(None)

    def set_ai(self):
        try:
            self.manager.models
        except:
            self.manager.models = [None, None]
            self.manager.playing = [0, 0]

    def update_text(self):
        self.set_ai()
        self.text0.text = "Player" if self.manager.playing[0] == 0 else "DQN" + ("" if self.manager.models[0] is None else
                                                                         " " + self.manager.models[0].fname)
        self.text1.text = "Player" if self.manager.playing[1] == 0 else "DQN" + ("" if self.manager.models[1] is None else
                                                                         " " + self.manager.models[1].fname)

    def playing_btn(self, player):
        self.set_ai()
        self.manager.playing[player] = 1 if self.manager.playing[player] == 0 \
                                            and self.manager.models[player] is not None else 0
        self.update_text()

    def import_network(self, player):
        self.set_ai()
        root = tk.Tk()
        root.withdraw()

        pathname = os.path.abspath(os.path.dirname(sys.argv[0])) + "/networks/player" + str(player)
        if not os.path.exists(pathname):
            os.makedirs(pathname)

        file_path = filedialog.askopenfilename(initialdir=pathname, title="Load neural network", defaultextension=".h5",
                                               filetypes=self.NETWORK_TYPES)
        self.manager.models[player] = AI(file_path)
        try:
            self.manager.models[player].agent.q_eval = load_model(file_path)
            self.manager.playing[player] = 1
            self.update_text()
        except:
            pass

    def export_network(self, player):
        self.set_ai()
        root = tk.Tk()
        root.withdraw()

        pathname = os.path.abspath(os.path.dirname(sys.argv[0]))+"/networks/player" + str(player)
        if not os.path.exists(pathname):
            os.makedirs(pathname)

        file_path = filedialog.asksaveasfilename(initialdir = pathname, title = "Save neural network",
                                                 defaultextension=".h5", filetypes=self.NETWORK_TYPES)

        model = AI(file_path)
        try:
            model.agent.save_model()
            self.manager.models[player] = model
            self.manager.playing[player] = 1
            self.update_text()
        except:
            pass


class CanvasScreen(Screen):
    def start_game(self):
        try:
            self.game = PongGame(self.manager.models, self.manager.playing)
        except:
            self.manager.models = [None, None]
            self.manager.playing = [0, 0]
            self.game = PongGame(self.manager.models, self.manager.playing)

        self.add_widget(self.game)
        self.game.start()



class PongApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(CanvasScreen(name='canvas'))

        return sm


PongApp().run()
