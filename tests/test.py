import win32gui
import pyautogui
import time
import keyboard


class Session:
    def __init__(self, config):
        self.round = 0
        self.config = {}
        for key, value in config.items():
            self.config[key] = value

    def take_pics_of_odds(self, *args):
        self.round += 1
        for i in range(1, 7):
            left_bound = int(self.config['left_bound'])
            right_bound = int(self.config['right_bound'])
            top = int(self.config['top{}'.format(i)])
            bot = int(self.config['bot{}'.format(i)])
            snap = pyautogui.screenshot(region=(left_bound, top, right_bound-left_bound, bot-top))
            snap.save('./resources/rounds/r{}_slot{}.png'.format(self.round, i))

        time.sleep(1)


def main():
    config = {}
    with open('../config.txt') as file:
        for line in file.readlines():
            if line != "\n":
                only_text = line.strip("\n")
                pair = only_text.split(' = ')
                config[pair[0]] = pair[1]
    session = Session(config=config)
    while True:
        if keyboard.is_pressed('1'):
            session.take_pics_of_odds()
            time.sleep(1)


if __name__ == '__main__':
    main()

