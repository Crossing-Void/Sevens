'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The project_management.py is mainly for whole project management,
mostly all function the project will use, is inside here

'''
from Tkinter_template.Assets.image import tk_image
from Tkinter_template.Assets.font import font_get
from tkinter import *
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
