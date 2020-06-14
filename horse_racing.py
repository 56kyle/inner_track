import random
from action import Action
import win32gui
import input
import pyautogui
import time
import collections
import os

Point = collections.namedtuple("Point", "x y")
Region = collections.namedtuple("Region", "left top width height")
Racer = collections.namedtuple("Racer", "odds location")
Color = collections.namedtuple("Color", "red green blue")


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
        while time.time() <= t1 + 3:
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

    @staticmethod
    def rgb2hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def determine_odds(self):
        racers = {'#00aeff': {"IT'S A TRAP": 1}, '#00e5f3': {'SALTY AND WOKE': 17}, '#00fff6': {'MUD DRAGON': 5},
                  '#00fffc': {'NORTHERN LIGHTS': 15}, '#105983': {'DRONE WARNING': 8},
                  '#1d8d52': {'MISTER REDACTED': 19},
                  '#209b23': {'DEXIE RUNNER': 6, 'DOOZY FLOOZY': 13}, '#228aff': {'BLUE DREAM': 2},
                  '#2c3d91': {'TENPENNY': 10},
                  '#2f9556': {'DIVORCED DOCTOR': 7}, '#343434': {'THROWING SHADY': 21},
                  '#3877a3': {'SIR SCRAMBLED': 26},
                  '#3aedb8': {'DRUNKEN BRANDEE': 14}, '#48f4ff': {'UPTOWN RIDER': 14},
                  '#4a75ff': {'BORROWED SORROW': 12, "DANCIN' POLE": 9}, '#4ae8ff': {'SCRAWNY NAG': 30},
                  '#4d7b72': {'HARD TIME DONE': 18}, '#4dadf7': {'BLACK ROCK ROOSTER': 18},
                  '#52d9b8': {'GETTING HAUGHTY': 3},
                  '#56ff29': {'FIRE HAZARDS': 24}, '#5792d4': {'DEAD FAM': 26}, '#6093f0': {'QUESTIONABLE DIGNITY': 12},
                  '#60cb93': {'SWEET RELEAF': 4}, '#63c5e9': {'CONSTANT BRAG': 3}, '#648319': {'PRETTY AS A PISTOL': 4},
                  '#6cff38': {'KRAFF RUNNING': 14}, '#6d80d4': {'CROCK JANLEY': 8}, '#765244': {"HENNIGAN'S STEED": 9},
                  '#771c58': {'MISS MARY JOHN': 22}, '#77c7ff': {'SOCIAL MEDIA WARRIOR': 27},
                  '#787878': {'LEAD IS OUT': 3},
                  '#834bf5': {'MICRO AGGRESSION': 8}, '#87eb96': {'FRIENDLY FIRE': 9},
                  '#921379': {'INVADE GRENADE': 13},
                  '#944384': {'MINIMUM WAGER': 26}, '#98d9ff': {'DREAM SHATTERER': 1}, '#9c47bb': {'GLASS OR TINA': 23},
                  '#9e5947': {'MISTER SCISSORS': 7}, '#9ed068': {'HELL FOR WEATHER': 2},
                  '#b070ff': {"SALT 'N' SAUCE": 1},
                  '#b1b1b1': {'THERE SHE BLOWS': 2}, '#bbffdd': {'STUDY BUDDY': 15}, '#c2e6ff': {'OMENS AND ICE': 3},
                  '#c7a362': {'WEE SCUNNER': 8}, '#cb254c': {"LOVER'S SPEED": 2}, '#ceec58': {'BANANA HAMMOCK': 16},
                  '#d16af3': {'DR. DEEZ REINS': 5}, '#d2ba32': {'WORTH A KINGDOM': 2},
                  '#d4441e': {'MEASLES SMEEZLES': 15},
                  '#d85050': {"YAY YO LET'S GO": 3}, '#e46161': {'SUMPTIN SAUCY': 1}, '#e6ff3a': {'GHOST DANK': 10},
                  '#e88e8e': {'STUPID MONEY': 30}, '#ec008c': {'ROBOCALL': 4}, '#ed5353': {'A TETHERED END': 27},
                  '#ed8a3a': {'FEED THE TROLLS': 30}, '#edc93a': {'DURBAN POISON': 20},
                  '#ee86cb': {'MISS TRIGGERED': 19},
                  '#eee2cd': {'CRACKERS AND PLEASE': 3}, '#f0ff00': {'REACH AROUND TOWN': 6},
                  '#f1e15f': {'THUNDER SKUNK': 20},
                  '#f2d23e': {'COUNTRY STUCK': 21, 'SQUARE TO GO': 6}, '#f54b4b': {'LIT AS TRUCK': 1},
                  '#f5874b': {'LONELY STEPBROTHER': 3}, '#f5c440': {'HOT & BOTHERED': 2},
                  '#f84067': {'BLEET ME BABY': 7},
                  '#f90707': {'CREEPY DENTIST': 7}, '#f94f5b': {'CANCELLED CHECK': 25},
                  '#fc00d0': {'MR. WORTHWHILE': 2},
                  '#fca9ff': {'BETTER THAN NOTHING': 15}, '#ff0000': {'NIGHT-TIME MARE': 16},
                  '#ff04cd': {'DEAD HEAT HATTIE': 17}, '#ff3232': {'BAD EGG': 29}, '#ff5151': {'DARLING RICKI': 22},
                  '#ff62bb': {'HIPPIE CRACK': 23}, '#ff6600': {'OLD ILL WILL': 29}, '#ff7550': {'MOON ROCKS': 4},
                  '#ff7e00': {'TEA ACHE SEA': 24}, '#ffbdef': {'FLIPPED WIG': 12, 'NUNS ORDERS': 9},
                  '#ffbeec': {'TURNT MOOD': 12, 'WAGE OF CONSENT': 21}, '#ffbf44': {'CLAPBACK CHARLIE': 10},
                  '#ffc21e': {'TAX THE POOR': 13}, '#ffe0f7': {'DOWNTOWN RENOWN': 4}, '#ffe400': {"OL' SKAG": 28},
                  '#ffe506': {'YELLOW SUNSHINE': 5}, '#ffebb6': {'SNATCHED YOUR MAMA': 1},
                  '#fff79b': {'MONEY TO BURN': 30},
                  '#ffffff': {'BOUNCY BLESSED': 5, "CAN'T BE WRONGER": 28, "DANCIN' SHOES": 5, 'LOS SANTOS SAVIOR': 5,
                              'PEDESTRIAN': 25, 'SIZZURP': 13, 'TOTAL BELTER': 1}}

        slot_x = 564
        slot_y_values = [
            320,
            440,
            564,
            685,
            805,
            927
        ]
        self.favored = Racer(30, (0, 0))
        total_percent = 0
        for y in slot_y_values:
            c = pyautogui.pixel(slot_x, y)
            hex_code = self.rgb2hex(c[0], c[1], c[2])
            color_path = "./resources/horses/{}".format(hex_code)
            if len(racers[hex_code].keys()) > 1:
                for candidate, odds in racers[hex_code].items():
                    location = pyautogui.locateOnScreen(color_path + "/" + candidate + '.png', confidence=.95)
                    if location and (y - 50) < location[1] < y:
                        total_percent += 100 / (odds + 1)
                        if self.favored.odds > odds:
                            self.favored = Racer(odds, (location[0], location[1]))
                        break
            elif len(racers[hex_code].keys()) == 1:
                odds = None
                for i in racers[hex_code].items():
                    candidate = i[0]
                    odds = i[1]
                total_percent += 100 / (odds + 1)
                if self.favored.odds > odds:
                    self.favored = Racer(odds, (slot_x-50, y))
        self.round_percentage = total_percent

    def place_bet(self):
        favored_racer = (self.favored.location[0] + random.randrange(1, 15), self.favored.location[1] + random.randrange(1, 10))
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
        time.sleep(31)  # Sleeps the duration of the "race"
        end_iter_tab = go_back_to_start.act(tab=None, go_back=False)


if __name__ == "__main__":
    main()
