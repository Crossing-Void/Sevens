'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The music.py is mainly for BGM aka music manipulations
user should build a instance for class Music to
do something to control whole music experience

'''
import pygame
import os


_msuic_path = 'musics'
pygame.init()
pygame.mixer.init()


class Music:
    def __init__(self):
        self.__music = None
        self.__pause = False

    @property
    def music(self):
        return self.__music

    @music.setter
    def music(self, value):
        self.__music = value
        if value is None:
            pygame.mixer.music.unload()
        else:
            pygame.mixer.music.load(os.path.join(_msuic_path, self.__music))
            pygame.mixer.music.play()

    @property
    def pause(self):
        return self.__pause

    @pause.setter
    def pause(self, value):
        self.__pause = value
        if self.__pause == True:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def toggle(self):
        self.pause = not (self.pause)

    def set_volume(self, volume):
        if (t := type(volume)) not in (int, float):
            raise Exception(
                f'The volume arguments should be a int or float, but got: {t}')
        pygame.mixer.music.set_volume(volume)

    def get_play_time(sec=True):
        return pygame.mixer.music.get_pos() / (1000 if sec else 1)

    def judge(self):
        if (not pygame.mixer.music.get_busy()) and (self.pause == False):
            if not (self.music is None):
                self.music = self.music
