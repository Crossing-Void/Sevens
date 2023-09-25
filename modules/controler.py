"""
Main control of poker game
"""
from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.soundeffect import play_sound, stop
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
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
            # time.sleep(random.randint(1, 3))
            time.sleep(0.1)
            result = p.play(self.table)
            if result[0] == "play":
                p.play_a_card(result[1])
                self.table.append(result[1])
                self.Card.show_card_in_table(result[1])
            elif result[0] == "depose":
                p.depose_a_card(result[1])

            # self.Card.show_hand(
            #     player_number, sort=False)
            if player_number != 0:
                self.Card.show_hand(
                    player_number, sort=False)
            else:
                self.Card.show_hand(
                    player_number, sort=True, turn_over=True)
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
        color = {
            0: "red",
            1: "green",
            2: "blue",
            3: "gold",

        }
        interval = 10
        width = 100
        self.c.create_image(self.cs[0]/2, self.cs[1]/2, image=tk_image("result.png", int(self.cs[0]*3/4), int((5*interval+6*width)*25/23), dirpath="images\\game"),
                            tags=("result-base"))
        a, b = self.c.coords("result-base")
        a -= int(self.cs[0]*3/4) / 2
        b -= int((5*interval+6*width)*25/23) / 2

        border_w = int(self.cs[0]*3/4) / 262 * 5  # half
        border_h = (5*interval+6*width) / 23      # half
        self.Chip.change_chip_size(int(width*1.5/4))
        points = []
        for p in range(4):
            player = self.players[p]
            point = 0
            for c in range(len(player.depose)):
                player.depose[c].turn_over(True)
                print(border_h + b + interval + (interval+width*1.5) * p)
                self.c.create_image(border_w + a + interval + width*c, border_h + b + interval + (interval+width*1.5) * p,
                                    image=self.Card.card_obj_to_image(player.depose[c], width), anchor="nw"
                                    )
                point += player.depose[c].data_to_num()[1]
            if point:
                self.c.create_text(border_w + a + interval + width*(c+1), border_h + b + interval + (interval+width*1.5) * p + width*0.75,
                                   anchor="w", text=f"{point}", font=font_get(int(width*3/8)), fill="gold"
                                   )
            points.append(point)
            player.depose.clear()

        # judge winner
        min_p = min(points)
        info = []
        for _ in range(4):
            info.append(
                (_,
                 "win" if points[_] == min_p else "lose",
                 points[_])
            )
        win, lose = 0, 0
        bet = 0
        for _ in info:
            if _[1] == "win":
                win += 1
            else:
                lose += 1
                bet += _[2] if _[2] <= 50 else _[2] * 2
        for _ in range(4):
            if info[_][1] == "win":
                text = f"+ {int(bet/win)}$"
                self.players[_].money += int(bet/win)
            else:
                if info[_][2] > 50:
                    text = f"- {info[_][2]*2}$"
                    self.players[_].money -= info[_][2] * 2
                else:
                    text = f"- {info[_][2]}$"
                    self.players[_].money -= info[_][2]
            self.c.create_text(a + int(self.cs[0]*3/4) - interval - border_w, border_h + b + interval + (interval+width*1.5) * _,
                               anchor="ne", text=self.players[_].name, font=font_get(int(width*1.5*3/12)), fill=color[_]
                               )
            self.c.create_text(a + int(self.cs[0]*3/4) - interval - border_w, border_h + b + interval + (interval+width*1.5) * _ + int(width*1.5*3/12)*4/3,
                               anchor="ne", text=text, font=font_get(int(width*1.5*3/20)), fill="#ff6b87" if info[_][1] == "win" else "green",
                               )
            self.Chip.show_chips(info[_][2] if info[_][1] == "lose" else int(bet/win), (a + int(self.cs[0]*3/4) - interval - border_w,
                                                                                        border_h + b + interval + (interval+width*1.5) * _ + width*1.5))
        self.c.update()
        self.Chip.change_chip_size(50)
        time.sleep(7)
        self.round_now += 1
        self.Animation.round(self.round_now)
