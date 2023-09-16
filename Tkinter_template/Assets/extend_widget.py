'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The extend_widget.py is mainly for some widget basic on tk widget,
adding some features on them

'''
from tkinter import Button


class BindButton(Button):
    '''
    for keyboard holdon feature
    need focus on 
    like use 'Return' for enter key
    '''

    def __init__(self, char, root=None, **option):
        self.char = char
        self.__state = False
        super().__init__(root, **option)
        self.__bind()

    def __bind(self):
        def keypress(event):
            if (self.char is None) or (event.keysym == self.char):
                self.config(relief='sunken')

        def keyrelease(event):
            if (self.char is None) or (event.keysym == self.char):
                self.config(relief='raised')
                if self.__state:
                    self.invoke()
                else:
                    self.__state = True

        self.bind('<KeyPress>', keypress)
        self.bind('<KeyRelease>', keyrelease)


class EffectButton(Button):
    '''
    achieve hover feature
    '''

    def __init__(self, color: tuple, root=None, **option):
        '''
        color(first for bg, second for fg)
        '''
        self.color = color
        super().__init__(root, **option)
        self.__bg = self['bg']
        self.__fg = self['fg']
        self.__bind()

    def __bind(self):
        def enter(event):
            self.config(bg=self.color[0], fg=self.color[1])

        def leave(event):
            self.config(bg=self.__bg, fg=self.__fg)

        self.bind('<Enter>', enter)
        self.bind('<Leave>', leave)
