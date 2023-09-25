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
        self.table = []
        self.round_now = 0

    def initialize(self):
        # select all mode
        self.record_mode = self.app.mode  # int 0
        self.player_number = self.app.player_number  # int 1
        self.game_mode = self.app.game_mode  # tuple(15, 500)

        # create player
        self.players.clear()
        for _ in range(self.player_number):
            self.players.append(
                player.Player("r", None, self.game_mode[1])
            )
        for _ in range(self.player_number, 4):
            self.players.append(
                player.Com("r", None, self.game_mode[1])
            )

        # start round
        self.round_now = 0
        self.round_now += 1
        self.Animation.round(self.round_now)

        # if (self.game_mode[0] != "∞") and (round > self.game_mode[0]):

    def turn(self, player_number):
        print(player_number)
        for p in self.players:
            if p.card:
                break

        else:
            # end
            self.end()
        p = self.players[player_number]
        if p.__class__ == player.Com:
            time.sleep(random.randint(1, 3))
            result = p.play(self.table)
            if result[0] == "play":
                p.play_a_card(result[1])
                self.table.append(result[1])
                self.Card.show_card_in_table(result[1])
            elif result[0] == "depose":
                p.depose_a_card(result[1])

            self.Card.show_hand(
                player_number, sort=False)
            self.c.update()

            if self.player_now == 3:
                self.player_now = 0
            else:
                self.player_now += 1
            self.turn(self.player_now)
        elif p.__class__ == player.Player:
            p.play(self)

    def game(self):
        # animation enter here
        self.table = []
        for player in self.players:
            for card in player.card:
                if str(card) == "Seven of Spades":
                    self.player_now = self.players.index(player)

        self.turn(self.player_now)

    def end(self):
        for p in self.players:
            print(p.depose)
        self.round_now += 1
        self.Animation.round(self.round_now)
