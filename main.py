from modules import decoration
from Tkinter_template.base import Interface
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
import time

Interface.rate = 1.0


class Main(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        super().__init__(title, icon, default_menu)
        # -------------------------
        self.Decorations = decoration.Decoration(self)
        # -------------------------


if __name__ == "__main__":
    main = Main("Sevens", "favicon.ico")

    main.canvas.create_image(main.canvas_side[0]//2, main.canvas_side[1]//2,
                             image=tk_image("Ace of Spades.png", 100,
                                            dirpath="images\\cards")
                             )
    while True:
        main.canvas.update()
        time.sleep(0.02)
