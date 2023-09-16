'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The universal.py is mainly for some goody function to save time
(mostly from previous project)
'''
from Tkinter_template.Assets.project_management import making_widget
from Tkinter_template.Assets.image import tk_image
from dataclasses import dataclass
from datetime import date
import random
import json
import time
import os


def delete_extension(filename):
    return filename[:filename.rfind('.')]


def str_tuple_date_change(arg):
    '''
    switch date tuple {(2022, 12, 12)}(includes datetime.date objs) and date string format {2022-12-12}
    '''
    if type(arg) == str:
        return (int(arg[:4]), int(arg[5:7]), int(arg[8:10]))
    elif type(arg) == tuple:
        return f'{arg[0]:04d}-{arg[1]:02d}-{arg[2]:02d}'
    elif type(arg) == date:
        return f'{arg.year:04d}-{arg.month:02d}-{arg.day:02d}'


def parse_json_to_property(app: object, json_file: str):
    '''
    support bool, int, float, str, list(max one layer)
    '''
    def category(value):
        '''
        only for zero layer object
        '''
        match value:
            case bool():
                return 'Boolean'
            case int():
                return 'Int'
            case float():
                return 'Double'
            case str():
                return 'String'
            case _:
                raise Exception('Parsing JSON error')

    def assign(name, value):
        app  # for exec app
        typename = category(value)
        if typename == 'String':
            exec(
                f'app.{name} = making_widget("{typename}Var")(app.root, value="{value}")'
            )
        else:
            exec(
                f'app.{name} = making_widget("{typename}Var")(app.root, value={value})'
            )

    with open(json_file) as f:
        settingDict = json.load(f)

    for key, value in settingDict.items():
        if type(value) == list:
            decoration = 0
            for sub_value in value:
                assign(f'{key}_{decoration}', sub_value)
                decoration += 1
        else:
            assign(key, value)


class MoveBg:
    '''
    A MoveBg obj only affects one canvas,
    if need to affect multiple canvas, build another obj
    for the class here
    '''
    imgName = []  # tuple (path, filename)

    def __init__(self, canvas: object, canvas_side: tuple, rate: float, source_folder: str, abandon_folder: tuple) -> None:
        self.c = canvas
        self.cs = canvas_side
        self.r = rate
        self.__timer = time.time()

        self.__gain_source_image(source_folder, abandon_folder)

    def __gain_source_image(self, folder, aba_folder):
        for now, _, filelist in os.walk(folder):
            for filename in filelist:
                if (now not in aba_folder) and (filename[filename.rfind('.'):] in (
                    '.png', '.tiff', '.jpg', '.ico', '.jpeg'
                )):
                    MoveBg.imgName.append((now, filename))

    def __create_image_for_bg(self):
        for obj in _BgObj.existObj:
            self.c.create_image(obj.x, obj.y, anchor='sw', tags=('moveBg'), image=tk_image(
                obj.img[1], width=obj.size, dirpath=obj.img[0]
            ))

    def create_obj(self, number: int = 1):
        for _ in range(number):
            r = self.r
            setting = {
                'x': random.randint(int(self.cs[0]//r), int(self.cs[0]-self.cs[0]//r)),
                'y': 0,
                'u': random.randint(-7, 7),
                'v': random.randint(3, 11),
                'size': random.randint(int(self.cs[0]//(r+1)), int(self.cs[0]//r)),
                'img': random.choice(MoveBg.imgName)
            }

            _BgObj(**setting)

    def flush(self):
        if (temp := time.time()) - self.__timer > 0.05:
            self.c.delete('moveBg')
            self.__create_image_for_bg()
            try:
                self.c.tag_raise('moveBg', 'cover')
            except:
                try:
                    min = self.c.find_all()[0]
                    self.c.tag_lower('moveBg', min)
                except:
                    pass
            self.__timer = temp
            for obj in _BgObj.existObj:
                if obj.move(self.cs):
                    self.create_obj()


@dataclass
class _BgObj:
    existObj = []
    x: int
    y: int
    u: int
    v: int
    size: int
    img: tuple

    def __post_init__(self) -> None:
        self.existObj.append(self)

    def move(self, bd):
        self.x += self.u
        self.y += self.v
        if self.x < 0 or self.x > bd[0]-self.size:
            self.u *= -1
        if self.y > bd[1]+self.size:
            self.existObj.remove(self)
            return True
