from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.font import font_get, measure
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from modules.effect.base import Base
import time


#!!!!!!!!!!!!!!!! to class args !!!!!!!!!!!!!!!!


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
            self.c.itemconfig("home-effect-start", fill="gold")

        def leave(e):
            self.__enter_in_text = False
            self.c.itemconfig("home-effect-start", fill="black")

        def press(e):
            play_sound("effect/home/press")
            self.end()

        self.__enter_in_text = False
        canvas_reduction(self.c, self.cs, self.controler.music_player,
                         "home.png", "effect\\home.mp3")

        # animate
        args = {
            "Clubs": (180, 179),
            "Diamonds": (179, 164),
            "Hearts": (164, 149),
            "Spades": (149, 134)
        }
        # revise
        img = tk_image(
            f"Seven of Clubs 180.png",  dirpath="images\\effect\\home", get_object_only=True)
        revise = img.width

        count = 0
        for key, value in args.items():
            for angle in range(*value, -1):
                self.c.delete(f"home-effect-{key}")
                self.c.create_image(self.cs[0]//2 + revise/4 * (count-1.5), self.cs[1]//2,
                                    image=tk_image(
                                    f"Seven of {key} {angle}.png",  dirpath="images\\effect\\home"),
                                    tags=("home-effect", f"home-effect-{key}"))
                self.c.update()
                time.sleep(0.04)
            time.sleep(0.2)
            count += 1

        # title
        self.c.create_image(self.cs[0]//2, self.cs[1]//6,
                            image=tk_image(
            f"logo.png",  height=int(self.cs[1]/4), dirpath="images\\effect\\logo"),
            tags=("home-effect", "home-effect-title"))

        # press to start

        self.c.create_text(self.cs[0]//2, self.cs[1]//6 * 5,
                           text="Press To Start", font=font_get(self.font_size),
                           tags=("home-effect", "home-effect-start"))
        self.c.create_image(self.cs[0]//2 - measure("Press To Start", self.font_size) // 2 - 30, self.cs[1]//6 * 5,
                            anchor="e",
                            image=tk_image(
            f"arrow_right.png",  height=self.font_size, dirpath="images\\effect\\logo"),
            tags=("home-effect", "home-effect-startimage1"))
        self.c.create_image(self.cs[0]//2 + measure("Press To Start", self.font_size) // 2 + 30, self.cs[1]//6 * 5,
                            anchor="w",
                            image=tk_image(
            f"arrow_left.png",  height=self.font_size, dirpath="images\\effect\\logo"),
            tags=("home-effect", "home-effect-startimage2"))

        self.c.tag_bind("home-effect-start", "<Enter>", enter)
        self.c.tag_bind("home-effect-start", "<Leave>", leave)
        self.c.tag_bind("home-effect-start", "<Button-1>", press)

    def end(self):

        self.c.delete("home-effect-start")
        self.c.delete("home-effect-startimage1")
        self.c.delete("home-effect-startimage2")
        # animate
        args = {
            "Spades": (135, 150),
            "Hearts": (150, 165),
            "Diamonds": (165, 180),
            "Clubs": (180, 179)
        }
        # revise
        img = tk_image(
            f"Seven of Clubs 180.png",  dirpath="images\\effect\\home", get_object_only=True)
        revise = img.width

        count = 3
        for key, value in args.items():
            if key == "Clubs":
                self.c.delete(f"home-effect-{key}")
                self.c.update()
                time.sleep(0.1)
                continue
            for angle in range(*value):
                self.c.delete(f"home-effect-{key}")
                self.c.create_image(self.cs[0]//2 + revise/4 * (count-1.5), self.cs[1]//2,
                                    image=tk_image(
                                    f"Seven of {key} {angle}.png",  dirpath="images\\effect\\home"),
                                    tags=("home-effect", f"home-effect-{key}"))
                self.c.update()
                time.sleep(0.01)
            self.c.move(f"home-effect-{key}", -revise/4, 0)
            self.c.update()
            time.sleep(0.1)
            count -= 1
            self.c.delete(f"home-effect-{key}")

        # title
        for i in range(10):
            self.c.delete("home-effect-title")
            self.c.create_image(self.cs[0]//2, self.cs[1]//6,
                                image=tk_image(
                f"logo.png",  height=int(self.cs[1]/(3-i*0.2)), dirpath="images\\effect\\logo"),
                tags=("home-effect", "home-effect-title"))
            self.c.update()
            time.sleep(0.01)

        self.controler.effect_enter("select_record")

    def loop(self):
        if not self.c.find_withtag("home-effect-start"):
            return

        if (t := time.time()) - self.timer[0] >= 0.8:
            if not self.__enter_in_text:
                fill = "#ff6b87" if self.c.itemcget(
                    "home-effect-start", "fill") == "black" else "black"
                self.c.itemconfig("home-effect-start", fill=fill)
                self.timer[0] = t

        if (t := time.time()) - self.timer[1] >= 0.2:
            if self.c.coords("home-effect-startimage1")[0] >= self.cs[0]//2 - measure("Press To Start", self.font_size) // 2 - 31:
                self.c.move("home-effect-startimage1", -30, 0)
            else:
                self.c.move("home-effect-startimage1", 30, 0)
            if self.c.coords("home-effect-startimage2")[0] <= self.cs[0]//2 + measure("Press To Start", self.font_size) // 2 + 31:
                self.c.move("home-effect-startimage2", 30, 0)
            else:
                self.c.move("home-effect-startimage2", -30, 0)
            self.timer[1] = t
