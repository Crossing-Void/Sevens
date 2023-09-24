from Tkinter_template.Assets.project_management import canvas_reduction
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
import random
import os


class Animation:
    def __init__(self, app, app2) -> None:
        self.app = app
        self.controler = app2
        self.c = self.app.canvas
        self.cs = self.app.canvas_side

    def round(self, round: int):
        # lenght > 1 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        def revise(e):
            self.c.unbind("<Button-1>")
            self.c.bind("<Button-1>", press)

        def press(e):
            self.c.unbind("<Button-1>")
            play_sound("game/start")
            self.app.Musics.music = os.path.join(
                "game", random.choice(os.listdir("musics\\game")))
            self.c.delete("round")

            # start
            self.controler.Chip.configure_chip()
            self.controler.Card.deal_card()
            self.controler.Card.create_table()
            self.controler.game()

        canvas_reduction(self.c, self.cs, self.app.Musics,
                         "background.png", "setup.mp3")
        # image
        width_round = tk_image("round.png", height=200,
                               dirpath="images\\game\\round", get_object_only=True).width
        width_number = tk_image(f"{round}.png", height=200,
                                dirpath="images\\game\\round", get_object_only=True).width
        middle_point = (width_round + width_number + 50) / 2
        self.c.create_image(
            self.cs[0]/2 - middle_point + width_round / 2, self.cs[1]/2, image=tk_image("round.png", height=200, dirpath="images\\game\\round"),
            tags=("round"))
        self.c.create_image(
            self.cs[0]/2 - middle_point + width_round + 50, self.cs[1]/2, image=tk_image(f"{round}.png", height=200, dirpath="images\\game\\round"), anchor='w',
            tags=("round"))

        self.c.bind("<Button-1>", revise)
