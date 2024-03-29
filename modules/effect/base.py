from abc import ABC, abstractclassmethod
import time
import re

class Base(ABC):
    def __init__(self, main, controler, timer_number: int = 1):
        self.main = main
        self.controler = controler

        time_ = time.time()
        self.timer = [time_] * timer_number

    @abstractclassmethod
    def start(self):
        return NotImplemented

    @abstractclassmethod
    def end(self):
        return NotImplemented

    @abstractclassmethod
    def loop(self):
        return NotImplemented

    def detect(self):
        x = self.main.root.winfo_pointerx() - self.main.root.winfo_rootx()
        y = self.main.root.winfo_pointery() - self.main.root.winfo_rooty()
        objs = self.c.find_overlapping(x, y, x+1, y+1)

        if len(objs) <= 1:
            return None
        else:
            # directly return genre name
            obj = objs[1]
            tags = self.main.canvas.gettags(obj)
            for tag in tags:
                m = re.search("^(\w+)-(\w+)$", tag)
                if m:
                    return m.group(2) 