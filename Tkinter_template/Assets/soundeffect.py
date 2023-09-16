'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The soundeffect.py is mainly for sound effects,
particularly a short sound for special use in project.

'''
from Tkinter_template.Assets.universal import delete_extension
import pygame
import os


pygame.init()
pygame.mixer.init()
_search_path = ['sounds']
_soundeffects = {}


def _gather_soundeffects():
    for path_ in _search_path:
        try:
            walker = os.walk(path_)
            break
        except:
            pass

    for now, _, filelist in walker:
        for filename in filelist:
            temp = now.split('\\')
            key = temp[1:]+[delete_extension(filename)] if len(
                temp) >= 2 else [delete_extension(filename)]
            _soundeffects['/'.join(key)] = pygame.mixer.Sound(
                os.path.join(now, filename))


_gather_soundeffects()


def play_sound(filename):
    _soundeffects[filename].play()
