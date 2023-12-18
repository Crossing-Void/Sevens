from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
from modules.effect.base import Base
import random
import time

img_path = "images\\effect\\select_record"

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

    def __draw_progressbar(self, proportion):
        """
        proportion is %
        """
        w, h = self.cs
        middle = w / 4 * 3
        height = h / 2 + h / 8 + 80
        l = self.progress_length
        proportion /= 100
        # done
        self.c.create_line(middle-l/2, height,
                           middle-l/2+l*proportion, height,
                           width=40, fill="blue", tags=("record", "record-record", "record-record-progressbar"))
        # not yet
        self.c.create_line(middle-l/2+l*proportion, height,
                           middle+l/2, height,
                           width=40, fill="silver", tags=("record", "record-record", "record-record-progressbar"))
        # percent
        self.c.create_text(middle+l/2 + 20, height, text=f"{int(proportion*100)}%", anchor="w",
                           font=font_get(30), fill="blue" if int(proportion*100) != 0 else "silver", 
                           tags=("record", "record-record", "record-record-progressbar"))

    def start(self):
        def press(type_):
            play_sound("effect/select_record/press")
            self.end(type_)

        self.__enter_area = None    # new or record
        self.__state = 0            # 0 or 1 stand for up or down
        self.__proportion = 0       # proportion 0 ~ 100 stand for %
        
        canvas_reduction(self.c, self.cs, self.controler.music_player,
                         "select_record.png", "effect\\select_record.mp3")

        w, h = self.cs

        # building new
        self.c.create_image(w/4, h/2,
                            image=tk_image("frame.png", int(
                                w/2-30), h, dirpath=img_path),
                            tags=("record", f"record-new"))
        self.c.create_image(w/4, h/8,
                            image=tk_image("new_title.png", int(
                                w/4-30), int(h/6), dirpath=img_path),
                            tags=("record", f"record-new"))
        self.c.create_image(w/4, h/2,
                            image=tk_image("new_icon.png",  height=int(
                                h/4), dirpath=img_path),
                            tags=("record", f"record-new", f"record-new-img"))

        self.c.tag_bind(f"record-new",
                        "<Button-1>", lambda e: press("new"))

        # building record
        self.c.create_image(w/4*3, h/2,
                            image=tk_image("frame.png", int(
                                w/2-30), h, dirpath=img_path),
                            tags=("record", f"record-record"))
        self.c.create_image(w/4*3, h/8,
                            image=tk_image("record_title.png", int(
                                w/4-30), int(h/6), dirpath=img_path),
                            tags=("record", f"record-record"))
        self.c.create_image(w/4*3, h/2,
                            image=tk_image("record_icon.png",  height=int(
                                h/4), dirpath=img_path),
                            tags=("record", f"record-record", "record-record-img"))

        self.c.tag_bind(f"record-record",
                        "<Button-1>", lambda e: press("record"))

        # record

        self.__draw_progressbar(self.__proportion)

    def end(self, type_):
        self.controler.user_select_record = type_
        time.sleep(0.5)
        self.c.delete("record-new")
        self.c.delete("record-record")
        self.c.update()
        time.sleep(0.5)

        if type_ == "new":
            self.controler.effect_enter("select_player_number")
        
        elif type_ == "record":
            # need to build where it should going 
            # put error in there
            canvas_reduction(
                self.c, self.cs, self.controler.music_player, music="effect\\home.mp3")
            self.c.create_image(self.cs[0]/2, self.cs[1]/2, image=tk_image(
                "error_icon.png", int(self.cs[1]/2)
            ))
            self.c.create_text(self.cs[0]/2, 20, anchor="n", text="Not Support Yet\n(Press Game Menu To Go Back To Home)", justify="center",
                               font=font_get(30), fill="#ff6b87")
            
            
            

    def loop(self):
        def leave_config(genre):
            if self.c.coords(f"record-{genre}-img")[1] <= self.cs[1]/2 - 1:
                self.c.move(f"record-{genre}-img", 0, 60)
            if genre == "record":
                self.__proportion = 0
                self.c.delete("record-record-progressbar")
                self.__draw_progressbar(self.__proportion)
            self.__enter_area = None
            self.__state = 0
        
        if not self.c.find_withtag("record"):
            return
        
        result = self.detect()
        
        if result:
            if self.__enter_area != result:
                play_sound("effect/select_record/enter")
                if self.__enter_area:
                    leave_config(self.__enter_area)
            self.__enter_area = result
        else:
            if self.__enter_area:
                leave_config(self.__enter_area)
                
                

        if (t := time.time()) - self.timer[0] >= 0.4:
            if (s := self.__enter_area) is not None:
                self.c.move(f"record-{s}-img",
                            0, 60 if self.__state else -60)
                self.__state = int(not self.__state)
            if s == "record":
                self.__proportion += random.randint(4, 9)
                if self.__proportion > 100:
                    self.__proportion -= 100
                self.c.delete("record-record-progressbar")
                self.__draw_progressbar(self.__proportion)
            self.timer[0] = t
