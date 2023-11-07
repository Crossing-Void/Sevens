from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.font import font_get, measure
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from modules.effect.base import Base
import time


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

    def __switch_bankruptcy_image(self, state: int):
        # state is 0 original, 1 is hidden
        if state:
            self.c.itemconfig(
                "player-mode-image-bankruptcy-normal", state="hidden")
            self.c.itemconfig(
                "player-mode-image-bankruptcy-hidden", state="normal")
        else:
            self.c.itemconfig(
                "player-mode-image-bankruptcy-normal", state="normal")
            self.c.itemconfig(
                "player-mode-image-bankruptcy-hidden", state="hidden")

    def __switch_round_dice(self, state: int):
        for point in range(1, 7):
            if point == 1:
                tags = f"player-mode-image-round-dice_normal"
            else:
                tags = f"player-mode-image-round-dice_{point}"

            self.c.itemconfig(
                tags, state="normal" if point == state else "hidden"
            )

    def __switch_ok(self, state: int):
        # 0 is on

        w = self.cs[0]
        on = f"player-mode-oknormal"
        off = f"player-mode-okhidden"
        ok = f"player-mode-okarrow"

        if state:
            self.c.itemconfig(
                on, state="normal")
            self.c.itemconfig(
                off, state="hidden")
            self.c.move(ok, 40, 0)
        else:
            self.c.itemconfig(
                on, state="hidden")
            self.c.itemconfig(
                off, state="normal")
            if self.c.coords(ok)[0] > w/2 + int(w-30) / 2 - 140 - 2:
                self.c.move(ok, -40, 0)

    def __add_chips(self, value):
        play_sound("effect/select_game_mode/add_chip")
        self.__bankruptcy_money += value
        if self.__bankruptcy_money > 2000:
            self.__bankruptcy_money = 2000
        self.__valid = True
        self.__show_round_money_info("bankruptcy")
        self.__draw_chips_for_money(self.__bankruptcy_money)

    def __remove_chips(self, value):
        play_sound("effect/select_game_mode/remove_chip")
        self.__bankruptcy_money -= value
        if self.__bankruptcy_money < 0:
            self.__bankruptcy_money = 0
        if self.__bankruptcy_money == 0:
            self.__valid = False
            self.__ok_state = 0
            self.__switch_ok(self.__ok_state, "bankruptcy")
        self.__show_round_money_info("bankruptcy")
        self.__draw_chips_for_money(self.__bankruptcy_money)

    def __select_round(self, num, round, sound=True):
        if sound:
            play_sound("effect/select_game_mode/select_round")

        for i in range(4):
            if i == num:
                self.c.itemconfig(
                    f"player-mode-hidden-round-number{i}-normal", state="hidden")
                self.c.itemconfig(
                    f"player-mode-hidden-round-number{i}-hidden", state="normal")
            else:
                self.c.itemconfig(
                    f"player-mode-hidden-round-number{i}-normal", state="normal")
                self.c.itemconfig(
                    f"player-mode-hidden-round-number{i}-hidden", state="hidden")

        self.__round_round = round
        self.__round_money = self.__class__.money_for_round[round]
        self.__valid = True
        self.__show_round_money_info("round")

    def __draw_chips_for_money(self, moeny: int):
        w, h = self.cs
        padding = 15
        interval = 8
        height = int((int(h/2-20) - 2 * padding -
                      interval - 28 * 4 / 3 * 2.5)/2)
        x, y = w/2 - int(w-30)/2, h / 4 * 3 - int(h/2-20) / 2
        x += 30
        y += 28 * 4 / 3 * 2.5
        self.c.delete("chip")
        self.controler.chip.show_chips(moeny, (
            w/2 + int(w-30)/2 - 100 -
            measure("Money: 1000", int(height*3/8)),
            y + padding+(height+interval) + height/2
        ))

    def __show_round_money_info(self, type_: str):
        w, h = self.cs
        padding = 15
        interval = 8
        height = int((int(h/2-20) - 2 * padding -
                      interval - 28 * 4 / 3 * 2.5)/2)
        x, y = w/2 - int(w-30)/2, h / 4 * 3 - int(h/2-20) / 2
        x += 30
        y += 28 * 4 / 3 * 2.5

        if type_ == "bankruptcy":
            round = self.__bankruptcy_round
            money = self.__bankruptcy_money
        elif type_ == "round":
            round = self.__round_round
            money = self.__round_money

        self.c.delete(f"player-mode-info")
        self.c.create_text(w/2 + int(w-30)/2 - 50 - measure("Money: 1000", int(height*3/8)), y + padding, text=f"Round: {round}",
                           fill="gold", font=font_get(int(height*3/8)), anchor="nw",
                           tag=("player-mode", f"player-mode-info", "player_mode-frame"))

        self.c.create_text(w/2 + int(w-30)/2 - 50 - measure("Money: 1000", int(height*3/8)),
                           y + padding+(height+interval), text=f"Money: {money:^4d}",
                           fill="gold", font=font_get(int(height*3/8)), anchor="nw",
                           tag=("player-mode", f"player-mode-info", "player_mode-frame"))

    def start(self):
        self.__select_game_mode_type = None
        self.__select_game_mode_state = 0

        self.__bankruptcy_money = 0
        self.__bankruptcy_round = "∞"
        self.__round_money = 0
        self.__round_round = "None"
        self.__valid = False
        self.__ok_state = 0

        def enter(type_):
            play_sound("effect/select_game_mode/enter")
            self.__select_game_mode_type = type_

        def leave(type_):
            if self.__select_game_mode_state != 0:
                if type_ == "bankruptcy":
                    self.__switch_bankruptcy_image(0)
                else:
                    self.__switch_round_dice(1)

            self.__select_game_mode_type = None
            self.__select_game_mode_state = 0

        def press(type_):
            play_sound("effect/select_game_mode/press")
            if type_ == "bankruptcy":
                self.c.itemconfig(
                    f"player-mode-outline-bankruptcy", state="normal")
                self.c.itemconfig(
                    f"player-mode-outline-round", state="hidden")
                self.controler.user_select_game_mode = "bankruptcy"

            elif type_ == "round":
                self.c.itemconfig(
                    f"player-mode-outline-round", state="normal")
                self.c.itemconfig(
                    f"player-mode-outline-bankruptcy", state="hidden")
                self.controler.user_select_game_mode = "round"
            self.show_frame(type_)

        canvas_reduction(self.c, self.cs, self.controler.music_player,
                         "select_game_mode.png", "effect\\select_game_mode.mp3")

        w, h = self.cs

        # bankruptcy mode

        # select rectangle
        self.c.create_rectangle(w/4 - int(w/2-30) / 2, h / 4 - int(h/2) / 2,
                                w/4 + int(w/2-30) / 2, h / 4 + int(h/2) / 2,
                                outline="red", width=20, state="hidden",
                                tags=("player-mode", f"player-mode-outline-bankruptcy", f"player-mode-whole-bankruptcy"))
        # show frame
        self.c.create_image(w/4, h/4, image=tk_image("frame.png", int(
            w/2-30), int(h/2), dirpath="images\\effect\\select_game_mode"),
            tags=("player-mode", f"player-mode-frame-bankruptcy", f"player-mode-whole-bankruptcy"))
        # title
        self.c.create_image(w/4, h/16, image=tk_image("bankruptcy_title.png", int(
            w/4-30), int(h/12), dirpath="images\\effect\\select_game_mode"),
            tags=("player-mode", f"player-mode-image-bankruptcy", f"player-mode-whole-bankruptcy"))
        self.c.create_image(w/4, h/16*4,
                            image=tk_image("bankruptcy_normal.png",  height=int(
                                h/5), dirpath="images\\effect\\select_game_mode"),
                            tags=("player-mode", (f"player-mode-image-bankruptcy-normal"), f"player-mode-whole-bankruptcy"))
        self.c.create_image(w/4, h/16*4,
                            image=tk_image("bankruptcy_hidden.png",  height=int(
                                h/5), dirpath="images\\effect\\select_game_mode"), state="hidden",
                            tags=("player-mode", (f"player-mode-image-bankruptcy-hidden"), f"player-mode-whole-bankruptcy"))
        self.c.create_text(w/4, h / 16 * 4 + int(h/5) / 2, text="Never End Until\nSomeone Bankrupt",
                           justify="center", fill="#ff6b87", font=font_get(int(h/30*3/4)), anchor="n",
                           tag=("player-mode", f"player-mode-text-bankruptcy", f"player-mode-whole-bankruptcy"))
        self.c.tag_bind(f"player-mode-whole-bankruptcy",
                        "<Enter>", lambda e, i="bankruptcy": enter(i))
        self.c.tag_bind(f"player-mode-whole-bankruptcy",
                        "<Leave>", lambda e, i="bankruptcy": leave(i))
        self.c.tag_bind(f"player-mode-whole-bankruptcy",
                        "<Button-1>", lambda e, i="bankruptcy": press(i))
        # round mode

        # select rectangle
        self.c.create_rectangle(w/4*3 - int(w/2-30) / 2, h / 4 - int(h/2) / 2,
                                w/4*3 + int(w/2-30) / 2, h / 4 + int(h/2) / 2,
                                outline="red", width=20, state="hidden",
                                tags=("player-mode", f"player-mode-outline-round", f"player-mode-whole-round"))
        # show frame
        self.c.create_image(w/4*3, h/4, image=tk_image("frame.png", int(
            w/2-30), int(h/2), dirpath="images\\effect\\select_game_mode"),
            tags=("player-mode", f"player-mode-frame-round", f"player-mode-whole-round"))

        # title
        self.c.create_image(w/4*3, h/16, image=tk_image("round_title.png", int(
            w/4-30), int(h/12), dirpath="images\\effect\\select_game_mode"),
            tags=("player-mode", f"player-mode-image-round", f"player-mode-whole-round"))

        # dice normal
        self.c.create_image(w/4*3, h/16*4,
                            image=tk_image("dice_normal.png",  height=int(
                                h/5), dirpath="images\\effect\\select_game_mode"),
                            tags=("player-mode", (f"player-mode-image-round-dice_normal"), f"player-mode-whole-round"))
        for i in range(2, 7):

            self.c.create_image(w/4*3, h/16*4,
                                image=tk_image(f"dice_{i}.png",  height=int(
                                    h/5), dirpath="images\\effect\\select_game_mode"), state="hidden",
                                tags=("player-mode", (f"player-mode-image-round-dice_{i}"), f"player-mode-whole-round"))

        self.c.create_text(w/4*3, h / 16 * 4 + int(h/5) / 2, text="After A Set Number Of Rounds\nPlayer With Most Money Wins\n(Someone Bankrupt Also End)",
                           justify="center", fill="#ff6b87", font=font_get(int(h/30*3/4)), anchor="n",
                           tag=("player-mode", f"player-mode-text-round", f"player-mode-whole-round"))

        self.c.tag_bind(f"player-mode-whole-round",
                        "<Enter>", lambda e, i="round": enter(i))
        self.c.tag_bind(f"player-mode-whole-round",
                        "<Leave>", lambda e, i="round": leave(i))
        self.c.tag_bind(f"player-mode-whole-round",
                        "<Button-1>", lambda e, i="round": press(i))

    def end(self):
        play_sound("effect/select_game_mode/press")
        print(self.controler.user_select_game_mode)
