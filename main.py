from Tkinter_template.Assets.project_management import create_menu
from Tkinter_template.base import Interface
from modules import *
import time
import sys

# do not want dashboard
Interface.rate = 1.0


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)

        # ----- revise 20 pixel -----
        self.dashboard['height'] = int(self.dashboard['height']) - 20
        self.dashboard_side = int(self.dashboard['width']), int(
            self.dashboard['height'])
        self.canvas['height'] = int(self.canvas['height']) - 20
        self.canvas_side = int(self.canvas['width']), int(
            self.canvas['height'])

        # ----- initialize -----
        self.Initializers = initializer.Initializer(self)
        if not self.Initializers.check_font_ready():
            sys.exit()

        self.Initializers.check_files_for_home(int(
            self.canvas_side[1] / 3
        ))

        self.Controlers = controler.Control(self)

        # ----- menu config -----

        self.game_menu = create_menu(self.top_menu)
        self.top_menu.add_cascade(menu=self.game_menu, label="Game")
        # menubar_main.add_command(label="Home", command=self.home.start)

        # start
        self.Controlers.effect_enter("home")


if __name__ == "__main__":
    main = Main("Sevens", "favicon.ico", False)

    while True:
        try:
            main.canvas.update()
            main.Controlers.music_player.judge()
            main.Controlers.effect_loop("home")
            main.Controlers.effect_loop("select_record")
            main.Controlers.effect_loop("select_player_number")
            main.Controlers.effect_loop("select_game_mode")
            # main.player_mode.loop()

            time.sleep(0.02)
        except BaseException:
            1 / 0
