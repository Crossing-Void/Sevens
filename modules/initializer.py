from Tkinter_template.Assets.project_management import progress_bar, new_window, making_widget
from Tkinter_template.Assets.font import font_get, check_font, set_font
from PIL import Image
import os

path = "images\\effect\\home"


class Initializer:
    def __init__(self, app) -> None:
        self.app = app

    @progress_bar({
        "new window": False
    })
    def __generate_image(self, height):
        # ----- generate rotate image -----
        args = {
            "Clubs": (180, 179),
            "Diamonds": (179, 164),
            "Hearts": (164, 149),
            "Spades": (149, 134)
        }
        # resize and save to temp file
        for key in args:
            img = Image.open(f"images\\cards\\Seven of {key}.png")
            width = int(img.width * height / img.height)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(f"images\\cards\\temp Seven of {key}.png")

        # rotate
        count = 0
        for key, value in args.items():
            for angle in range(*value, -1):
                img = Image.open(f"images\\cards\\temp Seven of {key}.png")
                img = img.rotate(angle, expand=True)
                img.save(os.path.join(path, f"Seven of {key} {angle}.png"))
                count += 1
                self.__generate_image.compelete_part(count)
        # delete copy card
        for key in args:
            os.remove(f"images\\cards\\temp Seven of {key}.png")

    def check_font_ready(self):
        # if font exists return True else into download and exit
        def download():
            win.destroy()
            set_font()

        if not check_font():
            win = new_window("Install Font", "favicon.ico", (800, 200))
            making_widget("Label")(win, text="Install Font \"Inconsolata\"",
                                   font=font_get(30, True)).pack(pady=10)
            making_widget("Label")(
                win, text="Because your computer does not have the required font for this game\nPress \"Download\" to begin the download",
                font=font_get(20)).pack(pady=5)
            making_widget("Button")(win, text="Download",
                                    font=font_get(26), bg="#ffff80", command=download).pack(side="bottom", pady=10)
            win.attributes('-topmost', 1)
            win.wait_window()

            return False
        return True

    def check_files_for_home(self, height: int):
        # for home effect dir
        if not os.path.exists(path):
            os.mkdir(path)
        # if cards number little than 46 then to prepare data
        if len(os.listdir(path)) < 46:
            win = new_window("Prepare data", "favicon.ico")
            making_widget("Label")(win, font=font_get(20, True),
                                   text="Preparing Data").grid(row=1, column=1, sticky="we")
            canvas = making_widget("Canvas")(
                win, width=300, height=200, bg="#ffff80")
            canvas.grid(row=2, column=1)
            self.__generate_image.add_arg({
                "total": 46,
                "size": (int(canvas['width']),
                         int(canvas['height'])),
                "canvas": canvas
            })
            self.__generate_image(self, height)
            win.destroy()
