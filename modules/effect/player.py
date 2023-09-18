from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, measure, font_span
from Tkinter_template.Assets.soundeffect import play_sound
import time


class Effect:
    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

    def start(self):
        self.__player_enter = None
        self.__player_state = 0

        def enter(r, c, limit):
            play_sound("player/enter_frame")
            self.__player_enter = (r, c)
            self.__limit = limit

        def leave(r, c):
            self.__player_enter = None
            self.__player_state = 0
            if self.c.coords(f"player-person{r}_{c}_0")[1] <= self.__limit - 1:
                for i in range(4):
                    self.c.move(
                        f"player-person{r}_{c}_{i}", 0, 30)

        def press(r, c):
            play_sound("player/press_frame")
            self.end(r, c)
        color = {
            "1p": "red",
            "2p": "green",
            "3p": "blue",
            "4p": "gold",
            "com": "black"
        }
        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "player.png", "player.mp3")

        w, h = self.cs
        interval = 15
        padding = 25
        for row in range(2):
            for column in range(2):
                p = row*2 + column+1
                self.c.create_image(w/4 * (2*column+1), h/4 * (2*row+1),
                                    image=tk_image("frame.png", int(
                                        w/2-30), int(h/2-30), dirpath="images\\system"),
                                    tags=("player", f"player-frame{row}_{column}", f"player-whole{row}_{column}"))
                for person in range(4):
                    base_w = w/4 * (2*column+1) - int(w/2-30) / 2
                    base_h = h/4 * (2*row+1) + int(h/2-30) / 2
                    span = int((int(w/2-30) - 3 * interval - 2 * padding) / 4)
                    self.c.create_image(base_w+padding+(span+interval)*person, base_h-5, anchor="sw",
                                        image=tk_image("person.png", span, int(
                                            (h/2-30)/2), dirpath="images\\system"),
                                        tags=(
                                            "player", f"player-person{row}_{column}_{person}", f"player-whole{row}_{column}")
                                        )
                    text = f"{person+1}p" if person+1 <= p else "com"
                    self.c.create_text(
                        base_w+padding+(span+interval)*person+span/2, base_h-5-int(
                            (h/2-30)/8), anchor="s", text=text, font=font_get(
                                font_span("com", int(span/3), upper_bound=int(
                                    (h/2-30)/8))
                        ), fill=color[text], tags=("player", f"player-person{row}_{column}_{person}", f"player-whole{row}_{column}"))
                self.c.create_text(w/4 * (2*column+1), h /
                                   4 * (2*row+1) - int(h/2-30) / 4,
                                   text=f"{p} " +
                                   ("Player" if p == 1 else "Players"),
                                   font=font_get(72), fill=color[f'{p}p'],
                                   tags=("player", f"player-title{row}_{column}_{person}", f"player-whole{row}_{column}"))
                self.c.tag_bind(
                    f"player-whole{row}_{column}", "<Enter>", lambda e, r=row, c=column,
                    limit=base_h-5: enter(r, c, limit))
                self.c.tag_bind(
                    f"player-whole{row}_{column}", "<Leave>", lambda e, r=row, c=column: leave(r, c))
                self.c.tag_bind(
                    f"player-whole{row}_{column}", "<Button-1>", lambda e, r=row, c=column: press(r, c))

        self.player_timer = time.time()

    def end(self, r, c):
        # delete not select
        player_number = r*2 + c+1
        for row in range(2):
            for column in range(2):
                if (r == row) and (c == column):
                    continue
                self.c.delete(f"player-whole{row}_{column}")
                self.c.update()
                time.sleep(0.5)

    def loop(self):
        if not self.c.find_withtag("player"):
            return

        if (t := time.time()) - self.player_timer >= 0.4:

            if (s := self.__player_enter) is not None:
                for i in range(4):
                    self.c.move(f"player-person{s[0]}_{s[1]}_{i}",
                                0, 30 if self.__player_state else -30)
                self.__player_state = int(not self.__player_state)

            self.player_timer = t
