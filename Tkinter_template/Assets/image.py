'''
@version: 1.1.0
@author: CrossingVoid
@date: 2023/03/05

The image.py is mainly for image manipulations,
particularly for tk image


version 1.1.0:
  function tk_image add a new parameter `get_object_only`
  default is false, if true it return TkImage object instead
  a Tk img source.
'''
from PIL import ImageTk, Image
from dataclasses import dataclass
import os


_search_path = [
    'images',
    'images\\covers',
    'images\\bitmaps',
]


@dataclass(frozen=True)
class TkImage:
    image_base = {}  # object: img_source
    whole_name: str
    width: int
    height: int

    def __post_init__(self):
        for image_built in TkImage.image_base:
            if self == image_built:
                # had build before
                self = image_built
                break
        else:
            # new image
            TkImage.image_base[self] = self.__output_image()

    def __output_image(self):
        img = Image.open(self.whole_name)
        img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img

    def get_image(self):
        return TkImage.image_base[self]


def tk_image(filename, width=None, height=None, *, dirpath=None, get_object_only=False):
    '''
    passing arguments only the filename, not include path,
    if not give dirpath, it will be search from the top of search_path
    and return Error for not find.
    '''
    # ----- path -----
    if not dirpath:
        for path_ in _search_path:
            if os.path.exists(os.path.join(path_, filename)):
                path = path_
                break
        else:
            raise Exception(f'Not find the image: {filename}')
    else:
        path = dirpath
    # ----- path -----

    # ----- size -----
    size = Image.open(os.path.join(path, filename)).size
    if width:
        if height:
            size = (width, height)
        else:
            rate = width / size[0]
            height = int(size[1] * rate)
            size = (width, height)
    elif height:
        rate = height / size[1]
        width = int(size[0] * rate)
        size = (width, height)
    # ----- size -----
    img = TkImage(os.path.join(path, filename), *size)
    if get_object_only:
        return img
    return img.get_image()
