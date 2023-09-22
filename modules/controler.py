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

        self.Chip = chips.Chip(app)
        self.Card = card.Card(app)

    def __show_round(self, round):
        def revise(e):
            self.c.unbind("<Button-1>")
            self.c.bind("<Button-1>", press)

        def press(e):
            self.c.unbind("<Button-1>")
            play_sound("game/start")
            self.app.Musics.music = random.choice(
                [music for music in os.listdir("musics") if music.startswith("game")])
            self.c.delete("round")

            # start
            self.start()

        # image
        width_round = tk_image("round.png", height=200,
                               dirpath="images\\game\\round", get_object_only=True).width
        width_number = tk_image(f"{round}.png", height=200,
                                dirpath="images\\game\\round", get_object_only=True).width
        middle_point = (width_round + width_number + 50) / 2
        self.c.create_image(
            self.cs[0]/2 - middle_point + width_round / 2, self.cs[1]/2, image=tk_image("round.png", height=200, dirpath="images\\game\\round"),
            tags=("round"))
        self.c.create_image(
            self.cs[0]/2 - middle_point + width_round + 50, self.cs[1]/2, image=tk_image(f"{round}.png", height=200, dirpath="images\\game\\round"), anchor='w',
            tags=("round"))

        # music
        self.c.bind("<Button-1>", revise)

    def __show_all_hand(self):
        corr = {
            0: 200,
            1: int((self.cs[1] - 250)/6),
            2: 100,
            3: int((self.cs[1] - 250)/6)
        }

        for i in range(4):
            w = corr[i]
            p = player.Player.id_to_player(i)

            if i == 0:
                p.sort_card()
                for c in p.card:
                    c.turn_over(True)
            middle_point = (w + w / 3 * len(p.card)) / 2
            for c in range(len(p.card)):
                corr2 = {
                    0: (self.cs[0]/2 - middle_point + w / 2 + w / 3 * c, self.cs[1]),
                    1: (w / 8, self.cs[1]/2 - middle_point + w / 2 + w / 3 * c),
                    2: (self.cs[0]/2 + middle_point - w / 2 - w / 3 * c, w / 8),
                    3: (self.cs[0] - w / 8, self.cs[1]/2 + middle_point - w / 2 - w / 3 * c),
                }
                self.c.create_image(
                    *corr2[i], image=self.Card.card_obj_to_image(p.card[c], w, i % 2), tags=(f"hand-{i}"))

    def __deal_card(self):
        self.deck = self.Card.create_a_deck()
        # deal card
        self.Card.stack_deck(
            self.deck, (self.cs[0]/2, self.cs[1]/2), 200)
        self.c.update()
        time.sleep(3)

        for n in range(len(self.deck) + 1):
            # show
            stop()
            self.c.delete("deck-stack")
            self.c.delete(f"hand-{n % 4}")
            play_sound("game/poker")
            self.Card.stack_deck(
                self.deck, (self.cs[0]/2, self.cs[1]/2), 200, n)
            self.c.update()

            if self.deck:
                # deal and get
                player.Player.id_to_player(n % 4).card.append(self.deck[0])
                del self.deck[0]
            self.__show_all_hand()
            self.c.update()
            time.sleep(0.1)

    def __configure_chip(self):
        corr = {
            0: ((self.cs[0]-10, self.cs[1]-10), "se"),
            1: ((self.Chip.chip_size+10, self.cs[1]-10), "sw"),
            2: ((self.Chip.chip_size+10, self.Chip.chip_size+10), "nw"),
            3: ((self.cs[0]-10, self.Chip.chip_size+10), "ne"),
        }
        for i in range(4):
            self.Chip.show_chips(player.Player.id_to_player(
                i).money, corr[i][0], corr[i][1])

    def initialize(self):
        # select all mode
        self.record_mode = self.app.mode  # int 0
        self.player_number = self.app.player_number  # int 1
        self.game_mode = self.app.game_mode  # tuple("bankrupt", 500)
        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "background.png", "setup.mp3")

        # create player
        player.Player.reset_player()
        for _ in range(self.player_number):
            player.Player("r", None, self.game_mode[1])
        for _ in range(self.player_number, 4):
            player.Com("r", None, self.game_mode[1])

        # start round
        self.__show_round(1)

    def start(self):
        self.__configure_chip()
        self.__deal_card()
