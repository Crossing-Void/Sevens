'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The font.py is mainly for font manipulations
'''
from tkinter.font import Font
import tkinter.font as font
import os

_font_family = 'Inconsolata'
_font_file_location = "data\\fonts_install\\inconsolata.ttf"


def check_font():
    if _font_family in list(font.families()):
        return True


def set_font():
    os.system(_font_file_location)


def change_font(font):
    global _font_family
    _font_family = font


def font_get(size, bold=False):
    return (_font_family, size, 'bold' if bold else '')


def font_span(text, fit_size, *, upper_bound=1000):
    '''
    Giving a width and text, generate exact font size.
    '''

    size = 1
    while True:
        if size >= upper_bound:
            return upper_bound
        if Font(font=font_get(size)).measure(text) > fit_size:
            break
        size += 1
    return size - 1


def measure(text, size):
    return Font(font=font_get(size)).measure(text)
