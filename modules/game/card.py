"""
Cards management of poker game
"""
from Tkinter_template.Assets.soundeffect import play_sound, stop
from Tkinter_template.Assets.image import tk_image
from dataclasses import dataclass
from enum import Enum, unique
import random
import time


@unique
class _rank(Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


@unique
class _suit(Enum):
    Clubs = 1
    Diamonds = 2
    Hearts = 3
    Spades = 4


@dataclass
class _card:
    suit: str
    rank: str
    front: bool

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def turn_over(self, state: bool = None):
        if state is None:
            self.front = not self.front
        else:
            self.front = state

    def data_to_num(self):
        return (eval(f"_suit.{self.suit}.value"),
                eval(f"_rank.{self.rank}.value"))


class Card:
    def __init__(self, app, app2=None) -> None:
        self.app = app
        self.controler = app2
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

    def card_name_new_obj(self, suit: int, rank: int, front=False):
        card = _card(_suit(suit).name,
                     _rank(rank).name,
                     front)
        return card

    def card_name_to_image(self, suit: int, rank: int, width, front=False):
        card = _card(_suit(suit).name,
                     _rank(rank).name,
                     front)
        return tk_image(str(card) + ".png", width, dirpath="images\\cards")

    def card_obj_to_image(self, object: _card, width, rotate90=False):
        if object.front:
            return tk_image(str(object) + ".png", width, dirpath="images\\cards")
        else:
            if rotate90:
                return tk_image("back2.png", height=width, dirpath="images\\cards")
            else:
                return tk_image("back.png", width, dirpath="images\\cards")

    def create_a_deck(self, shuffle=True):
        cards = [(suit, rank) for suit in range(1, 5) for rank in range(1, 14)]
        if shuffle:
            random.shuffle(cards)
        return [_card(_suit(suit).name, _rank(rank).name, False) for suit, rank in cards]

    # advanced method
    def stack_deck(self, deck: list[_card], position: tuple, width, displacement=0):
        overlapping_width = width / 200
        for n in range(len(deck)-1, -1, -1):
            self.c.create_image(position[0]+(n + displacement) * overlapping_width,
                                position[1]+(n + displacement) *
                                overlapping_width,
                                image=self.card_obj_to_image(deck[n], width),
                                tags=('deck-stack'))

    def deal_card(self):
        deck = self.create_a_deck()
        self.stack_deck(
            deck, (self.cs[0]/2, self.cs[1]/2), 200)
        self.c.update()
        time.sleep(3)

        for n in range(len(deck) + 1):
            # show
            stop()
            self.c.delete("deck-stack")
            play_sound("game/poker")
            self.stack_deck(
                deck, (self.cs[0]/2, self.cs[1]/2), 200, n)
            self.c.update()

            if deck:
                # deal and get
                self.controler.players[n % 4].card.append(deck[0])
                del deck[0]
            self.show_hand(n % 4, turn_over=True if n % 4 == 0 else False)
            self.c.update()
            time.sleep(0.1)

        time.sleep(2)
        self.show_hand(0, turn_over=False)
        self.c.update()
        time.sleep(1)
        self.show_hand(0, sort=True, turn_over=True)
        self.c.update()

        # def enter(num):
        #     w = int((self.cs[0] - 400) / 5 / 4)
        #     if self.__select_card is None and self.c.coords(f"hand-0-{num}")[1] > self.cs[1] + w / 4 - 1:
        #         self.c.move(f"hand-0-{num}", 0, -w)

        # def leave(num):
        #     w = int((self.cs[0] - 400) / 5 / 4)
        #     if self.__select_card is None and self.c.coords(f"hand-0-{num}")[1] < self.cs[1] + 1:
        #         self.c.move(f"hand-0-{num}", 0, w)

        # def press(num):
        #     w = int((self.cs[0] - 400) / 5 / 4)
        #     if self.__select_card is None:
        #         if self.c.coords(f"hand-0-{num}")[1] > self.cs[1] + w / 4 - 1:
        #             self.c.move(f"hand-0-{num}", 0, -w)
        #         self.__select_card = num

        #     else:
        #         if num == self.__select_card:
        #             self.c.move(f"hand-0-{self.__select_card}", 0, w)
        #             self.__select_card = None
        #         else:
        #             self.c.move(f"hand-0-{self.__select_card}", 0, w)
        #             self.c.move(f"hand-0-{num}", 0, -w)
        #             self.__select_card = num

        # def double_press(num):
        #     card = player.Player.numto_player(0).card[num]
        #     suit, rank = card.data_to_num()
        #     #  judge !!!!!
        #     if not player.Player.numto_player(0).play_card(card, []):
        #         play_sound("game/wrong")
        #     self.c.itemconfig(f"table-{suit}-{rank}", state="normal")
        # for c in range(13):

        #     self.c.tag_bind(f"hand-0-{c}", "<Enter>",
        #                     lambda e, n=c: enter(n))
        #     self.c.tag_bind(f"hand-0-{c}", "<Leave>",
        #                     lambda e, n=c: leave(n))
        #     self.c.tag_bind(f"hand-0-{c}", "<Button-1>",
        #                     lambda e, n=c: press(n))
        #     self.c.tag_bind(f"hand-0-{c}", "<Double-Button-1>",
        #                     lambda e, n=c: double_press(n))
        # self.__select_card = None
        # self.__create_table()

    def show_hand(self, num, sort=False, turn_over=False):
        self.c.delete(f"hand-{num}")
        corr = {
            0: int((self.cs[0] - 400) / 5),
            1: int((self.cs[1] - 400) / 5),
            2: int((self.cs[1] - 400) / 5),
            3: int((self.cs[1] - 400) / 5)
        }
        w = corr[num]
        p = self.controler.players[num]

        if sort:
            p.sort_card()

        for c in p.card:
            c.turn_over(turn_over)
        middle_point = (w + w / 3 * len(p.card)) / 2
        for c in range(len(p.card)):
            corr2 = {
                0: ((self.cs[0]-140)/2 - middle_point + w / 2 + w / 3 * c, self.cs[1] + w / 4),
                1: (w / 4, (self.cs[1]-140)/2 - middle_point + w / 2 + w / 3 * c),
                2: ((self.cs[0]+140)/2 + middle_point - w / 2 - w / 3 * c, w / 4),
                3: (self.cs[0] - w / 4, (self.cs[1]+140)/2 + middle_point - w / 2 - w / 3 * c),
            }
            self.c.create_image(
                *corr2[num], image=self.card_obj_to_image(p.card[c], w, num % 2), tags=(f"hand-{num}", f"hand-{num}-{c}"))

    def create_table(self):
        padding = 5
        w, h = self.cs
        y = (h-400)*9/40
        y_length = h - (h-400)*9/40 - (w-400)*6/40
        real_h = int((y_length - 5 * padding) / 4)
        real_w = int(real_h*2/3)

        for s in range(1, 5):
            for r in range(1, 14):
                self.c.create_image(w/2 + (r-7)*real_w*3/4, y + padding + (padding+real_h)*(s-1),
                                    image=self.Card.card_name_to_image(s, r, real_w, True), anchor="n",
                                    state="hidden", tags=(f"table-{s}-{r}"))
