from Tkinter_template.Assets.soundeffect import play_sound
import random
import re

class _player:
    def __init__(self, controler, name: str, image: str, money: int, id_: int) -> None:
        self.controler = controler
        self.name = name
        self.image = image
        self.money = money
        self.id = id_

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
    def __init__(self, controler, name: str, image: str, money: int, id_: int) -> None:
        super().__init__(controler, name, image, money, id_)

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
    def __init__(self, controler, name: str, image: str, money: int, id_: int) -> None:
        super().__init__(controler, name, image, money, id_)

    def __repr__(self) -> str:
        return f"Player object id: {self.id}"

    def __str__(self) -> str:
        return f"Player object id: {self.id}"

    def play(self, table):
        # <<<<<<<<<<<<<<<<<< change args to id
        def unbind():
            for c in range(len(self.card)):
                can.tag_unbind(f"hand-0-{c}", "<Enter>")
                can.tag_unbind(f"hand-0-{c}", "<Leave>")
                can.tag_unbind(f"hand-0-{c}", "<Button-1>")
                can.tag_unbind(f"hand-0-{c}", "<Double-Button-1>")
        
        def decide_card(num):
            card = self.card[num]

            if mode == "play":
                if not self.judge_card_valid(card, table):
                    play_sound("game/invalid")
                    return 
                
            unbind()
            if mode == "play":
                self.play_a_card(card)
                self.controler.table.append(card)
                self.controler.card.show_card_in_table(card)
            elif mode == "depose":
                  self.depose_a_card(card)
                  
            self.controler.card.show_hand(self.id, sort=True, turn_over=True)
            can.update()
            self.controler.turn = self.controler.calculate_turn(self.controler.turn)
            self.controler.play(self.controler.turn)
               
        def enter(num):
            if select_card:
                return
            if can.coords(f"hand-0-{num}")[1] > cs[1] + w / 4 - 1:
                can.move(f"hand-0-{num}", 0, -w/8)
                
        def leave(num):
            if select_card:
                return
            if can.coords(f"hand-0-{num}")[1] < cs[1] + w / 8 + 1:
                can.move(f"hand-0-{num}", 0, w/8)
                
           
        
        def press(num):
            nonlocal select_card
            if select_card is None:
                if can.coords(f"hand-0-{num}")[1] > cs[1] + w / 4 - 1:
                    can.move(f"hand-0-{num}", 0, -w/8)
                select_card = num

            else:
                if num == select_card:
                    decide_card(num)
                else:
                    can.move(f"hand-0-{select_card}", 0, w/8)
                    can.move(f"hand-0-{num}", 0, -w/8)
                    select_card = num
        
        def double_press(num):
            decide_card(num)
            
        
        can = self.controler.c
        cs = self.controler.cs
        w = int((cs[0] - 400) / 5)
        valid = list(filter(lambda c: self.judge_card_valid(c, table), self.card))
        mode = "play" if valid else "depose"
        select_card = None
        
        for c in range(len(self.card)):
            can.tag_bind(f"hand-0-{c}", "<Enter>",
                            lambda e, n=c: enter(n))
            can.tag_bind(f"hand-0-{c}", "<Leave>",
                            lambda e, n=c: leave(n))
            can.tag_bind(f"hand-0-{c}", "<Button-1>",
                            lambda e, n=c: press(n))
            can.tag_bind(f"hand-0-{c}", "<Double-Button-1>",
                            lambda e, n=c: double_press(n))

        # config first enter
     
        x = self.controler.app.root.winfo_pointerx() - self.controler.app.root.winfo_rootx()
        y = self.controler.app.root.winfo_pointery() - self.controler.app.root.winfo_rooty()
        objs = can.find_overlapping(x, y, x+1, y+1)
        max_number = -1
        if len(objs) > 1:
            for obj in objs[1:]:
                tags = can.gettags(obj)
                for tag in tags:
                    m = re.search("^hand-\d-(\d)$", tag)
                    if m:
                        if int(m.group(1)) > max_number:
                            max_number = int(m.group(1))
            if max_number != -1:
                enter(max_number)
                        

            
                    
        

        

        

        