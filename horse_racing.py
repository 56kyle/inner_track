
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
            # Occaisionally the ending screen doesn't appear and you have to exit out with escape
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
        if pyautogui.position().x < 400:
            pyautogui.moveTo(900, 400)
        snapshot = pyautogui.screenshot(region=racers_bounds)
        snapshot.save('./resources/temp/horses.png')
        plausible = list(range(1, 31))
        self.required_confidence = .95
        for i in plausible:
            if not pyautogui.locateAll("./resources/odds/{}.png".format(i), "./resources/temp/horses.png", confidence=.91):
                plausible.remove(i)
        while len(self.racers) != 6:
            print(self.required_confidence)
            for i in plausible:
                matching = pyautogui.locateAll("./resources/odds/{}.png".format(i), "./resources/temp/horses.png", confidence=self.required_confidence)
                if matching:
                    for candidate in matching:
                        adjusted_cand = Region(candidate.left + racers_bounds[0], candidate.top + racers_bounds[1], candidate.width, candidate.height)
                        appending = True
                        for racer in self.racers:
                            if abs(adjusted_cand.top - racer[1].top) < 15:
                                appending = False
                        if appending:
                            self.racers.append((i, adjusted_cand))
            if len(self.racers) > 6:
                self.required_confidence = self.required_confidence * 1.01
            elif len(self.racers) < 6:
                self.required_confidence = self.required_confidence * .99
            if len(self.racers) != 6:
                self.racers = []
            if self.required_confidence < .87:
                raise Exception

    def place_bet(self):
        favored_racer = (self.favored[1].left + random.randrange(1, 15), self.favored[1].top + random.randrange(1, 10))
        pyautogui.moveTo(favored_racer)
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

    @staticmethod
    def go_back_to_beginning():
        bet_again_button = Point(random.randrange(724, 1198), random.randrange(955, 1039))
        pyautogui.moveTo(bet_again_button)
        input.enter()


def main():
    session = Session()

    open_up_bets = Action(session.open_bet_screen, session.is_start_screen_open, gta=session.gta)
    find_odds = Action(session.determine_odds, session.is_bet_screen_open, gta=session.gta)
    place_bet = Action(session.place_bet, session.is_bet_screen_open, gta=session.gta)
    go_back_to_start = Action(session.go_back_to_beginning, session.is_end_screen_open, gta=session.gta)

    end_iter_tab = False
    while True:
        if not end_iter_tab:
            initial_tab = open_up_bets.act(tab=None, go_back=False)
        else:
            initial_tab = open_up_bets.act(tab=end_iter_tab, go_back=False)
        find_odds.act(tab=initial_tab, go_back=False)
        place_bet.act(tab=initial_tab, go_back=True)
        time.sleep(31) # Sleeps the duration of the "race"
        end_iter_tab = go_back_to_start.act(tab=None, go_back=False)


if __name__ == "__main__":
    main()
