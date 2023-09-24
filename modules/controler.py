"""
Main control of poker game
"""
from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.soundeffect import play_sound, stop
from Tkinter_template.Assets.image import tk_image
from modules.game import *
import random
import time
import os


class Control:
    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

        self.Chip = chips.Chip(app, self)
        self.Card = card.Card(app, self)
        self.Animation = animation.Animation(app, self)

        self.record_mode = None
        self.player_number = None
        self.game_mode = None

        self.players = []
        self.round_now = 0

    def initialize(self):
        # select all mode
        self.record_mode = self.app.mode  # int 0
        self.player_number = self.app.player_number  # int 1
        self.game_mode = self.app.game_mode  # tuple(15, 500)

        # create player
        self.players.clear()
        # for _ in range(self.player_number):
        #     self.players.append(
        #         player.Player("r", None, self.game_mode[1])
        #     )
        # for _ in range(self.player_number, 4):
        #     self.players.append(
        #         player.Com("r", None, self.game_mode[1])
        #     )
        for _ in range(4):
            self.players.append(
                player.Com("r", None, self.game_mode[1])
            )
        # start round
        self.round_now = 0
        self.round_now += 1
        self.Animation.round(self.round_now)

        # if (self.game_mode[0] != "∞") and (round > self.game_mode[0]):

    def temp(self, num):
        self.turn_ = num
        self.c.delete("d")
        self.c.create_text(
            400, 600, text=f"{self.turn_}", tag=("d"))

    def turn(self, num):
        self.temp(num)
        self.c.update()
        p = self.players[num]
        result = p.play(self.table)
        print(result)
        if result[0] == "play":
            p.play_a_card(result[1])
            self.table.append(result[1])
            self.Card.show_card_in_table(result[1])
        elif result[0] == "depose":
            p.depose_a_card(result[1])
        self.Card.show_hand(
            num, sort=False, turn_over=False if num != 0 else True)
        self.c.update()
        time.sleep(1)

        if num == 3:
            self.turn_ = 0
        else:
            self.turn_ += 1
        self.turn(self.turn_)

    def game(self):
        self.table = []
        for player in self.players:
            for card in player.card:
                if str(card) == "Seven of Spades":
                    self.temp(self.players.index(player))
        self.turn(self.turn_)
