from Tkinter_template.Assets.project_management import progress_bar, new_window, making_widget
from PIL import Image
from Tkinter_template.Assets.font import font_get, check_font, set_font
import sys
import os

path = "images\\effect"


class Initializer:
    def __init__(self, app) -> None:
        self.app = app

    @progress_bar({
        "new window": False
    })
    def __generate_image(self, height):
        args = {
            "Clubs": (180, 179),
            "Diamonds": (179, 164),
            "Hearts": (164, 149),
            "Spades": (149, 134)
        }

        for key in args:
            img = Image.open(f"images\\cards\\Seven of {key}.png")
            width = int(img.width * height / img.height)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(f"images\\cards\\temp Seven of {key}.png")
        count = 0
        for key, value in args.items():
            for angle in range(*value, -1):
                img = Image.open(f"images\\cards\\temp Seven of {key}.png")
                img = img.rotate(angle, expand=True)
                img.save(os.path.join(path, "home",
                         f"Seven of {key} {angle}.png"))
                count += 1
                self.__generate_image.compelete_part(count)

        for key in args:
            os.remove(f"images\\cards\\temp Seven of {key}.png")

    def check_font_ready(self):
        def download():
            win.destroy()
            set_font()

        if not check_font():
            win = new_window("Install Font", "favicon.ico", (800, 200))
            making_widget("Label")(win, text="Install Font \"Inconsolata\"",
                                   font=font_get(30)).pack()
            making_widget("Label")(
                win, text="Because your computer does not have the required font for this game\nPress \"Download\" to begin the download",
                font=font_get(20)).pack()
            making_widget("Button")(win, text="Download",
                                    font=font_get(26), bg="#ffff80", command=download).pack(side="bottom")
            win.attributes('-topmost', 1)
            win.wait_window()

            return False
        return True

    def check_path(self):
        # for home effect dir
        if not os.path.exists(os.path.join(path, "home")):
            os.mkdir(os.path.join(path, "home"))

    def check_files(self, height: int):
        # for home effect files
        if len(os.listdir(os.path.join(path, "home"))) < 46:
            self.__files_window = new_window(
                "Prepare data", "favicon.ico")
            making_widget("Label")(self.__files_window, font=font_get(20),
                                   text="Preparing Data").grid(row=1, column=1, sticky="we")
            self.__files_canvas = making_widget("Canvas")(self.__files_window, width=300,
                                                          height=200, bg="#ffff80")
            self.__files_canvas.grid(row=2, column=1)
            self.__generate_image.add_arg({
                "total": 46,
                "size": (int(self.__files_canvas['width']),
                         int(self.__files_canvas['height'])),
                "canvas": self.__files_canvas
            })
            self.__generate_image(self, height)
            self.__files_window.destroy()
