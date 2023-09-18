from PIL import Image
import os

path = "images\\effect"


def check_path():
    if not os.path.exists(os.path.join(path, "home")):
        os.mkdir(os.path.join(path, "home"))


def check_files(height: int):
    if len(os.listdir(os.path.join(path, "home"))) < 46:
        _generate_image(height)


def _generate_image(height):
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

    for key, value in args.items():
        for angle in range(*value, -1):
            img = Image.open(f"images\\cards\\temp Seven of {key}.png")
            img = img.rotate(angle, expand=True)
            img.save(os.path.join(path, "home", f"Seven of {key} {angle}.png"))

    for key in args:
        os.remove(f"images\\cards\\temp Seven of {key}.png")
