'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The project_management.py is mainly for whole project management,
mostly all function the project will use, is inside here

'''
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get, font_span
from tkinter import *
import time
import os


def create_menu(root):
    '''
    Can made menu own and inner code also use, need to bind to top_menu
    '''
    return Menu(root, font=font_get(16), tearoff=0)


def new_window(title, icon=None, maxsize: tuple = None):
    child_root = Toplevel()
    child_root.title(title)
    if icon:
        child_root.iconbitmap(os.path.join('images\\bitmaps', icon))
    if maxsize:
        child_root.maxsize(*maxsize)
        child_root.state('zoomed')
    child_root.resizable(0, 0)

    return child_root


def making_widget(widget: str):
    try:
        return eval(widget)
    except:
        raise ValueError(f'The widget: {widget} does not exist in Tk')


def canvas_obj_states(canvas, mode, *tag):
    '''
    canvas: select a canvas to make manipulation on it
    mode can accept: {delete, hidden, normal}
    tag(tuple): stand for remain tag

    ***** PUT `H` IN TAGS, IF YOU DO WANT KEEP HIDDEN OF THE OBJ 
          AND WIDGET USING `H` IN TAG BASICLLY SHOULD HAS `HIDDEN` STATE *****
    '''
    for id_ in canvas.find_all():
        for tags in canvas.gettags(id_):
            if tags in tag:
                # not do thing on it
                break
        else:
            if mode == 'delete':
                canvas.delete(id_)
            elif mode == 'normal':
                if 'H' in canvas.gettags(id_):
                    # some obj keep hidden even do the switch
                    pass
                else:
                    canvas.itemconfigure(id_, state='normal')
            elif mode == 'hidden':
                canvas.itemconfigure(id_, state='hidden')


def select_cover(canvas: object, side: tuple, file):
    canvas.delete('cover')
    for x in range(100):
        canvas.create_image(
            0, (side[1])*x, anchor='nw', image=tk_image(file, side[0], side[1]), tags=('cover'))

        canvas.tag_lower('cover', canvas.find_all()[0])


def canvas_reduction(canvas, canvas_side, music_obj=None, cover=None, music=None):
    canvas.delete('all')
    canvas.xview_moveto(0)
    canvas.yview_moveto(0)
    if music_obj:
        music_obj.music = None

    if cover:
        select_cover(canvas, canvas_side, cover)
    if music and music_obj:
        music_obj.music = music
    # can adding for common use bind keys
    canvas.update()
    canvas.unbind('<MouseWheel>')
    canvas.unbind('<Return>')
    canvas.unbind('<Button-1>')
    canvas.unbind('<Double-Button-1>')
    canvas.unbind('<space>')


def progress_bar(params, **args):
    if t := (type(params)) != dict:
        raise ValueError(f"The parameter params should be a dict, but got {t}")

    default_params = {
        'bg': '#FFF9A6',
        'outline': ('black', 'green'),
        'line width': 10,
        'position': (0, 0)
    }

    valid_args = [
        'total',  # int, set what number of part is
        'new window',  # boolean, progress bar should exists in new window or not
        'size',  # tuple, for all progress bar size(width, height)
        'canvas',  # for canvas to pad on
        'position',  # set progress bar to the position
        'bg',  # set new window's canvas bg
        'outline',  # tuple, (incomplete part, complete part)
        'line width',  # for line width
    ]
    # if new window is True, also need to pass size, otherwise pass size, canvas, position
    for key in params:
        if key not in valid_args:
            raise ValueError(f"Not a valid arguments: {key}")

    default_params.update(params)

    class ProgressBar:
        def __init__(self, func) -> None:
            self.func = func

        def __depict_progress(self, position: tuple = (0, 0), proportion=0):
            self.canvas.delete('progressbar')
            w, h = self.params['size'][0], self.params['size'][1]
            width_is_bigger = w >= h
            try:
                complete_ratio = proportion / self.params['total']
            except:
                complete_ratio = 0
            line_width = self.params['line width']
            out_line = self.params['outline']

            if width_is_bigger:
                point = (position[0] + int((w-h)/2),
                         position[1] + line_width/2,
                         position[0] + int((w-h)/2) + h,
                         position[1] + h - line_width / 2)

            else:
                point = (position[0] + line_width / 2,
                         position[1] + int((h-w)/2),
                         position[0] + w - line_width / 2,
                         position[1] + int((h-w)/2) + w)

            crr = int(complete_ratio*360)
            if crr == 360:
                self.canvas.create_oval(*point, width=line_width, outline=out_line[1],
                                        tags=('progressbar', 'progressbar-complete'))
            else:
                self.canvas.create_arc(*point, width=line_width, start=90-crr, extent=crr,
                                       style='arc', outline=out_line[1],
                                       tags=('progressbar', 'progressbar-complete'))
            if crr == 0:
                self.canvas.create_oval(*point, width=line_width, outline=out_line[0],
                                        tags=('progressbar', 'progressbar-incomplete'))
            else:
                self.canvas.create_arc(*point,  width=line_width, start=90, extent=360-crr, style='arc',
                                       outline=out_line[0],
                                       tags=('progressbar', 'progressbar-incomplete'))
            self.canvas.create_text(
                position[0]+int(w/2), position[1]+int(h/2),
                text=f'{round(complete_ratio*100, 1)}%', font=font_get(font_span('100.0%', h*0.9 if width_is_bigger else w*0.9)),
                tags=('progressbar', 'progressbar-ratio'))

            if hasattr(self, 'window'):
                t = self.window.title
                t(t()[:t().rfind("-")+1] + f' {round(complete_ratio*100, 1)}%')
            self.canvas.update()

        def __start(self):
            bg = self.params['bg']

            if self.params['new window']:
                self.window = new_window(
                    f"{self.func.__name__} -- Start", maxsize=self.params['size'])

                self.canvas = making_widget("Canvas")(self.window, width=self.params['size'][0],
                                                      height=self.params['size'][1], bg=bg)
                self.canvas.grid()
            else:
                self.canvas = self.params['canvas']
            self.__depict_progress(self.params['position'])

        def __call__(self, *args, **kwargs):
            self.__start()
            self.func(*args, **kwargs)
            time.sleep(0.5)
            if hasattr(self, 'window'):
                self.window.destroy()
            else:
                self.canvas.delete('progressbar')

        def add_arg(self, params, **kwargs):
            if t := (type(params)) != dict:
                raise ValueError(
                    f"The parameter params should be a dict, but got {t}")
            params.update(args)

            for key in params:
                if key not in valid_args:
                    raise ValueError(f"Not a valid arguments: {key}")

                self.__class__.params[key] = params[key]

        def compelete_part(self, proportion):
            self.__depict_progress(proportion=proportion)

    ProgressBar.params = default_params
    return ProgressBar
