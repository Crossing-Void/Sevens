'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The default_menu.py is mainly for optional
function in the selective function.

'''
from Tkinter_template.Assets.project_management import new_window, select_cover
from Tkinter_template.Assets.font import font_get
from Tkinter_template.Assets.image import tk_image
from PIL import ImageColor
from tkinter import *
import os


def background_color(canvas: object):
    def color(position):
        str_of_color = f'#{red.get():02x}{green.get():02x}{blue.get():02x}'
        canvas.config(bg=str_of_color)

    def select_color(color):
        canvas.config(bg=color)
        win.destroy()

    win = new_window('Background Color')

    red = Scale(win, font=font_get(20), bg='red', length=255, tickinterval=50, command=color,
                from_=0, to=255, label='Red')
    green = Scale(win, font=font_get(20), bg='green', length=255, tickinterval=50, command=color,
                  from_=0, to=255, label='Green')
    blue = Scale(win, font=font_get(20), bg='blue', length=255, tickinterval=50, command=color,
                 from_=0, to=255, label='Blue')

    color_select = ['chocolate', 'lightblue',
                    'violet', 'silver', 'indigo']
    x, y, z = ImageColor.getrgb(canvas['bg'])
    red.set(x)
    green.set(y)
    blue.set(z)
    red.grid(row=1, column=1, rowspan=len(
        color_select), sticky='sn')
    green.grid(row=1, column=2, rowspan=len(
        color_select), sticky='sn')
    blue.grid(row=1, column=3, rowspan=len(
        color_select), sticky='sn')

    index = 1
    for item in color_select:
        Button(win, font=font_get(20), bg=item, height=15//len(color_select), fg='black', text=item,
               command=lambda x=item: select_color(x)).grid(row=index, column=4, sticky='ew')
        index += 1


def canvas_cover(canvas: object, canvas_side: tuple, side: tuple = None):
    def click(num):
        canvas_.itemconfigure(f'rec{num}', state='normal')
        for i in range(len(cover)):
            if i != num:
                canvas_.itemconfigure(f'rec{i}', state='hidden')

    def double_click(num):
        select_cover(canvas, canvas_side, cover[num])
        win.destroy()
    if side is None:
        side = canvas_side
    win = new_window(
        'Windows Cover', maxsize=side)
    scrollbar = Scrollbar(win)
    scrollbar.grid(row=1, column=2, sticky='ns')
    canvas_ = Canvas(win, width=side[0]-int(scrollbar['width']), height=side[1], bg=canvas['bg'],
                     yscrollcommand=scrollbar.set)
    canvas_.grid(row=1, column=1)
    scrollbar['command'] = canvas.yview

    cover = [img for img in os.listdir('images\\covers') if img.endswith('png')
             or img.endswith('jpg') or img.endswith('jpeg')]
    wi_inter, hi_inter = 100, 120
    wi = (int(canvas_['width']) - 2*wi_inter - 20)//3
    hi = wi * 3 // 4

    for i in range(len(cover)):

        canvas_.create_image(20+i % 3 * (wi + wi_inter), 20+i//3 * (hi + hi_inter), anchor='nw',
                             image=tk_image(
            cover[i], wi, hi),
            tags=(f'img{i}'))

        canvas_.create_text(20+i % 3 * (wi + wi_inter) + wi//2, 20+i//3 * (hi + hi_inter)+20+24//2 + hi, font=font_get(24),
                            text=cover[i], tags=(f'text{i}'))

        x, y, x2, y2 = (20+i % 3 * (wi + wi_inter), 20+i//3 * (hi + hi_inter),
                        20+i % 3 * (wi + wi_inter)+wi, 20+i//3 * (hi + hi_inter)+hi)
        canvas_.create_rectangle(x-4, y-4, x2+4, y2+4, width=4, outline='gold',
                                 state='hidden', tags=(f'rec{i}'))

        canvas_.tag_bind(f'img{i}', '<Button-1>',
                         lambda event, x=i: click(x))
        canvas_.tag_bind(
            f'img{i}', '<Double-Button-1>', lambda event, x=i: double_click(x))

    canvas_['scrollregion'] = (
        0, 0, int(canvas['width']), 20+i//3 *
        (hi + hi_inter)+20+24//2 + hi+60
    )
    canvas_.bind('<MouseWheel>', lambda event: canvas_.yview_scroll(-(event.delta//120), 'units')
                 )
