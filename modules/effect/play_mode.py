from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, measure, font_span
from Tkinter_template.Assets.soundeffect import play_sound
from modules.game.chips import Chip
import time


class Effect:
    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side
        self.chips = Chip(self.app)

    def __switch_image(self, state: int):
        if state:
            self.c.itemconfig("player-mode-image0-normal", state="hidden")
            self.c.itemconfig("player-mode-image0-hidden", state="normal")
        else:
            self.c.itemconfig("player-mode-image0-normal", state="normal")
            self.c.itemconfig("player-mode-image0-hidden", state="hidden")

    def __switch_dice(self, state: int):
        for point in range(1, 7):
            if point == state:
                self.c.itemconfig(
                    f"player-mode-image1-hidden{point}", state="normal")
            else:
                self.c.itemconfig(
                    f"player-mode-image1-hidden{point}", state="hidden")

    def __switch_ok(self, state: int, mode: str):
        # 0 is on

        w = self.cs[0]
        on = f"player-mode-hidden-{mode}-ok-on"
        off = f"player-mode-hidden-{mode}-ok-off"
        ok = f"player-mode-hidden-{mode}-ok-deco"

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

    def __show_frame(self, i):
        self.c.delete("player_mode-frame")

        def add_chips(value):

            play_sound("player_mode/up")
            self.__bankruptcy_money += value
            if self.__bankruptcy_money > 2000:
                self.__bankruptcy_money = 2000
            self.__backruptcy_valid = True
            show()
            self.c.delete("chip")
            self.chips.show_chips(self.__bankruptcy_money, (
                w/2 + int(w-30)/2 - 100 -
                measure("Money: 1000", int(height*3/8)),
                y + padding+(height+interval) + height/2
            ))

        def remove_chips(value):
            play_sound("player_mode/down")
            self.__bankruptcy_money -= value
            if self.__bankruptcy_money < 0:
                self.__bankruptcy_money = 0
            if self.__bankruptcy_money == 0:
                self.__backruptcy_valid = False
                self.__ok_state = 0
                self.__switch_ok(self.__ok_state, "bankruptcy")
            show()
            self.c.delete("chip")
            self.chips.show_chips(self.__bankruptcy_money, (
                w/2 + int(w-30)/2 - 100 -
                measure("Money: 1000", int(height*3/8)),
                y + padding+(height+interval) + height/2
            ))

        def show():
            self.c.delete(f"player-mode-hidden-bankruptcy-round")
            self.c.delete(f"player-mode-hidden-bankruptcy-money")
            self.c.create_text(w/2 + int(w-30)/2 - 50 - measure("Money: 1000", int(height*3/8)), y + padding, text=f"Round: {self.__bankruptcy_round}",
                               fill="gold", font=font_get(int(height*3/8)), anchor="nw",
                               tag=("player-mode", f"player-mode-hidden-bankruptcy-round", "player_mode-frame"))

            self.c.create_text(w/2 + int(w-30)/2 - 50 - measure("Money: 1000", int(height*3/8)),
                               y + padding+(height+interval), text=f"Money: {self.__bankruptcy_money:^4d}",
                               fill="gold", font=font_get(int(height*3/8)), anchor="nw",
                               tag=("player-mode", f"player-mode-hidden-bankruptcy-money", "player_mode-frame"))

        def show2():
            self.c.delete(f"player-mode-hidden-round-round")
            self.c.delete(f"player-mode-hidden-round-money")
            self.c.create_text(w/2 + int(w-30)/2 - 50 - measure("Money: 1000", int(height*3/8)), y + padding, text=f"Round: {str(self.__round_round):^4s}",
                               fill="gold", font=font_get(int(height*3/8)), anchor="nw",
                               tag=("player-mode", f"player-mode-hidden-round-round", "player_mode-frame"))

            self.c.create_text(w/2 + int(w-30)/2 - 50 - measure("Money: 1000", int(height*3/8)),
                               y + padding+(height+interval), text=f"Money: {self.__round_money:^3d}",
                               fill="gold", font=font_get(int(height*3/8)), anchor="nw",
                               tag=("player-mode", f"player-mode-hidden-round-money", "player_mode-frame"))

        def select_round(num, round, sound=True):
            if sound:
                play_sound("player_mode/click_number")

            corr = {
                3: 100,
                5: 200,
                10: 500,
                15: 750
            }

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
            self.__round_money = corr[round]
            self.__round_valid = True
            show2()

        if not self.c.find_withtag("player-mode-hidden-rectangle"):
            w, h = self.cs
            self.c.create_image(w/2, h / 4 * 3,
                                image=tk_image("frame2.png", int(
                                    w-30), int(h/2-20), dirpath="images\\system"),
                                tags=("player-mode", f"player-mode-hidden-rectangle", "player_mode-frame"))
        if i:
            self.c.create_text(w/2, h / 4 * 3 - int(h/2-20) / 2 + 10, text="Select Round Number\n(Left Click For Choicing)",
                               justify="center", fill="#ff6b87", font=font_get(28), anchor="n",
                               tag=("player-mode", f"player-mode-hidden-round-text", "player_mode-frame"))
            padding = 15
            interval = 8
            height = int((int(h/2-20) - 2 * padding -
                         interval - 28 * 4 / 3 * 2.5)/2)
            x, y = w/2 - int(w-30)/2, h / 4 * 3 - int(h/2-20) / 2
            x += 30
            y += 28 * 4 / 3 * 2.5
            for num, value in enumerate((3, 5, 10, 15)):
                self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5, y + padding+(height+interval)*(num//2),
                                    image=tk_image(
                                        f"{value}.png", height=height, dirpath="images\\effect\\icon\\numbers"),
                                    tags=("player-mode", f"player-mode-hidden-round-number{num}-normal", "player_mode-frame"), anchor='nw')
                self.c.create_image(x + padding+(height+interval)*(num % 2)*1.5, y + padding+(height+interval)*(num//2),
                                    image=tk_image(
                                        f"{value}_.png", height=height, dirpath="images\\effect\\icon\\numbers"), state="hidden",
                                    tags=("player-mode", f"player-mode-hidden-round-number{num}-hidden", "player_mode-frame"), anchor='nw')
                self.c.tag_bind(
                    f"player-mode-hidden-round-number{num}-normal", "<Button-1>", lambda e, v=num, v2=value: select_round(v, v2))

            self.c.create_image(w/2 + int(w-30) / 2 - 50, h / 4 * 3 + int(h/2-20) / 2 - 15,
                                image=tk_image(
                f"ok-off.png", height=60, dirpath="images\\effect\\text"),
                tags=("player-mode", f"player-mode-hidden-round-ok-off", "player_mode-frame"), anchor='se')
            self.c.create_image(w/2 + int(w-30) / 2 - 50, h / 4 * 3 + int(h/2-20) / 2 - 15,
                                image=tk_image(
                f"ok-on.png", height=60, dirpath="images\\effect\\text"), state="hidden",
                tags=("player-mode", f"player-mode-hidden-round-ok-on", "player_mode-frame"), anchor='se')
            self.c.create_image(w/2 + int(w-30) / 2 - 180, h / 4 * 3 + int(h/2-20) / 2 - 15,
                                image=tk_image(
                f"play.png", height=60, dirpath="images\\system"),
                tags=("player-mode", f"player-mode-hidden-round-ok-deco", "player_mode-frame"), anchor='se')
            self.c.tag_bind("player-mode-hidden-round-ok-off",
                            "<Button-1>", lambda e: self.end("round"))
            self.c.tag_bind("player-mode-hidden-round-ok-on",
                            "<Button-1>", lambda e: self.end("round"))
            show2()
            try:
                select_round((3, 5, 10, 15).index(
                    self.__round_round), self.__round_round, sound=False)
            except:
                pass

        else:
            self.c.create_text(w/2, h / 4 * 3 - int(h/2-20) / 2 + 10, text="Select Start Money\n(Left Click For Adding and Right For Removing)",
                               justify="center", fill="#ff6b87", font=font_get(28), anchor="n",
                               tag=("player-mode", f"player-mode-hidden-bankruptcy-text", "player_mode-frame"))
            padding = 15
            interval = 8
            height = int((int(h/2-20) - 2 * padding -
                         interval - 28 * 4 / 3 * 2.5)/2)
            x, y = w/2 - int(w-30)/2, h / 4 * 3 - int(h/2-20) / 2
            x += 30
            y += 28 * 4 / 3 * 2.5
            for num, value in enumerate((1, 10, 50, 200)):
                self.c.create_image(x + padding+(height+interval)*(num % 2), y + padding+(height+interval)*(num//2),
                                    image=tk_image(
                                        f"{value}-bottom.png", height=height, dirpath="images\\game\\chips"),
                                    tags=("player-mode", f"player-mode-hidden-bankruptcy-chip{value}", "player_mode-frame"), anchor='nw')
                self.c.tag_bind(
                    f"player-mode-hidden-bankruptcy-chip{value}", "<Button-1>", lambda e, v=value: add_chips(v))
                self.c.tag_bind(
                    f"player-mode-hidden-bankruptcy-chip{value}", "<Button-3>", lambda e, v=value: remove_chips(v))
            show()

            self.c.create_image(w/2 + int(w-30) / 2 - 50, h / 4 * 3 + int(h/2-20) / 2 - 15,
                                image=tk_image(
                f"ok-off.png", height=60, dirpath="images\\effect\\text"),
                tags=("player-mode", f"player-mode-hidden-bankruptcy-ok-off", "player_mode-frame"), anchor='se')
            self.c.create_image(w/2 + int(w-30) / 2 - 50, h / 4 * 3 + int(h/2-20) / 2 - 15,
                                image=tk_image(
                f"ok-on.png", height=60, dirpath="images\\effect\\text"), state="hidden",
                tags=("player-mode", f"player-mode-hidden-bankruptcy-ok-on", "player_mode-frame"), anchor='se')
            self.c.create_image(w/2 + int(w-30) / 2 - 180, h / 4 * 3 + int(h/2-20) / 2 - 15,
                                image=tk_image(
                f"play.png", height=60, dirpath="images\\system"),
                tags=("player-mode", f"player-mode-hidden-bankruptcy-ok-deco", "player_mode-frame"), anchor='se')

            self.c.tag_bind("player-mode-hidden-bankruptcy-ok-off",
                            "<Button-1>", lambda e: self.end("bankruptcy"))
            self.c.tag_bind("player-mode-hidden-bankruptcy-ok-on",
                            "<Button-1>", lambda e: self.end("bankruptcy"))

            self.c.delete("chip")
            self.chips.show_chips(self.__bankruptcy_money, (
                w/2 + int(w-30)/2 - 100 -
                measure("Money: 1000", int(height*3/8)),
                y + padding+(height+interval) + height/2
            ))

    def start(self):
        self.__player_mode_enter = None
        self.__player_mode_state = 0

        self.__bankruptcy_money = 0
        self.__bankruptcy_round = "∞"
        self.__round_money = 0
        self.__round_round = "None"
        self.__backruptcy_valid = False
        self.__round_valid = False
        self.__ok_state = 0

        def enter(i):
            play_sound("player_mode/enter_frame")
            self.__player_mode_enter = i

        def leave(i):
            if self.__player_mode_state != 0:
                if i == 0:
                    self.__switch_image(0)
                else:
                    self.__switch_dice(1)

            self.__player_mode_enter = None
            self.__player_mode_state = 0

        def press(i):
            play_sound("player_mode/press_frame")
            if i:
                self.c.itemconfig(f"player-mode-outline{i}", state="normal")
                self.c.itemconfig(f"player-mode-outline{i-1}", state="hidden")
            else:
                self.c.itemconfig(f"player-mode-outline{i}", state="normal")
                self.c.itemconfig(f"player-mode-outline{i+1}", state="hidden")
            self.__show_frame(i)

        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "play_mode.png", "play_mode.mp3")

        w, h = self.cs
        image_name = ['bankruptcy.png', 'round.png']
        text = ["Never End Until\nSomeone Bankrupt",
                "After A Set Number Of Rounds\nPlayer With Most Money Wins\n(Someone Bankrupt Also End)"
                ]
        for i in range(2):
            self.c.create_rectangle(w/4 * (2*i+1) - int(w/2-30) / 2, h / 4 - int(h/2) / 2,
                                    w/4 * (2*i+1) + int(w/2-30) /
                                    2, h / 4 + int(h/2) / 2,
                                    outline="red", width=20, state="hidden",
                                    tags=("player-mode", f"player-mode-outline{i}", f"player-mode-whole{i}"))
            self.c.create_image(w/4 * (2*i+1), h / 4,
                                image=tk_image("frame.png", int(
                                    w/2-30), int(h/2), dirpath="images\\system"),
                                tags=("player-mode", f"player-mode-frame{i}", f"player-mode-whole{i}"))
            self.c.create_image(w/4 * (2*i+1), h / 16,
                                image=tk_image(image_name[i], int(
                                    w/4-30), int(h/12), dirpath="images\\effect\\text"),
                                tags=("player-mode", f"player-mode-image{i}", f"player-mode-whole{i}"))
            self.c.create_image(w/4 * (2*i+1), h / 16 * 4,
                                image=tk_image(image_name[i],  height=int(
                                    h/5), dirpath="images\\effect\\icon"),
                                tags=("player-mode", (f"player-mode-image{i}-normal" if i == 0 else f"player-mode-image{i}-hidden{i}"), f"player-mode-whole{i}"))
            self.c.create_text(w/4 * (2*i+1), h / 16 * 4 + int(h/5) / 2, text=text[i],
                               justify="center", fill="#ff6b87", font=font_get(int(h/30*3/4)), anchor="n",
                               tag=("player-mode", f"player-mode-text{i}", f"player-mode-whole{i}"))
            if i == 0:
                # bankrupt
                self.c.create_image(w/4 * (2*i+1), h / 16 * 4,
                                    image=tk_image("bankruptcy2.png",  height=int(
                                        h/5), dirpath="images\\effect\\icon"), state="hidden",
                                    tags=("player-mode", f"player-mode-image{i}-hidden", f"player-mode-whole{i}"))
            else:
                # round
                for point in range(2, 7):
                    self.c.create_image(w/4 * (2*i+1), h / 16 * 4,
                                        image=tk_image(f"{point}.png",  height=int(
                                            h/5), dirpath="images\\effect\\icon\\dice"), state="hidden",
                                        tags=("player-mode", f"player-mode-image{i}-hidden{point}", f"player-mode-whole{i}"))
            self.c.tag_bind(f"player-mode-whole{i}",
                            "<Enter>", lambda e, i=i: enter(i))
            self.c.tag_bind(f"player-mode-whole{i}",
                            "<Leave>", lambda e, i=i: leave(i))
            self.c.tag_bind(f"player-mode-whole{i}",
                            "<Button-1>", lambda e, i=i: press(i))
        self.player_mode_timer = time.time()

    def end(self, mode: str):
        play_sound("player_mode/press_frame")
        if mode == "bankruptcy":
            if self.__backruptcy_valid:
                self.app.game_mode = (
                    self.__bankruptcy_round, self.__bankruptcy_money)
                self.app.controler.initialize()
        elif mode == "round":
            if self.__round_valid:
                self.app.game_mode = (self.__round_round, self.__round_money)
                self.app.controler.initialize()

    def loop(self):
        if not self.c.find_withtag("player-mode"):
            return
        if (t := time.time()) - self.player_mode_timer >= 0.4:
            if (s := self.__player_mode_enter) is not None:
                if s == 0:
                    self.__player_mode_state = int(
                        not self.__player_mode_state)
                    self.__switch_image(self.__player_mode_state)

                else:
                    if self.__player_mode_state == 6:
                        self.__player_mode_state = 0
                    self.__player_mode_state += 1
                    self.__switch_dice(self.__player_mode_state)

            if self.__backruptcy_valid and self.c.find_withtag("player-mode-hidden-bankruptcy-ok-deco"):
                self.__ok_state = int(not self.__ok_state)
                self.__switch_ok(self.__ok_state, "bankruptcy")
            if self.__round_valid and self.c.find_withtag("player-mode-hidden-round-ok-deco"):
                self.__ok_state = int(not self.__ok_state)
                self.__switch_ok(self.__ok_state, "round")
            self.player_mode_timer = t
