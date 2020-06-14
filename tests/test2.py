
import pyautogui
import keyboard
import time


def main():
    while True:
        x, y = pyautogui.position()
        print(pyautogui.pixel(x, y))
        time.sleep(.5)


if __name__ == "__main__":
    main()
