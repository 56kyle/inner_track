
import pyautogui
import time
import collections

Point = collections.namedtuple("Point", "x y")


def main():
    time.sleep(5)
    slot_x = 564
    slot_y_values = [
        320,
        440,
        564,
        685,
        805,
        927
    ]
    for y in slot_y_values:
        pyautogui.moveTo((slot_x, y))
        time.sleep(1)



if __name__ == "__main__":
    main()
