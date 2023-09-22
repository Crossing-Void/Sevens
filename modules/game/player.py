class _player:
    id_ = 0
    players = []

    def __init__(self, name: str, image: str, money: int) -> None:

        self.id = _player.id_
        self.money = money
        self.name = name
        self.image = image
        self.card = []
        self.depose = []

        _player.id_ += 1
        _player.players.append(self)

    @ classmethod
    def id_to_player(cls, id_: int):
        for obj in _player.players:
            if obj.id == id_:
                return obj

    @ classmethod
    def reset_player(cls):
        _player.id_ = 0
        _player.players = []

    def sort_card(self):
        self.card.sort(key=lambda card: card.data_to_num())


class Com(_player):
    def __init__(self, name: str, image: str, money: int) -> None:
        super().__init__(name, image, money)

    def __repr__(self) -> str:
        return f"Com object id: {self.id}"

    def __str__(self) -> str:
        return f"Com object id: {self.id}"


class Player(_player):
    def __init__(self, name: str, image: str, money: int) -> None:
        super().__init__(name, image, money)

    def __repr__(self) -> str:
        return f"Player object id: {self.id}"

    def __str__(self) -> str:
        return f"Player object id: {self.id}"