#         play_sound("player_mode/press_frame")
#         if mode == "bankruptcy":
#             if self.__backruptcy_valid:
#                 self.app.game_mode = (
#                     self.__bankruptcy_round, self.__bankruptcy_money)
#                 self.app.controler.initialize()
#         elif mode == "round":
#             if self.__round_valid:
#                 self.app.game_mode = (self.__round_round, self.__round_money)
#                 self.app.controler.initialize()

    def loop(self):
        if not self.c.find_withtag("player-mode"):
            return
        if (t := time.time()) - self.timer[0] >= 0.4:
            if (type_ := self.__select_game_mode_type) is not None:
                if type_ == "bankruptcy":
                    self.__select_game_mode_state = int(
                        not self.__select_game_mode_state)
                    self.__switch_bankruptcy_image(
                        self.__select_game_mode_state)

                elif type_ == "round":
                    if self.__select_game_mode_state == 6:
                        self.__select_game_mode_state = 0
                    self.__select_game_mode_state += 1
                    self.__switch_round_dice(self.__select_game_mode_state)

            if self.__valid and self.c.find_withtag("player-mode-okarrow"):
                self.__ok_state = int(not self.__ok_state)
                self.__switch_ok(self.__ok_state)

            self.timer[0] = t

    def show_frame(self, type_):
        self.c.delete("player_mode-frame")

        w, h = self.cs
        padding = 15
        interval = 8
        height = int((int(h/2-20) - 2 * padding -
                      interval - 28 * 4 / 3 * 2.5)/2)
        x, y = w/2 - int(w-30)/2, h / 4 * 3 - int(h/2-20) / 2
        x += 30
        y += 28 * 4 / 3 * 2.5

        # create skeleton
        if not self.c.find_withtag("player-mode-hidden-rectangle"):
            self.c.create_image(w/2, h / 4 * 3,
                                image=tk_image("press_frame.png", int(
                                    w-30), int(h/2-20), dirpath="images\\effect\\select_game_mode"),
                                tags=("player-mode", f"player-mode-hidden-rectangle", "player_mode-frame"))

        if type_ == "bankruptcy":
            self.c.create_text(w/2, h / 4 * 3 - int(h/2-20) / 2 + 10, text="Select Start Money\n(Left Click For Adding and Right For Removing)",
                               justify="center", fill="#ff6b87", font=font_get(28), anchor="n",
                               tag=("player-mode", f"player-mode-hidden-bankruptcy-text", "player_mode-frame"))

            for num, value in enumerate((1, 10, 50, 200)):
                self.controler.chip.draw_chip(value, (
                    x + padding+(height+interval)*(num % 2), y +
                    padding+(height+interval)*(num//2)
                ), (height, height), anchor="nw", tags=("player-mode", f"player-mode-hidden-bankruptcy-chip{value}", "player_mode-frame")
                )

                self.c.tag_bind(
                    f"player-mode-hidden-bankruptcy-chip{value}", "<Button-1>", lambda e, v=value: self.__add_chips(v))
                self.c.tag_bind(
                    f"player-mode-hidden-bankruptcy-chip{value}", "<Button-3>", lambda e, v=value: self.__remove_chips(v))
            self.__show_round_money_info("bankruptcy")
            self.__draw_chips_for_money(self.__bankruptcy_money)
        elif type_ == "round":
            self.c.create_text(w/2, h / 4 * 3 - int(h/2-20) / 2 + 10, text="Select Round Number\n(Left Click For Choicing)",
                               justify="center", fill="#ff6b87", font=font_get(28), anchor="n",
                               tag=("player-mode", f"player-mode-hidden-round-text", "player_mode-frame"))

            for num, value in enumerate((3, 5, 10, 15)):
                if len(str(value)) == 2:
                    for n in range(len(str(value))):
                        self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5 + padding+(height+interval)*0.5*n, y + padding+(height+interval)*(num//2),
                                            image=tk_image(
                            f"round_{str(value)[n]}_normal.png", height=height, dirpath="images\\effect\\select_game_mode"),
                            tags=("player-mode", f"player-mode-hidden-round-number{num}-normal", "player_mode-frame"), anchor='nw')
                        self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5 + padding+(height+interval)*0.5*n, y + padding+(height+interval)*(num//2),
                                            image=tk_image(
                            f"round_{str(value)[n]}_hidden.png", height=height, dirpath="images\\effect\\select_game_mode"), state="hidden",
                            tags=("player-mode", f"player-mode-hidden-round-number{num}-hidden", "player_mode-frame"), anchor='nw')
                else:
                    self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5, y + padding+(height+interval)*(num//2),
                                        image=tk_image(
                                            f"round_{value}_normal.png", height=height, dirpath="images\\effect\\select_game_mode"),
                                        tags=("player-mode", f"player-mode-hidden-round-number{num}-normal", "player_mode-frame"), anchor='nw')
                    self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5, y + padding+(height+interval)*(num//2),
                                        image=tk_image(
                                            f"round_{value}_hidden.png", height=height, dirpath="images\\effect\\select_game_mode"), state="hidden",
                                        tags=("player-mode", f"player-mode-hidden-round-number{num}-hidden", "player_mode-frame"), anchor='nw')
                self.c.tag_bind(
                    f"player-mode-hidden-round-number{num}-normal", "<Button-1>", lambda e, v=num, v2=value: self.__select_round(v, v2))
            self.__show_round_money_info("round")
            self.__draw_chips_for_money(self.__round_money)
        # create ok label
        self.c.create_image(w/2 + int(w-30) / 2 - 50, h / 4 * 3 + int(h/2-20) / 2 - 15,
                            image=tk_image(
            f"ok_normal.png", height=60, dirpath="images\\effect\\select_game_mode"),
            tags=("player-mode", f"player-mode-oknormal", "player_mode-frame"), anchor='se')
        self.c.create_image(w/2 + int(w-30) / 2 - 50, h / 4 * 3 + int(h/2-20) / 2 - 15,
                            image=tk_image(
            f"ok_hidden.png", height=60, dirpath="images\\effect\\select_game_mode"), state="hidden",
            tags=("player-mode", f"player-mode-okhidden", "player_mode-frame"), anchor='se')
        self.c.create_image(w/2 + int(w-30) / 2 - 180, h / 4 * 3 + int(h/2-20) / 2 - 15,
                            image=tk_image(
            f"arrow_right.png", height=60, dirpath="images\\effect\\select_game_mode"),
            tags=("player-mode", f"player-mode-okarrow", "player_mode-frame"), anchor='se')

        self.c.tag_bind("player-mode-oknormal",
                        "<Button-1>", lambda e: self.end())
        self.c.tag_bind("player-mode-okhidden",
                        "<Button-1>", lambda e: self.end())
