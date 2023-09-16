'''
@version: 1.1.3
@author: CrossingVoid
@date: 2023/03/05

The base.py include the main class `Interface`.

Using our template, should(or need) to construct your projoct folder in the form:

Structure:
    Project
        images
          bitmaps
            files
          covers
            files
        sounds
          files
        musics
          files
        datas
          files
        modules
          files
        project.py

Minimum:
    Project
        project.py

'''
from Tkinter_template.Assets.project_management import create_menu
from tkinter import *
import os


class Interface:
    rate = 0.8

    def __init__(self, title: str, icon=None, default_menu=True):
        self.__default_menu = default_menu
        self.__create_root(title, icon)
        self.__create_canvas()
        self.__create_menu_default()
        self.__create_dashboard()

    def __create_root(self, title, icon):
        '''
        root, side(tuple), isFullscreen(property)
        '''
        self.root = Tk()
        self.side = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        # self.side stand for fullscreen and not include top menu bar 20 pixel
        self.root.title(title)
        if icon:
            self.root.iconbitmap(os.path.join('images\\bitmaps', icon))
        self.root.maxsize(*self.side)
        self.root.resizable(0, 0)
        self.root.state('zoomed')
        self.isFullscreen = True

    @ property
    def isFullscreen(self):
        return self.__isFullscreen

    @ isFullscreen.setter
    def isFullscreen(self, value):
        self.__isFullscreen = value
        self.root.wm_attributes('-fullscreen', self.isFullscreen)

    def __create_canvas(self):
        '''
        canvas, canvas_side(tuple)

        -20 for top bar(20 pixel)
        '''
        def esc(event):
            self.isFullscreen = not (self.isFullscreen)

        self.canvas = Canvas(self.root, width=self.side[0] * self.rate, height=self.side[1] - (20 if self.__default_menu else 0),
                             highlightthickness=0, bg='lightblue')

        self.canvas.focus_set()
        self.canvas_side = int(self.canvas['width']), int(
            self.canvas['height'])
        self.canvas.grid(row=1, column=1, sticky='snew')
        self.canvas.bind('<Escape>', esc)

    def __create_menu_default(self):
        '''
        top_menu(is the horizontal one), default_menu(the leftmost one for selective function)
        '''
        self.top_menu = create_menu(self.root)
        self.root.config(menu=self.top_menu)

        self.default_menu = create_menu(self.top_menu)

        if self.__default_menu:
            self.top_menu.add_cascade(
                label='Selective Function', menu=self.default_menu
            )

    def __create_dashboard(self):
        '''
        dashboard, dashboard_side(tuple)
        '''
        self.dashboard = Frame(self.root, cursor='dot',
                               width=self.side[0] * (1 - self.rate), height=self.side[1] - (20 if self.__default_menu else 0))
        self.dashboard_side = int(self.dashboard['width']), int(
            self.dashboard['height'])

        self.dashboard.grid(row=1, column=2, sticky='snew')


# ------------------------------------------------------------------------------------------------------------------
