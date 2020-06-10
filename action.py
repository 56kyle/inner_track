
import win32gui
import pyautogui


class Action:
    def __init__(self, method, prereq=None):
        self.prereq = prereq
        self.method = method

    def prereq(self):
        self.prereq()

    def act(self):
        while True:
            if self.prereq is None or self.prereq():
                return self.method()

