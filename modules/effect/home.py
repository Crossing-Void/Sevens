"""
Animate and effect of poker game
home screen
"""
from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.font import font_get, measure
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
import time


class Effect:
    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

    def start(self):
        self.__enter_in_text = False

        def enter(e):
            self.__enter_in_text = True
            play_sound("effect/enter")
            self.c.itemconfig("main-effect-start", fill="gold")

        def leave(e):
            self.__enter_in_text = False
            self.c.itemconfig("main-effect-start", fill="black")

        def press(e):
            play_sound("effect/press")
            self.end()

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

    def end(self):
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

    def loop(self):
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
