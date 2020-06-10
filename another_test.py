import win32gui
import pyautogui
import time
import collections


Point = collections.namedtuple("Point", "x y")
Area = collections.namedtuple("Area", "left top right bottom")


class State:
    def __init__(self):
        self.cursor = pyautogui.position()
        self.window = win32gui.GetForegroundWindow()
        print(win32gui.GetWindowText(self.window))

    def set(self):
        pyautogui.moveTo(self.cursor)
        win32gui.SetForegroundWindow(self.window)


def when_afk(action):
    while True:
        p1 = pyautogui.position()
        time.sleep(.01)
        if p1 == pyautogui.position():
            break
    return action()


def exit_chrome(hwnd):
    prev = when_afk(State)
    win32gui.SetForegroundWindow(hwnd)
    pyautogui.click(1910, 10)
    prev.set()


def window_handler(hwnd, *args):
    if 'Google Chrome' in win32gui.GetWindowText(hwnd):
        exit_chrome(hwnd)


def main():
    while True:
        win32gui.EnumWindows(window_handler, None)


if __name__ == '__main__':
    main()