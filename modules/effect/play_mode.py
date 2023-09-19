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

    def start(self):
        # self.__player-mode_enter = None
        # self.__player-mode_state = 0
        # self.__proportion = 0

        # def enter(i, limit):
        #     play_sound("player-mode/enter_frame")
        #     self.__player-mode_enter = i
        #     self.__limit = limit

        # def leave(i):
        #     self.__player-mode_enter = None
        #     self.__player-mode_state = 0
        #     if self.c.coords(f"player-mode-image{i}")[1] <= self.__limit - 1:
        #         self.c.move(f"player-mode-image{i}", 0, 60)
        #     if i == 1:
        #         self.__proportion = 0
        #         self.c.delete("player-mode-progress")
        #         self.__draw_progress(
        #             self.__middle_w, self.__height, self.__progress_length, self.__proportion)

        # def press(i):
        #     play_sound("player-mode/press_frame")
        #     self.end(i)
        # color = {
        #     "1p": "red",
        #     "2p": "green",
        #     "3p": "blue",
        #     "4p": "gold",
        #     "com": "black"
        # }
        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "play_mode.png", "play_mode.mp3")

        w, h = self.cs
        image_name = ['bankruptcy.png', 'round.png']
        for i in range(2):
            self.c.create_image(w/4 * (2*i+1), h / 4,
                                image=tk_image("frame.png", int(
                                    w/2-30), int(h/2), dirpath="images\\system"),
                                tags=("player-mode", f"player-mode-frame{i}", f"player-mode-whole{i}"))
            self.c.create_image(w/4 * (2*i+1), h / 16,
                                image=tk_image(image_name[i], int(
                                    w/4-30), int(h/12), dirpath="images\\effect\\text"),
                                tags=("player-mode", f"player-mode-text{i}", f"player-mode-whole{i}"))
            self.c.create_image(w/4 * (2*i+1), h / 16 * 4,
                                image=tk_image(image_name[i],  height=int(
                                    h/5), dirpath="images\\effect\\icon"),
                                tags=("player-mode", f"player-mode-image{i}", f"player-mode-whole{i}"))
            if i == 0:
                # bankrupt
                self.c.create_text(w/4 * (2*i+1), h / 16 * 4 + int(h/5) / 2, text="Never End Until\nSomeone Bankrupt",
                                   justify="center", fill="#ff6b87", font=font_get(int(h/20*3/4)), anchor="n",
                                   tag=("player-mode", f"player-mode-image{i}", f"player-mode-whole{i}"))
            else:
                # round
                self.c.create_text(w/4 * (2*i+1), h / 16 * 4 + int(h/5) / 2, text="After A Set Number Of Rounds\nMost Money Wins",
                                   justify="center", fill="#ff6b87", font=font_get(int(h/20*3/4)), anchor="n",
                                   tag=("player-mode", f"player-mode-image{i}", f"player-mode-whole{i}"))

        #     self.c.tag_bind(f"player-mode-whole{i}",
        #                     "<Enter>", lambda e, i=i, limit=h / 2: enter(i, limit))
        #     self.c.tag_bind(f"player-mode-whole{i}",
        #                     "<Leave>", lambda e, i=i: leave(i))
        #     self.c.tag_bind(f"player-mode-whole{i}",
        #                     "<Button-1>", lambda e, i=i: press(i))
        # self.player-mode_timer = time.time()

    # def end(self, i):
    #     mode = i
    #     self.app.mode = i
    #     # delete not select
    #     time.sleep(0.5)
    #     self.c.delete(f"player-mode-whole1")
    #     self.c.update()
    #     time.sleep(0.5)

    #     if mode == 0:
    #         # new
    #         # to game
    #     self.app.controler.initialize()
    #         self.app.player.start()
    #     else:
    #         # player-mode
    #         pass

    # def loop(self):
    #     if not self.c.find_withtag("player-mode"):
    #         return
    #     if (t := time.time()) - self.player-mode_timer >= 0.4:
    #         if (s := self.__player-mode_enter) is not None:
    #             self.c.move(f"player-mode-image{s}",
    #                         0, 60 if self.__player-mode_state else -60)
    #             self.__player-mode_state = int(not self.__player-mode_state)
    #         if s == 1:
    #             self.__proportion += random.randint(4, 9)
    #             if self.__proportion > 100:
    #                 self.__proportion -= 100
    #             self.c.delete("player-mode-progress")
    #             self.__draw_progress(
    #                 self.__middle_w, self.__height, self.__progress_length, self.__proportion)
    #         self.player-mode_timer = t
