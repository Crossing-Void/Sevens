"""
Chips management of poker game
"""
from Tkinter_template.Assets.image import tk_image
from dataclasses import dataclass

_chip_value = (200, 50, 10, 1)


@dataclass
class _chip:
    value: int

    def __post__init__(self):
        if self.value not in _chip_value:
            raise ValueError(f"The chip value not valid, got {self.value}")

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"

    def draw(self, size: tuple, decoration_string: str):
        return tk_image(f"{str(self)}-{decoration_string}.png", *size, dirpath="images\\game\\chips")


class Chip:
    chip_size = 50
    overlapping_width = int(chip_size / 25)
    corr = {
        "se": "bottom",
        "sw": "left",
        "nw": "upper",
        "ne": "right"
    }

    def __init__(self, main, controler) -> None:
        self.main = main
        self.controler = controler
        self.c = self.main.canvas
        self.cs = self.main.canvas_side

    def __money_to_number_of_chip(self, money: int):
        if money < 0:
            raise ValueError(f"The money should be larger than 0, but got: {money}")
        
        number_of_chip = []
        for value in _chip_value:
            num = money // value
            number_of_chip.append(num)
            money -= num * value
        return number_of_chip

    @classmethod
    def change_chip_size(cls, size: int):
        cls.chip_size = size
        cls.overlapping_width = int(cls.chip_size / 25)

    def show_chips(self, money: int, position: tuple, angle="se"):
        if angle not in ("se", "sw", "ne", "nw"):
            raise ValueError(f"The angle not valid, got {angle}")

        x, y = position  # right bottom
        number_of_chip = self.__money_to_number_of_chip(money)

        count = 0
        for value, number in zip(_chip_value, number_of_chip):
            for i in range(number):
                w, h = x, y
                # overlapping
                w -= self.overlapping_width * i * (1 if "e" in angle else -1)
                h -= self.overlapping_width * i * (1 if "s" in angle else -1)
                # move w
                if angle == "se":
                    w -= (self.chip_size * 1.2) * count
                if angle == "nw":
                    w += (self.chip_size * 1.2) * count
                # move y
                if angle == "sw":
                    h -= (self.chip_size * 1.2) * count
                if angle == "ne":
                    h += (self.chip_size * 1.2) * count

                self.c.create_image(w, h, image=_chip(value).draw((self.chip_size, self.chip_size), self.corr[angle]), anchor="se",
                                    tags=("chips"))
            count += 1

    def draw_single_chip(self, money: int, position: tuple, size: tuple, **kwargs):
        if money not in _chip_value:
            raise ValueError(f"{money} not supported")

        self.c.create_image(position[0], position[1], image=_chip(
            money).draw(size, "bottom"), **kwargs)

    def configure_chip(self):
        corr = {
            0: ((self.cs[0]-10, self.cs[1]-10), "se"),
            1: ((self.chip_size+10, self.cs[1]-10), "sw"),
            2: ((self.chip_size+10, self.chip_size+10), "nw"),
            3: ((self.cs[0]-10, self.chip_size+10), "ne"),
        }
        for i in range(4):
            self.show_chips(
                self.controler.players[i].money, corr[i][0], corr[i][1])
