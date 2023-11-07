from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.font import font_get, font_span
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from modules.effect.base import Base
import time


class Effect(Base):
    color_for_player = {
        "1p": "red",
        "2p": "green",
        "3p": "blue",
        "4p": "gold",
        "com": "black"
    }

    def __init__(self, main, controler, timer_number=1):
        super().__init__(main, controler, timer_number)
        self.c = self.main.canvas
        self.cs = self.main.canvas_side

    def calculate_player_number(self, row, column):
        return row*2 + column + 1

    def start(self):
        def press(r, c):
            play_sound("effect/select_player_number/press")
            self.end(r, c)

        self.__player_enter = None  # (row, column)
        self.__player_state = 0     # 1 for up 0 for down
        self.__limit_high = 0  # for back to original height
        self.__is_enter = False  # avoid continuous enter

        canvas_reduction(self.c, self.cs, self.controler.music_player,
                         "select_player_number.png", "effect\\select_player_number.mp3")

        w, h = self.cs
        interval = 15
        padding = 25

        for row in range(2):
            # for row ---> 0
            #         ---> 1
            for column in range(2):
                # for column | |
                #            | |
                #            v v
                #            0 1
                player_number = self.calculate_player_number(
                    row, column)  # one player --> 1
                # create frame
                self.c.create_image(w/4 * (2*column+1), h/4 * (2*row+1),
                                    image=tk_image("frame.png", int(
                                        w/2-30), int(h/2-30), dirpath="images\\effect\\select_player_number"),
                                    tags=("player", f"player-frame{row}_{column}", f"player-whole{row}_{column}", f"{row}{column}"))
                # create person
                for person in range(4):
                    base_w = w/4 * (2*column+1) - int(w/2-30) / 2
                    base_h = h/4 * (2*row+1) + int(h/2-30) / 2
                    span = int((int(w/2-30) - 3 * interval - 2 * padding) / 4)
                    self.c.create_image(base_w+padding+(span+interval)*person, base_h-5, anchor="sw",
                                        image=tk_image("player.png", span, int(
                                            (h/2-30)/2), dirpath="images\\effect\\select_player_number"),
                                        tags=(
                                            "player", f"player-person{row}_{column}_{person}", f"player-whole{row}_{column}", f"{row}{column}")
                                        )
                    text = f"{person+1}p" if person + \
                        1 <= player_number else "com"
                    self.c.create_text(
                        base_w+padding+(span+interval)*person+span/2, base_h-5-int(
                            (h/2-30)/8), anchor="s", text=text, font=font_get(
                                font_span("com", int(span/3), upper_bound=int(
                                    (h/2-30)/8))
                        ), fill=self.__class__.color_for_player[text], tags=("player", f"player-person{row}_{column}_{person}", f"player-whole{row}_{column}", f"{row}{column}"))

                self.c.create_text(w/4 * (2*column+1), h /
                                   4 * (2*row+1) - int(h/2-30) / 4,
                                   text=f"{player_number} " +
                                   ("Player" if player_number == 1 else "Players"),
                                   font=font_get(72), fill=self.__class__.color_for_player[f'{player_number}p'],
                                   tags=("player", f"player-title{row}_{column}_{person}", f"player-whole{row}_{column}", f"{row}{column}"))

                self.c.tag_bind(
                    f"player-whole{row}_{column}", "<Button-1>", lambda e, r=row, c=column: press(r, c))

    def end(self, r, c):
        player_number = self.calculate_player_number(r, c)
        self.controler.user_select_player_number = player_number
        for row in range(2):
            for column in range(2):
                if (r == row) and (c == column):
                    continue
                self.c.delete(f"player-whole{row}_{column}")
                self.c.update()
                time.sleep(0.5)

        if player_number > 1:
            canvas_reduction(
                self.c, self.cs, self.controler.music_player, music="effect\\home.mp3")
            self.c.create_image(self.cs[0]/2, self.cs[1]/2, image=tk_image(
                "error_icon.png", int(self.cs[1]/2)
            ))
            self.c.create_text(self.cs[0]/2, 20, anchor="n", text="Not Support Yet\n(Press Game Menu To Go Back To Home)", justify="center",
                               font=font_get(30), fill="#ff6b87")
        else:
            self.controler.effect_enter("select_game_mode")

    def loop(self):
        if not self.c.find_withtag("player"):
            return

        is_enter, objs = self.detect()

        if is_enter:
            w, h = self.cs
            if not self.__is_enter:
                tag = self.c.gettags(objs[1])[-1]
                tag = tag if tag != "current" else self.c.gettags(objs[1])[-2]
                play_sound("effect/select_player_number/enter")
                self.__player_enter = [int(info)
                                       for info in tag]
                self.__is_enter = True
                self.__limit_high = h/4 * \
                    (2*self.__player_enter[0]+1) + int(h/2-30) / 2 - 5
        else:
            if self.__limit_high:
                r, c = self.__player_enter
                if self.c.coords(f"player-person{r}_{c}_0")[1] <= self.__limit_high - 1:
                    for i in range(4):
                        self.c.move(
                            f"player-person{r}_{c}_{i}", 0, 30)
                self.__limit_high = 0
                self.__is_enter = False
                self.__player_enter = None
                self.__player_state = 0

        if (t := time.time()) - self.timer[0] >= 0.4:

            if (s := self.__player_enter) is not None:
                for i in range(4):
                    self.c.move(f"player-person{s[0]}_{s[1]}_{i}",
                                0, 30 if self.__player_state else -30)
                self.__player_state = int(not self.__player_state)

            self.timer[0] = t
