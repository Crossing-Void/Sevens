from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.soundeffect import play_sound, stop
from Tkinter_template.Assets.music import Music
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
from modules.game import *

import random
import time
import os
from modules.effect import *


class Control:
    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side
        # music player
        self.music_player = Music()

        # initialize effect
        self.home = home.Effect(self.app, self, 2)
        self.select_record = select_record.Effect(self.app, self)
        self.select_player_number = select_player_number.Effect(self.app, self)
        self.select_game_mode = select_game_mode.Effect(self.app, self)

        # game object
        self.chip = chip.Chip(self.app, self)
        self.card = card.Card(self.app, self)
        
    @staticmethod
    def calculate_turn(num: int):
        return num + 1 if num <= 2 else 0
        
        

        
       
    
    def initialize(self):
        # user arguments
        self.user_select_record = None  # "new" or "record"
        self.user_select_player_number = None  # int
        self.user_select_game_mode = None  # nametuple(round, money)

        # --------------- for game ---------------
        self.round_count = 1
        self.players = []
        

    def effect_enter(self, option: str):
        if option not in ("home", "select_game_mode",
                          "select_player_number", "select_record"):
            raise ValueError(f"Effect {option} is not exists")

        exec(f"self.{option}.start()")

    def effect_loop(self, option: str):
        if option not in ("home", "select_game_mode",
                          "select_player_number", "select_record"):
            raise ValueError(f"Effect {option} is not exists")

        exec(f"self.{option}.loop()")

    # --------------------------- for game ---------------------------
    def round(self, round: int):
        def revise(e):
            self.c.unbind("<Button-1>")
            self.c.bind("<Button-1>", press)
            
        def press(e):
            self.c.tag_unbind("cover", "<Button-1>")
            play_sound("game/start_a_game")
            self.c.delete("round")
            self.c.update()
            time.sleep(0.5)
            self.music_player.music = os.path.join(
                "game\\game_duration", random.choice(os.listdir("musics\\game\\game_duration")))
            time.sleep(1)
            
            


            # enter a game
            if round == 1:
                # create player
                for i in range(4):
                    info = (self, "r", None, self.user_select_game_mode.money, i)
                    if i < self.user_select_player_number:
                        self.players.append(player.Player(*info))
                    else:
                        self.players.append(player.Com(*info))
                    
            self.game()
            
            

        
        img_path = "images\\game\\round"
        canvas_reduction(self.c, self.cs, self.music_player,
                         "game.png", "game\\ready_for_game.mp3")
        # image
        width_round = tk_image("round.png", height=200,
                               dirpath=img_path, get_object_only=True).width
        middle_point = width_round
        for number in str(round):
            middle_point += tk_image(f"{number}.png", height=200,
                                     dirpath=img_path, get_object_only=True).width
            middle_point += 20
        middle_point = (middle_point + 50) / 2

        self.c.create_image(
            self.cs[0]/2 - middle_point + width_round / 2, self.cs[1]/2, image=tk_image("round.png", height=200, dirpath="images\\game\\round"),
            tags=("round"))
        revise_term = 0
        for number in str(round):
            self.c.create_image(
                self.cs[0]/2 - middle_point + width_round + 50 + revise_term, self.cs[1]/2, image=tk_image(f"{number}.png", height=200, dirpath="images\\game\\round"), anchor='w',
                tags=("round"))
            revise_term += tk_image(f"{number}.png", height=200,
                                    dirpath=img_path, get_object_only=True).width + 20

        self.c.tag_bind("cover", "<Button-1>", press)

    
    def game(self):
        self.table = []
        self.turn = 0
        self.chip.configure_chip()
        self.card.deal_card()
        self.card.create_table()

        # decide who is the first
        for player in self.players:
            if "Seven of Spades" in [str(card) for card in player.card]:
                self.turn = self.players.index(player)
        
        self.play(self.turn)
       
    def play(self, turn_number: int):
        for p in self.players:
            if p.card:
                break
        else:
            # end
            self.end()
            return 
            
        p = self.players[turn_number]

        if p.__class__ == player.Com:
            time.sleep(random.randint(1, 2))
            result = p.play(self.table)
            if result[0] == "play":
                p.play_a_card(result[1])
                self.table.append(result[1])
                self.card.show_card_in_table(result[1])
            elif result[0] == "depose":
                p.depose_a_card(result[1])
            print(p.id, result)
            # need to be revised
            self.card.show_hand(
                turn_number, sort=False, turn_over=False)
            
            
            self.c.update()
            self.turn = self.calculate_turn(turn_number)
            self.play(self.turn)
        

        elif p.__class__ == player.Player:
            p.play(self.table)

        


   









   

    

    

    def end(self):
        color = {
            0: "red",
            1: "green",
            2: "blue",
            3: "gold",
        }
        img_path = "images\\game\\result"
        interval = 10
        width = 100
        self.c.create_image(self.cs[0]/2, self.cs[1]/2, image=tk_image("frame.png", int(self.cs[0]*3/4), int((5*interval+6*width)*25/23), dirpath=img_path),
                            tags=("result", "result-frame"))
        a, b = self.c.coords("result-frame")
        a -= int(self.cs[0]*3/4) / 2
        b -= int((5*interval+6*width)*25/23) / 2

        border_w = int(self.cs[0]*3/4) / 262 * 5  # half
        border_h = (5*interval+6*width) / 23      # half
        self.chip.change_chip_size(int(width*1.5/4))
        points = []
        for i in range(4):
            player = self.players[i]
            point = 0
            for c in range(len(player.depose)):
                player.depose[c].turn_over(True)
                
                self.c.create_image(border_w + a + interval + width*c, border_h + b + interval + (interval+width*1.5) * i,
                                    image=self.card.card_obj_to_image(player.depose[c], width), anchor="nw"
                                    )
                point += player.depose[c].data_to_num()[1]
            if point:
                self.c.create_text(border_w + a + interval + width*(c+1), border_h + b + interval + (interval+width*1.5) * i + width*0.75,
                                   anchor="w", text=f"{point}", font=font_get(int(width*3/8)), fill="gold"
                                   )
            points.append(point)
            player.depose.clear()

        # judge winner
        min_p = min(points)
        info = []
        for _ in range(4):
            info.append(
                (_,
                 "win" if points[_] == min_p else "lose",
                 points[_])
            )
        win, lose = 0, 0
        bet = 0
        for _ in info:
            if _[1] == "win":
                win += 1
            else:
                lose += 1
                bet += _[2] if _[2] <= 50 else _[2] * 2
        for _ in range(4):
            if info[_][1] == "win":
                text = f"+ {int(bet/win)}$"
                self.players[_].money += int(bet/win)
            else:
                if info[_][2] > 50:
                    text = f"- {info[_][2]*2}$"
                    self.players[_].money -= info[_][2] * 2
                else:
                    text = f"- {info[_][2]}$"
                    self.players[_].money -= info[_][2]
            self.c.create_text(a + int(self.cs[0]*3/4) - interval - border_w, border_h + b + interval + (interval+width*1.5) * _,
                               anchor="ne", text=self.players[_].name, font=font_get(int(width*1.5*3/12)), fill=color[_]
                               )
            self.c.create_text(a + int(self.cs[0]*3/4) - interval - border_w, border_h + b + interval + (interval+width*1.5) * _ + int(width*1.5*3/12)*4/3,
                               anchor="ne", text=text, font=font_get(int(width*1.5*3/20)), fill="#ff6b87" if info[_][1] == "win" else "green",
                               )
            self.chip.show_chips(info[_][2] if info[_][1] == "lose" else int(bet/win), (a + int(self.cs[0]*3/4) - interval - border_w,
                                                                                        border_h + b + interval + (interval+width*1.5) * _ + width*1.5))
        self.c.update()
        self.chip.change_chip_size(50)
        time.sleep(7)
        self.round_count += 1
        
        self.round(self.round_count)
        
