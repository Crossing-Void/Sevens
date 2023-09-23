from Tkinter_template.Assets.project_management import create_menu
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, check_font
from Tkinter_template.Assets.music import Music
from Tkinter_template.base import Interface
from modules.effect import *
from modules import *
import time
import sys

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
        self.initializer = initializer.Initializer(self)
        if not self.initializer.check_font_ready():
            sys.exit()

        self.initializer.check_path()
        self.initializer.check_files(int(self.canvas_side[1] / 3))

        # ----- check -----

        # -------------------------
        self.Musics = Music()
        self.Soundeffects = soundeffect.Soundeffect(self)

        # effect
        self.home = home.Effect(self)
        self.record = record.Effect(self)
        self.player = player.Effect(self)
        self.player_mode = play_mode.Effect(self)

        # game
        self.controler = controler.Control(self)

        # -------------------------

        self.__buile_menu()

        # home start
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
            main.player.loop()
            main.record.loop()
            main.player_mode.loop()
            time.sleep(0.02)
        except:
            1 / 0
