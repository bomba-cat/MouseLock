import pyautogui as py
import keyboard as key
from tkinter import *
import time

width, height = py.size()
py.FAILSAFE = True
FAILSAFE = True
right_click = False
moved = False
exit = False
broken = False
lock = 'v'
default = True
newX = 0
newY = 0

def right_held(event):
    global right_click, moved
    if moved == False:
        right_click = True
    moved = True

def right_released(event):
    global right_click
    right_click = False

def on_close():
    global exit
    win.destroy()
    exit = True

def change_failsafe():
    global FAILSAFE
    if FAILSAFE:
        py.FAILSAFE = False
        FAILSAFE = False
        failsafe.config(text=f'Failsafe: {FAILSAFE}')
    elif not FAILSAFE:
        py.FAILSAFE = True
        FAILSAFE = True
        failsafe.config(text=f'Failsafe: {FAILSAFE}')
    else:
        win.destroy()
        py.alert(title='An Error Occured!', text='Error getting the py.FAILSAFE status!')
        exit()

def change_lock_key(error):
    global lock
    if not error:
        new_lock = py.password(title='Change the Lock key',text='What do you want to change the Lock key to?', mask=None)
    elif error:
        new_lock = py.password(title='Change the Lock key',text='Unknown Key, please try again!', mask=None)
    else:
        py.alert(title='An Error Occured!', text='An error ocurred trying to chatch an exception! Please Report this to the Developers!')
    if new_lock != None:
        lock=new_lock
        lockbutton.config(text=f'Change Lock Key: {lock}')
    else:
        return

def change_mouse_root(change_to_default):
    global default, newX, newY, lock
    if not change_to_default:
        py.alert(title='Get Ready', text='Move your mouse to the new root position and press the button X')
        while True:
            if key.is_pressed('x'):
                pos = py.position()
                newX = pos[0]
                newY = pos[1]
                default = False
                break
    elif change_to_default:
        sure = py.confirm(title='Are you sure?',text='Are you sure you want to reset to the default settings?', buttons=['Yes','No'])
        if sure == 'Yes':
            py.alert(title='Reset to default settings',text='You were reset to the default settings!')
            default = True
            lock = 'v'
            lockbutton.config(text=f'Change Lock Key: {lock}')
            py.FAILSAFE = True
            FAILSAFE = True
            failsafe.config(text=f'Failsafe: {FAILSAFE}')
        elif sure != 'Yes':
            default = False
            py.alert(title='',text='Settings didnt change!')

win = Tk()

win.bind('<Button-3>', right_held)
win.bind('<B3-ButtonRelease>', right_released)
win.protocol('WM_DELETE_WINDOW', on_close)

warning = Label(text='Do not close this Window!')
warning.place(x=230,y=0)

hint = Label(text='Please minimize the window while the Lock is in use!')
hint.place(x=165,y=20)

failsafe = Button(text=f'Failsafe: {FAILSAFE}',command=change_failsafe)
failsafe.place(x=520,y=50)

lockbutton = Button(text=f'Change Lock Key: {lock}',command=lambda: change_lock_key(False))
lockbutton.place(x=0,y=50)

newpos = Button(text='Change position of Lock Root', command=lambda: change_mouse_root(False))
newpos.place(x=0,y=100)

default = Button(text='Default settings', command=lambda: change_mouse_root(True))
default.place(x=510,y=100)

win.title('Mouse Locker by xk_rl')
win.geometry('600x200')

def cap_mouse():
    global broken
    while True:
        if default:
            py.moveTo(width/2,height/2)
        elif not default:
            py.moveTo(newX, newY)
        if key.is_pressed(lock):
            time.sleep(0.2)
            broken = True
            break

while True:
    try:
        if key.is_pressed(lock):
            time.sleep(0.2)
            if not broken:
                cap_mouse()
            if broken:
                time.sleep(0.2)
                broken = False
    except ValueError:
        lockbutton.config(text=f'Change Lock Key: Unknown')
        change_lock_key(True)
    """ 
    W.I.P -
    Implementing the posibility to turn your camera in third person without the mouse moving away from the initial position 
    """
    
    """
    if right_click:
        pos = py.position()
        print(pos)
    if not right_click:
        if moved:
            py.move(pos[0],pos[1])
            print(pos[0],pos[1])
            moved = False
    """
    if exit:
        break
    win.update()