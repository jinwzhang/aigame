import mouse
import time
import random as rd


def click_rd(which='left',times=1):
    if which == 'left':
        for i in range(times):
            time.sleep(0.03+rd.random() / 10)
            mouse.press()
            time.sleep(0.03 + rd.random() / 10)
            mouse.release()
    elif which == 'right':
        for i in range(times):
            time.sleep(0.03 + rd.random() / 10)
            mouse.press(button=mouse.RIGHT)
            time.sleep(0.03 + rd.random() / 10)
            mouse.release(button=mouse.RIGHT)
    elif which == 'middle':
        'middle is TODO'
    else:
        raise ValueError('鼠标按键错误')

def abs_move_rd(x, y):
    mouse.move(x, y, absolute=True, duration=0.05 + rd.random())


if __name__ == '__main__':
    time.sleep(2)
    mouse.double_click()
