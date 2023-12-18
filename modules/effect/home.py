from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.font import font_get, measure
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from modules.effect.base import Base
import time

img_path = "images\\effect\\home"
img_path2 = "images\\effect\\logo"


class Effect(Base):
    def __init__(self, main, controler, timer_number=1):
        super().__init__(main, controler, timer_number)
        self.c = self.main.canvas
        self.cs = self.main.canvas_side

        self.font_size = 72

    def start(self):
        def enter(e):
            self.__enter_in_text = True
            play_sound("effect/home/enter")
            self.c.itemconfig("home-text", fill="gold")

        def leave(e):
            self.__enter_in_text = False
            self.c.itemconfig("home-text", fill="black")

        def press(e):
            play_sound("effect/home/press")
            self.end()

        self.__enter_in_text = False
        canvas_reduction(self.c, self.cs, self.controler.music_player,
                         "home.png", "effect\\home.mp3")

        # create title image src
        for i in range(10):
            tk_image(
                f"logo.png",  height=int(self.cs[1]/(3-i*0.2)), dirpath=img_path2
            )

        # animate
        args = {
            "Clubs": (180, 179),
            "Diamonds": (179, 164),
            "Hearts": (164, 149),
            "Spades": (149, 134)
        }
        # revise
        img = tk_image(
            f"Seven of Clubs 180.png",  dirpath=img_path, get_object_only=True)
        revise = img.width

        count = 0
        for key, value in args.items():
            for angle in range(*value, -1):
                self.c.delete(f"home-card-{key}")
                self.c.create_image(self.cs[0]//2 + revise/4 * (count-1.5), self.cs[1]//2,
                                    image=tk_image(
                                    f"Seven of {key} {angle}.png",  dirpath=img_path),
                                    tags=("home", f"home-card-{key}"))
                self.c.update()
                time.sleep(0.04)
            time.sleep(0.2)
            count += 1

        # title
        self.c.create_image(self.cs[0]//2, self.cs[1]//6,
                            image=tk_image(
            f"logo.png",  height=int(self.cs[1]/4), dirpath=img_path2),
            tags=("home", "home-title"))

        # press to start

        self.c.create_text(self.cs[0]//2, self.cs[1]//6 * 5,
                           text="Press To Start", font=font_get(self.font_size),
                           tags=("home", "home-text"))
        self.c.create_image(self.cs[0]//2 - measure("Press To Start", self.font_size) // 2 - 30, self.cs[1]//6 * 5,
                            anchor="e", image=tk_image(
            f"arrow_right.png",  height=self.font_size, dirpath=img_path2),
            tags=("home", "home-arrowL"))
        self.c.create_image(self.cs[0]//2 + measure("Press To Start", self.font_size) // 2 + 30, self.cs[1]//6 * 5,
                            anchor="w", image=tk_image(
            f"arrow_left.png",  height=self.font_size, dirpath=img_path2),
            tags=("home", "home-arrowR"))

        self.c.tag_bind("home-text", "<Enter>", enter)
        self.c.tag_bind("home-text", "<Leave>", leave)
        self.c.tag_bind("home-text", "<Button-1>", press)

    def end(self):

        self.c.delete("home-text")
        self.c.delete("home-arrowL")
        self.c.delete("home-arrowR")

        # animate
        args = {
            "Spades": (135, 150),
            "Hearts": (150, 165),
            "Diamonds": (165, 180),
            "Clubs": (180, 179)
        }
        # revise
        img = tk_image(
            f"Seven of Clubs 180.png",  dirpath=img_path, get_object_only=True)
        revise = img.width

        count = 3
        for key, value in args.items():
            if key == "Clubs":
                self.c.delete(f"home-card-{key}")
                self.c.update()
                time.sleep(0.1)
                continue
            for angle in range(*value):
                self.c.delete(f"home-card-{key}")
                self.c.create_image(self.cs[0]//2 + revise/4 * (count-1.5), self.cs[1]//2,
                                    image=tk_image(
                                    f"Seven of {key} {angle}.png",  dirpath=img_path),
                                    tags=("home", f"home-card-{key}"))
                self.c.update()
                time.sleep(0.01)
            self.c.move(f"home-card-{key}", -revise/4, 0)
            self.c.update()
            time.sleep(0.1)
            count -= 1
            self.c.delete(f"home-card-{key}")

        # title
        for i in range(10):
            self.c.delete("home-title")
            self.c.create_image(self.cs[0]//2, self.cs[1]//6,
                                image=tk_image(
                f"logo.png",  height=int(self.cs[1]/(3-i*0.2)), dirpath=img_path2),
                tags=("home", "home-title"))
            self.c.update()
            time.sleep(0.02)

        self.controler.effect_enter("select_record")

    def loop(self):
        if not self.c.find_withtag("home-text"):
            return

        if (t := time.time()) - self.timer[0] >= 0.8:
            if not self.__enter_in_text:
                fill = "#ff6b87" if self.c.itemcget(
                    "home-text", "fill") == "black" else "black"
                self.c.itemconfig("home-text", fill=fill)
                self.timer[0] = t

        if (t := time.time()) - self.timer[1] >= 0.2:
            if self.c.coords("home-arrowL")[0] >= self.cs[0]//2 - measure("Press To Start", self.font_size) // 2 - 31:
                self.c.move("home-arrowL", -30, 0)
            else:
                self.c.move("home-arrowL", 30, 0)
            if self.c.coords("home-arrowR")[0] <= self.cs[0]//2 + measure("Press To Start", self.font_size) // 2 + 31:
                self.c.move("home-arrowR", 30, 0)
            else:
                self.c.move("home-arrowR", -30, 0)
            self.timer[1] = t
