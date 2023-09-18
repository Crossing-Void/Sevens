from Tkinter_template.Assets.project_management import create_menu
from Tkinter_template.base import Interface
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
from Tkinter_template.Assets.music import Music
from modules.effect import *
from modules import initialize
from modules import *
import time

Interface.rate = 1.0


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)
        # ----- revise -----
        self.dashboard['height'] = int(self.dashboard['height']) - 20
        self.dashboard_side = int(self.dashboard['width']), int(
            self.dashboard['height'])
        self.canvas['height'] = int(self.canvas['height']) - 20
        self.canvas_side = int(self.canvas['width']), int(
            self.canvas['height'])
        # ----- revise -----
        # ----- check -----
        initialize.check_path()
        initialize.check_files(int(self.canvas_side[1]/3))
        # ----- check -----

        # -------------------------
        self.Musics = Music()
        self.Decorations = decoration.Decoration(self)
        self.Cards = card.Card(self)
        self.Soundeffects = soundeffect.Soundeffect(self)

        # effect
        self.home = home.Effect(self)
        # -------------------------

        self.__buile_menu()

        # main start
        self.home.start()

    def __buile_menu(self):
        menubar_main = create_menu(self.top_menu)
        self.top_menu.add_cascade(menu=menubar_main, label="Game")
        menubar_main.add_command(label="Home", command=self.home.start)


if __name__ == "__main__":
    main = Main("Sevens", "favicon.ico", False)

    while True:
        try:
            main.canvas.update()
            main.Musics.judge()
            main.home.loop()
            time.sleep(0.02)
        except:
            1 / 0
