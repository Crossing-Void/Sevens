import random


class _player:
    def __init__(self, name: str, image: str, money: int) -> None:
        self.name = name
        self.image = image
        self.money = money

        self.card = []
        self.depose = []

    def sort_card(self):
        self.card.sort(key=lambda card: card.data_to_num())

    def judge_card_valid(self, card, table):
        suit, rank = card.data_to_num()
        if rank == 7:
            return True
        else:
            numbers = [c.data_to_num()[1]
                       for c in table if c.suit == card.suit]
            if not numbers:
                return False
            if rank in (max(numbers)+1, min(numbers)-1):
                return True
            return False

    def play_a_card(self, card):
        self.card.remove(card)

    def depose_a_card(self, card):
        self.card.remove(card)
        self.depose.append(card)


class Com(_player):
    def __init__(self, name: str, image: str, money: int) -> None:
        super().__init__(name, image, money)

    def __repr__(self) -> str:
        return f"Com object id: {self.id}"

    def __str__(self) -> str:
        return f"Com object id: {self.id}"

    def __random_play(self, table):
        valid = list(
            filter(lambda c: self.judge_card_valid(c, table), self.card))
        if valid:
            return ("play", random.choice(valid))
        else:
            # depose
            return ("depose", random.choice(self.card))

    def play(self, table):
        return self.__random_play(table)


class Player(_player):
    def __init__(self, name: str, image: str, money: int) -> None:
        super().__init__(name, image, money)

    def __repr__(self) -> str:
        return f"Player object id: {self.id}"

    def __str__(self) -> str:
        return f"Player object id: {self.id}"

    # def play(self, controler):
    #     controler.Card.player_bind(controler.players.index(self))
