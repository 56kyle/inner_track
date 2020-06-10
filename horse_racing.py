
import random
from action import Action
import win32gui
import input
import pyautogui
import time
import collections

Point = collections.namedtuple("Point", "x y")
Region = collections.namedtuple("Region", "left top width height")


class Session:
    def __init__(self):
        self.gta = None
        self.racers = []
        self.favored = None
        self.round_percentage = 0
        self.required_confidence = 0
        self.total_rounds = 0
        self.rounds_max_bet = 0
        self.rounds_min_bet = 0
        self.start_screen_marker = './resources/markers/single_event.png'
        self.bet_screen_marker = './resources/markers/single_bet_black.png'
        self.end_screen_marker = './resources/markers/bet_again.png'
        while not self.gta:
            self.gta = win32gui.FindWindow(None, "Grand Theft Auto V")
            time.sleep(.1)

    def is_gta_focused(self):
        return win32gui.GetForegroundWindow() == self.gta

    def is_start_screen_open(self):
        while not self.is_gta_focused():
            pass
        return pyautogui.locateOnScreen(self.start_screen_marker, confidence=.9)

    def is_bet_screen_open(self):
        while not self.is_gta_focused():
            pass
        return pyautogui.locateOnScreen(self.bet_screen_marker, confidence=.9)

    def is_end_screen_open(self):
        while not self.is_gta_focused():
            pass
        t1 = time.time()
        while time.time() <= t1 + 5:
            if pyautogui.locateOnScreen(self.end_screen_marker, confidence=.9):
                return True
        else:
            input.esc()
            time.sleep(1)
            input.enter()
            return True

    @staticmethod
    def open_bet_screen():
        click_location = Point(random.randrange(1206, 1678), random.randrange(867, 951))
        pyautogui.moveTo(click_location)
        input.enter()

    def determine_odds(self):
        self.required_confidence = .94
        self.racers = []
        self.append_racers()
        self.finish_calculations()

    def finish_calculations(self):
        self.favored = self.racers[0]
        self.round_percentage = 0
        for racer in self.racers:
            if self.favored[0] > racer[0]:
                self.favored = racer
            self.round_percentage += 100 / (racer[0] + 1)

    def append_racers(self):
        racers_bounds = (150, 340, 340-150, 1000-340)
        snapshot = pyautogui.screenshot(region=racers_bounds)
        snapshot.save('./resources/temp/horses.png')
        plausible_odds = list(range(1, 31))
        for i in range(1, 31):
            matching = pyautogui.locateAll('./resources/temp/horses.png', "./resources/odds/{}.png".format(i), confidence=self.required_confidence)
            if len(matching) == 0:
            if matching is not None:
                for candidate in list(matching):
                    adjusted_cand = Region(candidate.left + racers_bounds[0], candidate.top + racers_bounds[1], candidate.width, candidate.height)
                    appending = True
                    for racer in self.racers:
                        if i == racer[0] and abs(adjusted_cand.top - racer[1].top) < 15:
                            appending = False
                    if appending:
                        pyautogui.moveTo(adjusted_cand.left, adjusted_cand.top)
                        self.racers.append((i, adjusted_cand))

    def place_bet(self):
        pyautogui.moveTo(self.favored[1].left+random.randrange(1, 15), self.favored[1].top+random.randrange(1, 10))
        input.enter()
        if self.round_percentage < 95:
            self.rounds_max_bet += 1
            input.tab()
        else:
            self.rounds_min_bet += 1
        self.total_rounds += 1
        submit_bet_button = Point(random.randrange(976, 1586), random.randrange(751, 839))
        pyautogui.moveTo(submit_bet_button)
        input.enter()
        time.sleep(30)

    @staticmethod
    def go_back_to_beginning():
        bet_again_button = Point(random.randrange(724, 1198), random.randrange(955, 1039))
        pyautogui.moveTo(bet_again_button)
        input.enter()


def main():
    session = Session()

    open_up_bets = Action(session.open_bet_screen, session.is_start_screen_open)
    find_odds = Action(session.determine_odds, session.is_bet_screen_open)
    place_bet = Action(session.place_bet, session.is_bet_screen_open)
    go_back_to_start = Action(session.go_back_to_beginning, session.is_end_screen_open)

    while True:
        open_up_bets.act()
        find_odds.act()
        round_pic = pyautogui.screenshot()
        round_pic.save("./resources/rounds/test/{}.png".format(session.total_rounds))
        place_bet.act()
        go_back_to_start.act()


if __name__ == "__main__":
    main()
