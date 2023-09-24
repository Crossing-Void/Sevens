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

    def play_card(self, obj, table):
        suit, rank = obj.data_to_num()
        if rank == 7:
            self.card.remove(obj)
            return True
        else:
            numbers = [card.data_to_num()[1]
                       for card in table if card.suit == obj.suit]
            if not numbers:
                return False
            if rank in (max(numbers)+1, min(numbers)-1):
                self.card.remove(obj)
                return True
            return False


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
