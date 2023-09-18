from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, measure, font_span
from Tkinter_template.Assets.soundeffect import play_sound
import random
import time


class Effect:
    def __init__(self, app) -> None:
        self.app = app
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

    def __draw_progress(self, middle_w, height, length, proportion):
        # done
        proportion /= 100
        self.c.create_line(middle_w-length/2, height,
                           middle_w-length/2+length*proportion, height,
                           width=40, fill="blue", tags=("record", "record-done", "record-progress", f"record-whole1"))
        # not yet
        self.c.create_line(middle_w-length/2+length*proportion, height,
                           middle_w+length/2, height,
                           width=40, fill="silver", tags=("record", "record-notyet", "record-progress", f"record-whole1"))
        # percent
        self.c.create_text(middle_w+length/2 + 20, height, text=f"{int(proportion*100)}%", anchor="w",
                           font=font_get(30), fill="blue" if int(proportion*100) != 0 else "silver", tags=("record", "record-percent", "record-progress", f"record-whole1"))

    def start(self):
        self.__record_enter = None
        self.__record_state = 0
        self.__proportion = 0

        def enter(i, limit):
            play_sound("record/enter_frame")
            self.__record_enter = i
            self.__limit = limit

        def leave(i):
            self.__record_enter = None
            self.__record_state = 0
            if self.c.coords(f"record-image{i}")[1] <= self.__limit - 1:
                self.c.move(f"record-image{i}", 0, 60)
            if i == 1:
                self.__proportion = 0
                self.c.delete("record-progress")
                self.__draw_progress(
                    self.__middle_w, self.__height, self.__progress_length, self.__proportion)

        def press(i):
            play_sound("record/press_frame")
            self.end(i)
        # color = {
        #     "1p": "red",
        #     "2p": "green",
        #     "3p": "blue",
        #     "4p": "gold",
        #     "com": "black"
        # }
        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "record.png", "record.mp3")

        w, h = self.cs
        image_name = ['new.png', 'record.png']
        for i in range(2):
            self.c.create_image(w/4 * (2*i+1), h / 2,
                                image=tk_image("frame.png", int(
                                    w/2-30), h, dirpath="images\\system"),
                                tags=("record", f"record-frame{i}", f"record-whole{i}"))
            self.c.create_image(w/4 * (2*i+1), h / 8,
                                image=tk_image(image_name[i], int(
                                    w/4-30), int(h/6), dirpath="images\\effect\\text"),
                                tags=("record", f"record-text{i}", f"record-whole{i}"))
            self.c.create_image(w/4 * (2*i+1), h / 2,
                                image=tk_image(image_name[i],  height=int(
                                    h/4), dirpath="images\\effect\\icon"),
                                tags=("record", f"record-image{i}", f"record-whole{i}"))
            if i == 0:
                # new
                pass
            else:
                # record
                for _ in range(10):
                    if int(h/4) < _ * 100:
                        self.__progress_length = _ * 100
                        break
                self.__middle_w = w/4 * (2*i+1)

                self.__height = h / 2 + h / 8 + 80
                self.__draw_progress(
                    self.__middle_w, self.__height, self.__progress_length, self.__proportion)

            self.c.tag_bind(f"record-whole{i}",
                            "<Enter>", lambda e, i=i, limit=h / 2: enter(i, limit))
            self.c.tag_bind(f"record-whole{i}",
                            "<Leave>", lambda e, i=i: leave(i))
            self.c.tag_bind(f"record-whole{i}",
                            "<Button-1>", lambda e, i=i: press(i))
        self.record_timer = time.time()

    def end(self, i):
        mode = i
        # delete not select
        time.sleep(0.5)
        self.c.delete(f"record-whole1")
        self.c.update()
        time.sleep(0.5)

        if mode == 0:
            # new
            self.app.player.start()
        else:
            # record
            pass

    def loop(self):
        if not self.c.find_withtag("record"):
            return
        if (t := time.time()) - self.record_timer >= 0.4:
            if (s := self.__record_enter) is not None:
                self.c.move(f"record-image{s}",
                            0, 60 if self.__record_state else -60)
                self.__record_state = int(not self.__record_state)
            if s == 1:
                self.__proportion += random.randint(4, 9)
                if self.__proportion > 100:
                    self.__proportion -= 100
                self.c.delete("record-progress")
                self.__draw_progress(
                    self.__middle_w, self.__height, self.__progress_length, self.__proportion)
            self.record_timer = t
