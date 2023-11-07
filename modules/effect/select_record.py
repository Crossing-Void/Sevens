from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
from modules.effect.base import Base
import random
import time


class Effect(Base):
    def __init__(self, main, controler, timer_number=1):
        super().__init__(main, controler, timer_number)
        self.c = self.main.canvas
        self.cs = self.main.canvas_side

        # decide progress bar length
        for _ in range(10):
            if int(self.cs[1]/4) < _ * 100:
                self.progress_length = _ * 100
                break

    def __draw_progress(self, proportion):
        w, h = self.cs
        middle = w / 4 * 3
        height = h / 2 + h / 8 + 80
        l = self.progress_length
        proportion /= 100
        # done
        self.c.create_line(middle-l/2, height,
                           middle-l/2+l*proportion, height,
                           width=40, fill="blue", tags=("record", "record-done", "record-progress", f"record-whole-record", "record"))
        # not yet
        self.c.create_line(middle-l/2+l*proportion, height,
                           middle+l/2, height,
                           width=40, fill="silver", tags=("record", "record-notyet", "record-progress", f"record-whole-record", "record"))
        # percent
        self.c.create_text(middle+l/2 + 20, height, text=f"{int(proportion*100)}%", anchor="w",
                           font=font_get(30), fill="blue" if int(proportion*100) != 0 else "silver", tags=("record", "record-percent", "record-progress", f"record-whole-record", "record"))

    def start(self):

        def press(type_):
            play_sound("effect/select_record/press")
            self.end(type_)

        self.__record_enter = None    # new or record
        self.__record_state = 0       # 0 or 1 stand for up or down
        self.__proportion = 0         # proportion 0 ~ 100 stand for %
        self.__is_enter = False
        canvas_reduction(self.c, self.cs, self.controler.music_player,
                         "select_record.png", "effect\\select_record.mp3")

        w, h = self.cs

        # building new
        self.c.create_image(w/4, h/2,
                            image=tk_image("frame.png", int(
                                w/2-30), h, dirpath="images\\effect\\select_record"),
                            tags=("record", f"record-frame-new", f"record-whole-new", "new"))
        self.c.create_image(w/4, h/8,
                            image=tk_image("new_title.png", int(
                                w/4-30), int(h/6), dirpath="images\\effect\\select_record"),
                            tags=("record", f"record-text-new", f"record-whole-new", "new"))
        self.c.create_image(w/4, h/2,
                            image=tk_image("new_icon.png",  height=int(
                                h/4), dirpath="images\\effect\\select_record"),
                            tags=("record", f"record-image-new", f"record-whole-new", "new"))

        self.c.tag_bind(f"record-whole-new",
                        "<Button-1>", lambda e: press("new"))

        # building record
        self.c.create_image(w/4*3, h/2,
                            image=tk_image("frame.png", int(
                                w/2-30), h, dirpath="images\\effect\\select_record"),
                            tags=("record", f"record-frame-record", f"record-whole-record", "record"))
        self.c.create_image(w/4*3, h/8,
                            image=tk_image("record_title.png", int(
                                w/4-30), int(h/6), dirpath="images\\effect\\select_record"),
                            tags=("record", f"record-text-record", f"record-whole-record", "record"))
        self.c.create_image(w/4*3, h/2,
                            image=tk_image("record_icon.png",  height=int(
                                h/4), dirpath="images\\effect\\select_record"),
                            tags=("record", f"record-image-record", f"record-whole-record", "record"))

        self.c.tag_bind(f"record-whole-record",
                        "<Button-1>", lambda e: press("record"))

        # record

        self.__draw_progress(self.__proportion)

    def end(self, type_):
        self.controler.user_select_record = type_
        time.sleep(0.5)

        if type_ == "new":
            self.c.delete(f"record-whole-record")
            self.c.update()
            time.sleep(0.5)
            self.controler.effect_enter("select_player_number")
        elif type_ == "record":
            self.c.delete(f"record-whole-new")
            self.c.update()
            time.sleep(0.5)
            canvas_reduction(
                self.c, self.cs, self.controler.music_player, music="effect\\home.mp3")
            self.c.create_image(self.cs[0]/2, self.cs[1]/2, image=tk_image(
                "error_icon.png", int(self.cs[1]/2)
            ))
            self.c.create_text(self.cs[0]/2, 20, anchor="n", text="Not Support Yet\n(Press Game Menu To Go Back To Home)", justify="center",
                               font=font_get(30), fill="#ff6b87")

    def loop(self):
        if not self.c.find_withtag("record"):
            return

        is_enter, objs = self.detect()

        def leave(type_):
            self.__record_enter = None
            self.__record_state = 0
            if self.c.coords(f"record-image-{type_}")[1] <= h/2 - 1:
                self.c.move(f"record-image-{type_}", 0, 60)
            if type_ == "record":
                self.__proportion = 0
                self.c.delete("record-progress")
                self.__draw_progress(self.__proportion)
        if is_enter:
            if not self.__is_enter:
                tag = self.c.gettags(objs[1])[-1]
                tag = tag if tag != "current" else self.c.gettags(objs[1])[-2]
                play_sound("effect/select_record/enter")
                self.__record_enter = tag
                self.__is_enter = True

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
            if (s := self.__record_enter) is not None:
                self.c.move(f"record-image-{s}",
                            0, 60 if self.__record_state else -60)
                self.__record_state = int(not self.__record_state)
            if s == "record":
                self.__proportion += random.randint(4, 9)
                if self.__proportion > 100:
                    self.__proportion -= 100
                self.c.delete("record-progress")
                self.__draw_progress(self.__proportion)
            self.timer[0] = t
