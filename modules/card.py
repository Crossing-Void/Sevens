"""
Cards management of poker game
"""
from Tkinter_template.Assets.image import tk_image
from dataclasses import dataclass
from enum import Enum, unique


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

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Card:
    def __init__(self, app) -> None:
        self.app = app

    def card_name_new_obj(self, suit: int, rank: int):
        card = _card(_suit(suit).name,
                     _rank(rank).name
                     )
        return card

    def card_name_to_image(self, suit: int, rank: int, size: tuple):
        card = _card(_suit(suit).name,
                     _rank(rank).name
                     )
        return tk_image(str(card) + ".png", *size, dirpath="images\\cards")

    def card_obj_to_image(self, object: _card, size: tuple):
        return tk_image(str(object) + ".png", *size, dirpath="images\\cards")
