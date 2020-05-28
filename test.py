from pyautogui import *
import keyboard
import random


resources = './resources/'
files = [
    '0.png',
    '1.png',
    '2.png',
    '3.png',
    '4.png',
    '5.png',
    '6.png',
    '7.png',
    '8.png',
    '9.png'
]


def main():
    while True:
        if keyboard.is_pressed('1'):
            print('Breaking from loop.')
            break
        else:
            pass

    time.sleep(5)

    for i in range(6):
        odds = screenshot(region=(184, 367+(i*118), 71, 30))
        odds.save('./odds/' + str(i) + 'ss' + str(random.randint(1, 19999)) + '.png')


if __name__ == "__main__":
    main()
