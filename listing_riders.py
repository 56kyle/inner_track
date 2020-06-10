
import pyautogui
import time
import collections

Point = collections.namedtuple("Point", "x y")


def main():
    time.sleep(5)
    slots = [
        Point(x=564, y=319),
        Point(x=564, y=440),
        Point(x=564, y=563),
        Point(x=564, y=685),
        Point(x=564, y=805),
        Point(x=564, y=929)
    ]
    for i in slots:
        pyautogui.moveTo(i)
        time.sleep(1)


if __name__ == "__main__":
    main()
