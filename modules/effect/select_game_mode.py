from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.font import font_get, measure
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from modules.effect.base import Base
from collections import namedtuple
import time


img_path = "images\\effect\\select_game_mode"

class Effect(Base):
    money_for_round = {
        3: 100,
        5: 200,
        10: 500,
        15: 750
    }

    def __init__(self, main, controler, timer_number=1):
        super().__init__(main, controler, timer_number)
        self.c = self.main.canvas
        self.cs = self.main.canvas_side

    def __switch_image(self, genre, state: int):
        w = self.cs[0]
        if genre == "bankruptcy":
            self.c.itemconfig(f"mode-bankruptcy-img{state}", state="normal")
            self.c.itemconfig(f"mode-bankruptcy-img{int(not(state))}", state="hidden")
        elif genre == "round":
            for point in range(6):
                self.c.itemconfig(
                    f"mode-round-img{point}", state="normal" if point == state else "hidden"
                )
        elif genre == "ok":
            self.c.itemconfig(f"frame-ok{state}", state="normal")
            self.c.itemconfig(f"frame-ok{int(not state)}", state="hidden")
            self.c.move("frame-ok-arrow", 40 * (1 if state else -1), 0)
            # revise left
            if not(self.c.coords("frame-ok-arrow")[0] > w/2 + int(w-30) / 2 - 140 - 2 - 40):
                self.c.move("frame-ok-arrow", 40, 0)
                
    def __show_frame(self, type_):
        def chip_manipulate(genre: str, value):
            """
            add or remove 
            """
            play_sound(f"effect/select_game_mode/{genre}_chip")
            self.__bankruptcy_money += value * (1 if genre == "add" else -1)
            self.__valid = True

            if self.__bankruptcy_money > 2000:
                self.__bankruptcy_money = 2000
            if self.__bankruptcy_money <= 0:
                self.__bankruptcy_money = 0
                self.__valid = False
                self.__state2 = 0
                self.__switch_image("ok", self.__state2)
            
            show_info("bankruptcy")
            draw_chips(self.__bankruptcy_money)

        def round_manipulate(round, sound=True):
            if sound:
                play_sound("effect/select_game_mode/select_round")

            for i in self.__class__.money_for_round:
                self.c.itemconfig(
                    f"frame-number-{i}-normal", state="hidden" if i == round else "normal")
                self.c.itemconfig(
                    f"frame-number-{i}-hidden", state="normal" if i == round else "hidden")
                

            self.__round_round = round
            self.__round_money = self.__class__.money_for_round[round]
            self.__valid = True
            show_info("round") 
            draw_chips(self.__round_money)
                
        def draw_chips(moeny: int):
            self.c.delete("chips")
            self.controler.chip.show_chips(moeny, (w/2 + int(w-30)/2 - 100 -
                measure("Money: 1000", int(height*3/8)),
                y + padding+(height+interval) + height/2
            ))

        def show_info(type_: str):
            round = self.__dict__[f"_{self.__class__.__name__}__{type_}_round"]
            money = self.__dict__[f"_{self.__class__.__name__}__{type_}_money"]
         
            self.c.delete(f"frame-info")
            self.c.create_text(w/2 + int(w-30)/2 - 50 - measure("Money: 1000", int(height*3/8)), y + padding, text=f"Round: {round}",
                            fill="gold", font=font_get(int(height*3/8)), anchor="nw",
                            tag=("mode", f"frame", "frame-info"))

            self.c.create_text(w/2 + int(w-30)/2 - 50 - measure("Money: 1000", int(height*3/8)),
                            y + padding+(height+interval), text=f"Money: {money:^4d}",
                            fill="gold", font=font_get(int(height*3/8)), anchor="nw",
                            tag=("mode", f"frame", "frame-info"))
        
        self.c.delete("frame")
        w, h = self.cs
        padding = 15
        interval = 8
        height = int((int(h/2-20) - 2 * padding -
                      interval - 28 * 4 / 3 * 2.5)/2)
        x, y = w/2 - int(w-30)/2, h / 4 * 3 - int(h/2-20) / 2
        x += 30
        y += 28 * 4 / 3 * 2.5

        self.c.create_image(w/2, h / 4 * 3,
            image=tk_image("press_frame.png", int(
            w-30), int(h/2-20), dirpath=img_path),
             tags=("mode", "frame"))

        if type_ == "bankruptcy":
            self.c.create_text(w/2, h / 4 * 3 - int(h/2-20) / 2 + 10, text="Select Start Money\n(Left Click For Adding and Right For Removing)",
                               justify="center", fill="#ff6b87", font=font_get(28), anchor="n",
                               tag=("mode", "frame"))

            for num, value in enumerate((1, 10, 50, 200)):
                self.controler.chip.draw_single_chip(value, (
                    x + padding+(height+interval)*(num % 2), y +
                    padding+(height+interval)*(num//2)
                ), (height, height), anchor="nw", tags=("mode", "frame", f"frame-chip-{value}")
                )

                self.c.tag_bind(
                    f"frame-chip-{value}", "<Button-1>", lambda e, v=value: chip_manipulate("add", v))
                self.c.tag_bind(
                    f"frame-chip-{value}", "<Button-3>", lambda e, v=value: chip_manipulate("remove", v))
            if self.__bankruptcy_money <= 0:
                self.__valid = False
            else:
                self.__valid = True
            show_info("bankruptcy")
            draw_chips(self.__bankruptcy_money)
        elif type_ == "round":
            self.c.create_text(w/2, h / 4 * 3 - int(h/2-20) / 2 + 10, text="Select Round Number\n(Left Click For Choicing)",
                               justify="center", fill="#ff6b87", font=font_get(28), anchor="n",
                               tag=("mode", "frame"))

            for num, value in enumerate((3, 5, 10, 15)):
                if len(str(value)) >= 2:
                    for n in range(len(str(value))):
                        self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5 + padding+(height+interval)*0.5*n, y + padding+(height+interval)*(num//2),
                                            image=tk_image(
                            f"round_{str(value)[n]}_normal.png", height=height, dirpath=img_path),
                            tags=("mode", "frame", f"frame-number-{value}-normal"), anchor='nw')
                        self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5 + padding+(height+interval)*0.5*n, y + padding+(height+interval)*(num//2),
                                            image=tk_image(
                            f"round_{str(value)[n]}_hidden.png", height=height, dirpath=img_path), state="hidden",
                            tags=("mode", "frame", f"frame-number-{value}-hidden"), anchor='nw')
                else:
                    self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5, y + padding+(height+interval)*(num//2),
                                        image=tk_image(
                                            f"round_{value}_normal.png", height=height, dirpath=img_path),
                                        tags=("mode", "frame", f"frame-number-{value}-normal"), anchor='nw')
                    self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5, y + padding+(height+interval)*(num//2),
                                        image=tk_image(
                                            f"round_{value}_hidden.png", height=height, dirpath=img_path), state="hidden",
                                        tags=("mode", "frame", f"frame-number-{value}-hidden"), anchor='nw')
                self.c.tag_bind(
                    f"frame-number-{value}-normal", "<Button-1>", lambda e, v=value: round_manipulate(v))
            
            if self.__round_round:
                round_manipulate(self.__round_round, sound=False)
            else:
                self.__valid = False
            show_info("round")
            draw_chips(self.__round_money)
        # create ok label
        self.c.create_image(w/2 + int(w-30) / 2 - 50, h / 4 * 3 + int(h/2-20) / 2 - 15,
                            image=tk_image(
            f"ok_normal.png", height=60, dirpath=img_path),
            tags=("mode", "frame", f"frame-ok0"), anchor='se')
        self.c.create_image(w/2 + int(w-30) / 2 - 50, h / 4 * 3 + int(h/2-20) / 2 - 15,
                            image=tk_image(
            f"ok_hidden.png", height=60, dirpath=img_path), state="hidden",
            tags=("mode", "frame", f"frame-ok1"), anchor='se')
        self.c.create_image(w/2 + int(w-30) / 2 - 180, h / 4 * 3 + int(h/2-20) / 2 - 15,
                            image=tk_image(
            f"arrow_right.png", height=60, dirpath=img_path),
            tags=("mode", "frame", f"frame-ok-arrow"), anchor='se')

        self.c.tag_bind(f"frame-ok0",
                        "<Button-1>", lambda e: self.end(e))
        self.c.tag_bind(f"frame-ok1",
                        "<Button-1>", lambda e: self.end(e))
    

    

    

    

    

    def start(self):
        self.__enter_area = None
        self.__state = 0 # for dicr or chip
        self.__state2 = 0 # for ok text
        self.__bankruptcy_money = 0
        self.__bankruptcy_round = "∞"
        self.__round_money = 0
        self.__round_round = None
        self.__valid = False
        
        def press(type_):
            play_sound("effect/select_game_mode/press")

            self.c.itemconfig(f"mode-bankruptcy-outline", 
                              state="normal" if type_ == "bankruptcy" else "hidden")
            self.c.itemconfig(f"mode-round-outline", 
                              state="normal" if type_ == "round" else "hidden")
            
            self.__show_frame(type_)

        canvas_reduction(self.c, self.cs, self.controler.music_player,
                         "select_game_mode.png", "effect\\select_game_mode.mp3")

        w, h = self.cs

        # ------------------------- bankruptcy mode -------------------------

        # select rectangle
        self.c.create_rectangle(w/4 - int(w/2-30) / 2, h / 4 - int(h/2) / 2,
                                w/4 + int(w/2-30) / 2, h / 4 + int(h/2) / 2,
                                outline="red", width=20, state="hidden",
                                tags=("mode", f"mode-bankruptcy", "mode-bankruptcy-outline"))
        # show frame
        self.c.create_image(w/4, h/4, image=tk_image("frame.png", int(
            w/2-30), int(h/2), dirpath=img_path),
            tags=("mode", f"mode-bankruptcy"))
        # title
        self.c.create_image(w/4, h/16, image=tk_image("bankruptcy_title.png", int(
            w/4-30), int(h/12), dirpath=img_path),
            tags=("mode", f"mode-bankruptcy"))
        # image
        self.c.create_image(w/4, h/16*4,
                            image=tk_image("bankruptcy_normal.png",  height=int(
                                h/5), dirpath=img_path),
                            tags=("mode", f"mode-bankruptcy", "mode-bankruptcy-img0"))
        self.c.create_image(w/4, h/16*4,
                            image=tk_image("bankruptcy_hidden.png",  height=int(
                                h/5), dirpath=img_path), state="hidden",
                            tags=("mode", f"mode-bankruptcy", "mode-bankruptcy-img1"))
        # text
        self.c.create_text(w/4, h / 16 * 4 + int(h/5) / 2, text="Never End Until\nSomeone Bankrupt",
                           justify="center", fill="#ff6b87", font=font_get(int(h/30*3/4)), anchor="n",
                           tag=("mode", f"mode-bankruptcy"))
        
    
        self.c.tag_bind(f"mode-bankruptcy",
                        "<Button-1>", lambda e: press("bankruptcy"))

        # ------------------------- round mode -------------------------

        # select rectangle
        self.c.create_rectangle(w/4*3 - int(w/2-30) / 2, h / 4 - int(h/2) / 2,
                                w/4*3 + int(w/2-30) / 2, h / 4 + int(h/2) / 2,
                                outline="red", width=20, state="hidden",
                                tags=("mode", f"mode-round", "mode-round-outline"))
        # show frame
        self.c.create_image(w/4*3, h/4, image=tk_image("frame.png", int(
            w/2-30), int(h/2), dirpath=img_path),
            tags=("mode", f"mode-round"))

        # title
        self.c.create_image(w/4*3, h/16, image=tk_image("round_title.png", int(
            w/4-30), int(h/12), dirpath=img_path),
            tags=("mode", f"mode-round"))

        # image
        self.c.create_image(w/4*3, h/16*4,
                            image=tk_image("dice_normal.png",  height=int(
                                h/5), dirpath=img_path),
                            tags=("mode", f"mode-round", "mode-round-img0"))
        for i in range(2, 7):
            self.c.create_image(w/4*3, h/16*4,
                                image=tk_image(f"dice_{i}.png",  height=int(
                                    h/5), dirpath=img_path), state="hidden",
                                tags=("mode", f"mode-round", f"mode-round-img{i-1}"))
        # text
        self.c.create_text(w/4*3, h / 16 * 4 + int(h/5) / 2, text="After A Set Number Of Rounds\nPlayer With Most Money Wins\n(Someone Bankrupt Also End)",
                           justify="center", fill="#ff6b87", font=font_get(int(h/30*3/4)), anchor="n",
                           tag=("mode", f"mode-round"))

        self.c.tag_bind(f"mode-round",
                        "<Button-1>", lambda e: press("round"))

    def end(self, e):
        if self.__valid:
            play_sound("effect/select_game_mode/success")
            area = "round" if self.c.itemcget("mode-round-outline", "state") == "normal" else "bankruptcy"
            self.controler.user_select_game_mode = namedtuple("game_mode", "round money")(
                self.__dict__[f"_{self.__class__.__name__}__{area}_round"], 
                self.__dict__[f"_{self.__class__.__name__}__{area}_money"]
            )
            # start game
            self.controler.round(self.controler.round_count)
        else:
            play_sound("effect/select_game_mode/enter_invalid")
            
            
    def loop(self):
        def leave_config(genre):
            self.__enter_area = None
            self.__state = 0
            self.__switch_image(genre, self.__state)

        if not self.c.find_withtag("mode"):
            return
        result = self.detect()
        
        if result:
            if self.__enter_area != result:
                play_sound("effect/select_game_mode/enter")
                if self.__enter_area:
                    leave_config(self.__enter_area)
            self.__enter_area = result
        else:
            if self.__enter_area:
                leave_config(self.__enter_area)

        if (t := time.time()) - self.timer[0] >= 0.4:
            if (type_ := self.__enter_area) is not None:
                self.__switch_image(type_, self.__state)
                if type_ == "bankruptcy":
                    self.__state = int(not self.__state)
                elif type_ == "round":
                    if self.__state == 5:
                        self.__state = -1
                    self.__state += 1

            if self.__valid and self.c.find_withtag("frame-ok-arrow"):
                self.__state2 = int(not self.__state2)
                self.__switch_image("ok", self.__state2)
                

            self.timer[0] = t

    
