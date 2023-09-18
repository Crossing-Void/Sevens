"""
Animate and effect of poker game
"""
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

    def main_start(self):
        self.__enter = False

        def enter(e):
            self.__enter = True
            play_sound("effect/enter")
            self.c.itemconfig("main-effect-start", fill="gold")

        def leave(e):
            self.__enter = False
            self.c.itemconfig("main-effect-start", fill="black")

        def press(e):
            play_sound("effect/press")
            self.main_press()

        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "main.png", "main.mp3")
        # animate
        args = {
            "Clubs": (180, 179),
            "Diamonds": (179, 164),
            "Hearts": (164, 149),
            "Spades": (149, 134)
        }
        count = 0
        img = tk_image(
            f"Seven of Clubs 180.png",  dirpath="images\\effect\\main", get_object_only=True)
        revise = img.width
        for key, value in args.items():
            for angle in range(*value, -1):
                self.c.delete(f"main-effect-{key}")
                self.c.create_image(self.cs[0]//2 + revise/4 * (count-1.5), self.cs[1]//2,
                                    image=tk_image(
                                    f"Seven of {key} {angle}.png",  dirpath="images\\effect\\main"),
                                    tags=("main-effect", f"main-effect-{key}"))
                self.c.update()
                time.sleep(0.04)
            time.sleep(0.2)
            count += 1

        # title
        self.c.create_image(self.cs[0]//2, self.cs[1]//6,
                            image=tk_image(
            f"logo.png",  height=int(self.cs[1]/3), dirpath="images\\effect\\title"),
            tags=("main-effect", "main-effect-title"))

        # press to start
        self.__font_size = 72
        self.c.create_text(self.cs[0]//2, self.cs[1]//6 * 5,
                           text="Press To Start", font=font_get(72),
                           tags=("main-effect", "main-effect-start"))
        self.c.create_image(self.cs[0]//2 - measure("Press To Start", self.__font_size) // 2 - 30, self.cs[1]//6 * 5,
                            anchor="e",
                            image=tk_image(
            f"play.png",  height=self.__font_size, dirpath="images\\system"),
            tags=("main-effect", "main-effect-startimage1"))
        self.c.create_image(self.cs[0]//2 + measure("Press To Start", self.__font_size) // 2 + 30, self.cs[1]//6 * 5,
                            anchor="w",
                            image=tk_image(
            f"play_left.png",  height=self.__font_size, dirpath="images\\system"),
            tags=("main-effect", "main-effect-startimage2"))

        self.c.tag_bind("main-effect-start", "<Enter>", enter)
        self.c.tag_bind("main-effect-start", "<Leave>", leave)
        self.c.tag_bind("main-effect-start", "<Button-1>", press)

        self.main_start_timer = time.time()
        self.main_start_timer2 = time.time()

    def main_press(self):
        self.c.delete("main-effect-start")
        self.c.delete("main-effect-startimage1")
        self.c.delete("main-effect-startimage2")
        # animate
        args = {
            "Spades": (135, 150),
            "Hearts": (150, 165),
            "Diamonds": (165, 180),
            "Clubs": (180, 179)
        }
        count = 3
        img = tk_image(
            f"Seven of Clubs 180.png",  dirpath="images\\effect\\main", get_object_only=True)
        revise = img.width
        for key, value in args.items():
            if key == "Clubs":
                self.c.delete(f"main-effect-{key}")
                self.c.update()
                time.sleep(0.1)
                continue
            for angle in range(*value):
                self.c.delete(f"main-effect-{key}")
                self.c.create_image(self.cs[0]//2 + revise/4 * (count-1.5), self.cs[1]//2,
                                    image=tk_image(
                                    f"Seven of {key} {angle}.png",  dirpath="images\\effect\\main"),
                                    tags=("main-effect", f"main-effect-{key}"))
                self.c.update()
                time.sleep(0.01)
            self.c.move(f"main-effect-{key}", -revise/4, 0)
            self.c.update()
            time.sleep(0.1)
            count -= 1
            self.c.delete(f"main-effect-{key}")

        # title
        for i in range(10):
            self.c.delete("main-effect-title")
            self.c.create_image(self.cs[0]//2, self.cs[1]//6,
                                image=tk_image(
                f"logo.png",  height=int(self.cs[1]/(3-i*0.2)), dirpath="images\\effect\\title"),
                tags=("main-effect", "main-effect-title"))
            self.c.update()
            time.sleep(0.01)
        self.select_player()

    def select_player(self):
        self.__player_enter = None
        self.__player_state = 0

        def enter(r, c, limit):
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
            pass
        color = {
            "1p": "red",
            "2p": "green",
            "3p": "blue",
            "4p": "gold",
            "com": "black"
        }
        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "player.png", "player_select.mp3")

        w, h = self.cs
        interval = 15
        padding = 25
        for row in range(2):
            for column in range(2):
                p = row*2 + column+1
                self.c.create_image(w/4 * (2*column+1), h/4 * (2*row+1),
                                    image=tk_image("frame.png", int(
                                        w/2-30), int(h/2-30), dirpath="images\\system"),
                                    tags=("player", f"player-frame{row}_{column}"))
                for person in range(4):
                    base_w = w/4 * (2*column+1) - int(w/2-30) / 2
                    base_h = h/4 * (2*row+1) + int(h/2-30) / 2
                    span = int((int(w/2-30) - 3 * interval - 2 * padding) / 4)
                    self.c.create_image(base_w+padding+(span+interval)*person, base_h-5, anchor="sw",
                                        image=tk_image("person.png", span, int(
                                            (h/2-30)/2), dirpath="images\\system"),
                                        tags=(
                                            "player", f"player-person{row}_{column}_{person}")
                                        )
                    text = f"{person+1}p" if person+1 <= p else "com"
                    self.c.create_text(
                        base_w+padding+(span+interval)*person+span/2, base_h-5-int(
                            (h/2-30)/8), anchor="s", text=text, font=font_get(
                                font_span("com", int(span/3), upper_bound=int(
                                    (h/2-30)/8))
                        ), fill=color[text], tags=("player", f"player-person{row}_{column}_{person}"))
                self.c.create_text(w/4 * (2*column+1), h /
                                   4 * (2*row+1) - int(h/2-30) / 4,
                                   text=f"{p} " +
                                   ("Player" if p == 1 else "Players"),
                                   font=font_get(self.__font_size), fill="#ff6b87")
                self.c.tag_bind(
                    f"player-frame{row}_{column}", "<Enter>", lambda e, r=row, c=column,
                    limit=base_h-5: enter(r, c, limit))
                self.c.tag_bind(
                    f"player-frame{row}_{column}", "<Leave>", lambda e, r=row, c=column: leave(r, c))
                self.c.tag_bind(
                    f"player-frame{row}_{column}", "<Button-1>", lambda e, r=row, c=column: press(r, c))

        self.player_timer = time.time()

    def main_start_loop(self):
        if not self.c.find_withtag("main-effect-start"):
            return
        if (t := time.time()) - self.main_start_timer >= 0.8:
            if not self.__enter:
                fill = "#ff6b87" if self.c.itemcget(
                    "main-effect-start", "fill") == "black" else "black"
                self.c.itemconfig("main-effect-start", fill=fill)
                self.main_start_timer = t
        if (t := time.time()) - self.main_start_timer2 >= 0.2:
            if self.c.coords("main-effect-startimage1")[0] >= self.cs[0]//2 - measure("Press To Start", self.__font_size) // 2 - 31:
                self.c.move("main-effect-startimage1", -30, 0)
            else:
                self.c.move("main-effect-startimage1", 30, 0)
            if self.c.coords("main-effect-startimage2")[0] <= self.cs[0]//2 + measure("Press To Start", self.__font_size) // 2 + 31:
                self.c.move("main-effect-startimage2", 30, 0)
            else:
                self.c.move("main-effect-startimage2", -30, 0)
            self.main_start_timer2 = t

    def player_loop(self):
        if not self.c.find_withtag("player"):
            return
        if (t := time.time()) - self.player_timer >= 0.4:

            if (s := self.__player_enter) is not None:
                for i in range(4):
                    self.c.move(f"player-person{s[0]}_{s[1]}_{i}",
                                0, 30 if self.__player_state else -30)
                self.__player_state = int(not self.__player_state)

            self.player_timer = t
