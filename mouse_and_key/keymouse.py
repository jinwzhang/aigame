import win32api, win32con, win32gui
import pyautogui
import time
import random as rd
import mouse
import keyboard


"""
请使用管理员身份在cmd下调用程序

bcdedit /set nointegritychecks on开启 测试模式
bcdedit /set testsigning on禁用强制驱动签名模式
shutdown  -r -t 0 重启
"""


class KeyMouse:
    def __init__(self, window):
        self.window = win32gui.FindWindow(0, window)

    def set_window(self):
        win32gui.SetForegroundWindow(self.window)

    def click_rd(self, which='left', times=1):
        if which == 'left':
            for i in range(times):
                time.sleep(0.03 + rd.random() / 10)
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

    def mouse_move(self, x, y):
        # 移动鼠标
        mouse.move(x, y, absolute=False, duration=0.35 + rd.random()/6)

    def move_abs_rd(self, x, y):
        mouse.move(x, y, absolute=True, duration=0.35 + rd.random()/6)

    def mouse_drag(self, x_direction, y_direction):
        # 往x, y方向点击拖拽鼠标
        pass

    def mouse_scroll(self, n):
        pass

    def key_press_release(self, key_name):
        """
        string1: 输入的键盘按键字符串
         除了单个字符串，还可以向typewrite()函数传递键字符串的列表
         详情见typewrite_dict.txt
        """
        time.sleep(0.03 + rd.random() / 20)
        keyboard.press(key_name)
        time.sleep(0.02 + rd.random() / 10)
        keyboard.release(key_name)

    def hotkey_combo(self, key1, key2):
        # 快捷键组合 如 ctrl + c
        pass


if __name__ == '__main__':
    # hWndList = []
    # win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    # for hwnd in hWndList:
    #     clsname = win32gui.GetClassName(hwnd)
    #     title = win32gui.GetWindowText(hwnd)
    #     print(title)
    #
    km =KeyMouse('梦幻西游 ONLINE - (无与伦比[兰亭序] - 白米℃[11965514])')
    km.set_window()
    # km.mouse_move(1790, 200)
    # km.mouse_click(times=6)
    km.key_press_release('F6')
