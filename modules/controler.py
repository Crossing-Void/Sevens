"""
Main control of poker game
"""
from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.image import tk_image
from modules.game import *
import time


class Control:
    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

        self.players = []

        self.Chip = chips.Chip(app)
        self.Card = card.Card(app)

    def initialize(self):
        # select all mode
        self.record_mode = self.app.mode
        self.player_number = self.app.player_number
        self.game_mode = self.app.game_mode  # tuple("bankrupt", 500)

        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "background.png", "setup.mp3")
        # selfself.Card.create_a_deck()
        # # create_player
        # for i in range(self.player_number):
        #     self.players.append(player.Person())
        # for i in range(self.player_number, 4):
        #     self.players.append(player.Com())
