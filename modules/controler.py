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
        # lenght > 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        def revise(e):
            self.c.unbind("<Button-1>")
            self.c.bind("<Button-1>", press)

        def press(e):
            self.c.unbind("<Button-1>")
            play_sound("game/start")
            self.app.Musics.music = os.path.join(
                "game", random.choice(os.listdir("musics\\game")))
            self.c.delete("round")

            # start
            self.__configure_chip()
            self.__deal_card()

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

    def __deal_card(self):
        deck = self.Card.create_a_deck()
        # deal card
        self.Card.stack_deck(
            deck, (self.cs[0]/2, self.cs[1]/2), 200)
        self.c.update()
        time.sleep(3)

        for n in range(len(deck) + 1):
            # show
            stop()
            self.c.delete("deck-stack")
            play_sound("game/poker")
            self.Card.stack_deck(
                deck, (self.cs[0]/2, self.cs[1]/2), 200, n)
            self.c.update()

            if deck:
                # deal and get
                player.Player.id_to_player(n % 4).card.append(deck[0])
                del deck[0]
            self.__show_hand(n % 4)
            self.c.update()
            time.sleep(0.1)

        def enter(num):
            w = int((self.cs[0] - 400) / 5 / 4)
            if self.__select_card is None and self.c.coords(f"hand-0-{num}")[1] > self.cs[1] + w / 4 - 1:
                self.c.move(f"hand-0-{num}", 0, -w)

        def leave(num):
            w = int((self.cs[0] - 400) / 5 / 4)
            if self.__select_card is None and self.c.coords(f"hand-0-{num}")[1] < self.cs[1] + 1:
                self.c.move(f"hand-0-{num}", 0, w)

        def press(num):
            w = int((self.cs[0] - 400) / 5 / 4)
            if self.__select_card is None:
                if self.c.coords(f"hand-0-{num}")[1] > self.cs[1] + w / 4 - 1:
                    self.c.move(f"hand-0-{num}", 0, -w)
                self.__select_card = num

            else:
                if num == self.__select_card:
                    self.c.move(f"hand-0-{self.__select_card}", 0, w)
                    self.__select_card = None
                else:
                    self.c.move(f"hand-0-{self.__select_card}", 0, w)
                    self.c.move(f"hand-0-{num}", 0, -w)
                    self.__select_card = num

        def double_press(num):
            card = player.Player.id_to_player(0).card[num]
            suit, rank = card.data_to_num()
            #  judge !!!!!
            if not player.Player.id_to_player(0).play_card(card, []):
                play_sound("game/wrong")
            self.c.itemconfig(f"table-{suit}-{rank}", state="normal")
        for c in range(13):

            self.c.tag_bind(f"hand-0-{c}", "<Enter>",
                            lambda e, n=c: enter(n))
            self.c.tag_bind(f"hand-0-{c}", "<Leave>",
                            lambda e, n=c: leave(n))
            self.c.tag_bind(f"hand-0-{c}", "<Button-1>",
                            lambda e, n=c: press(n))
            self.c.tag_bind(f"hand-0-{c}", "<Double-Button-1>",
                            lambda e, n=c: double_press(n))
        self.__select_card = None
        self.__create_table()

    def __show_hand(self, id_):

        self.c.delete(f"hand-{id_}")
        corr = {
            0: int((self.cs[0] - 400) / 5),
            1: int((self.cs[1] - 400) / 5),
            2: int((self.cs[1] - 400) / 5),
            3: int((self.cs[1] - 400) / 5)
        }
        w = corr[id_]
        p = player.Player.id_to_player(id_)

        if id_ == 0:
            p.sort_card()
            for c in p.card:
                c.turn_over(True)
        middle_point = (w + w / 3 * len(p.card)) / 2
        for c in range(len(p.card)):
            corr2 = {
                0: ((self.cs[0]-140)/2 - middle_point + w / 2 + w / 3 * c, self.cs[1] + w / 4),
                1: (w / 4, (self.cs[1]-140)/2 - middle_point + w / 2 + w / 3 * c),
                2: ((self.cs[0]+140)/2 + middle_point - w / 2 - w / 3 * c, w / 4),
                3: (self.cs[0] - w / 4, (self.cs[1]+140)/2 + middle_point - w / 2 - w / 3 * c),
            }
            self.c.create_image(
                *corr2[id_], image=self.Card.card_obj_to_image(p.card[c], w, id_ % 2), tags=(f"hand-{id_}", f"hand-{id_}-{c}"))

    def __create_table(self):
        padding = 5
        w, h = self.cs
        x = (h-400)*9/40
        y = (h-400)*9/40
        x_length = w - (h-400)*9/40 - (h-400)*9/40
        y_length = h - (h-400)*9/40 - (w-400)*6/40
        real_h = int((y_length - 5 * padding) / 4)
        real_w = int(real_h*2/3)
        for s in range(1, 5):
            for r in range(1, 14):
                self.c.create_image(w/2 + (r-7)*real_w*3/4, y + padding + (padding+real_h)*(s-1),
                                    image=self.Card.card_name_to_image(s, r, real_w, True), anchor="n",
                                    state="hidden", tags=(f"table-{s}-{r}"))

    def new_round(self, round):
        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "background.png", "setup.mp3")
        self.__show_round(round)

    def initialize(self):
        # select all mode
        self.record_mode = self.app.mode  # int 0
        self.player_number = self.app.player_number  # int 1
        self.game_mode = self.app.game_mode  # tuple(15, 500)

        # create player
        player.Player.reset_player()
        for _ in range(self.player_number):
            player.Player("r", None, self.game_mode[1])
        for _ in range(self.player_number, 4):
            player.Com("r", None, self.game_mode[1])

        # start round
        self.round = 0
        self.new_round(self.round)

        # if (self.game_mode[0] != "∞") and (round > self.game_mode[0]):
