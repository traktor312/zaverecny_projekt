from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty

import sys, os
import tkinter as tk
from tkinter import filedialog
from keras.models import load_model

from game import PongGame
from ai2 import AI2


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
        self.manager.playing[player] = 1 if self.manager.playing[player] == 0 else 0
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
        self.manager.models[player] = AI2(file_path)
        try:
            self.manager.models[player].agent.q_eval = load_model(file_path)
        except:
            pass
        self.update_text()

    def export_network(self, player):
        self.set_ai()
        root = tk.Tk()
        root.withdraw()

        pathname = os.path.abspath(os.path.dirname(sys.argv[0]))+"/networks/player" + str(player)
        if not os.path.exists(pathname):
            os.makedirs(pathname)

        file_path = filedialog.asksaveasfilename(initialdir = pathname, title = "Save neural network",
                                                 defaultextension=".h5", filetypes=self.NETWORK_TYPES)

        model = AI2(file_path)
        try:
            model.agent.save_model()
        except:
            pass


class CanvasScreen(Screen):
    def start_game(self):
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
