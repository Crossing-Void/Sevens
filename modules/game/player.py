class _player:
    def __init__(self, name: str, image: str, money: int) -> None:
        self.money = money
        self.name = name
        self.image = image
        self.card = []
        self.depose = []


class Com(_player):
    def __init__(self, name: str, image: str, money: int) -> None:
        super().__init__(name, image, money)


class Person(_player):
    def __init__(self, name: str, image: str, money: int) -> None:
        super().__init__(name, image, money)
