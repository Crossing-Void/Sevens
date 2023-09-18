from modules import decoration
from modules import effect
from modules import card
from modules import initialize
from Tkinter_template.Assets.project_management import create_menu
from Tkinter_template.base import Interface
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
from Tkinter_template.Assets.music import Music
import time

Interface.rate = 1.0


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)
        self.dashboard['height'] = int(self.dashboard['height']) - 20
        self.dashboard_side = int(self.dashboard['width']), int(
            self.dashboard['height'])
        self.canvas['height'] = int(self.canvas['height']) - 20
        self.canvas_side = int(self.canvas['width']), int(
            self.canvas['height'])
        initialize.check_path()
        initialize.check_files(int(self.canvas_side[1]/3))
        self.Musics = Music()
        # -------------------------
        self.Decorations = decoration.Decoration(self)
        self.Cards = card.Card(self)
        self.Effects = effect.Effect(self)
        # -------------------------

        self.__buile_menu()

        self.Effects.main_start()

    def __buile_menu(self):
        menubar_game = create_menu(self.top_menu)
        self.top_menu.add_cascade(menu=menubar_game, label="Game")
        self.top_menu.add_command(
            label="Main", command=self.Effects.main_start)


if __name__ == "__main__":
    main = Main("Sevens", "favicon.ico", False)

    while True:
        try:
            main.canvas.update()
            main.Musics.judge()
            main.Effects.main_start_loop()
            main.Effects.player_loop()
            time.sleep(0.02)
        except:
            1 / 0
