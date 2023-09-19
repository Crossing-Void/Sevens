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

    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

    def __money_to_number_of_chip(self, money: int):
        number_of_chip = []
        for value in _chip_value:
            num = money // value
            number_of_chip.append(num)
            money -= num * value
        return number_of_chip

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

                self.c.create_image(w, h, image=_chip(value).draw((self.chip_size, self.chip_size), self.corr[angle]), anchor="se"
                                    )
            count += 1
