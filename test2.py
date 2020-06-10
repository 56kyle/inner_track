
import pyautogui
import keyboard
import time


def main():
    num = 0
    while True:
        if keyboard.is_pressed('1'):
            num += 1
            snap = pyautogui.screenshot()
            print('snap')
            snap.save('./resources/rounds/r{}.png'.format(num))
            time.sleep(.5)


if __name__ == "__main__":
    main()
