
import win32gui
import win32api
from ctypes import *


class Action:
    def __init__(self, method, prereq=None, gta=None):
        self.prereq = prereq
        self.method = method
        self.gta = gta

    def prereq(self):
        self.prereq()

    def act(self, tab=None, go_back=True):
        while True:
            if tab is None:
                tab = win32gui.GetForegroundWindow()
            pos1 = win32api.GetCursorPos()
            if tab != self.gta:
                win32gui.SetForegroundWindow(self.gta)
            if self.prereq is None or self.prereq():
                self.method()
                if win32gui.GetForegroundWindow() != tab and go_back:
                    win32gui.SetForegroundWindow(tab)
                win32api.SetCursorPos(pos1)
                return tab

