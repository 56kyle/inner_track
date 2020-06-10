
import random
import pyautogui
import keyboard
import input
import collections
import win32api
import win32gui
import time

Point = collections.namedtuple("Point", "x y")
Box = collections.namedtuple("Box", "left top right bot")
Racer = collections.namedtuple("Racer", "odds box")


class Session:
    def __init__(self):
        self.rounds = 0
        self.gta = None
        while not self.gta:
            self.gta = win32gui.FindWindow(None, "Grand Theft Auto V")
            time.sleep(1)
        else:
            print("Gta Found")

        while win32gui.GetForegroundWindow() != self.gta:
            time.sleep(1)
        else:
            left, top, right, bot = win32gui.GetClientRect(self.gta)
            self.screen = Box(left, top, right, bot)
            print("Screen Size Found - ", end="")
            print(self.screen)

    def is_gta(self):
        return self.gta == win32gui.GetForegroundWindow()

    def pause_until_window_change(self, marker):
        while not pyautogui.locateOnScreen(marker, confidence=.95):
            pass

    def afk_or_not(self):
        p1 = win32gui.GetCursorPos()
        time.sleep(.1)
        p2 = win32gui.GetCursorPos()
        return p2 == p1

    def on_afk(self, action):
        last_position = win32gui.GetCursorPos()
        while not self.afk_or_not():
            last_position = win32gui.GetCursorPos()
        else:
            previous_window = win32gui.GetForegroundWindow()
            if previous_window != self.gta:
                win32gui.SetForegroundWindow(self.gta)
            while not self.is_gta():
                pass
            else:
                action()
                pyautogui.moveTo(last_position)
                if previous_window != self.gta:
                    win32gui.SetForegroundWindow(previous_window)

    def bet(self):
        if self.main_or_single():
            self.on_afk(self.enter_betting_menu)
            self.on_afk(self.select_best_odds)
            self.on_afk(self.adjust_and_place_bet)
            self.on_afk(self.back_to_starting_screen)

    def enter_betting_menu(self):
        p1 = Point(random.randrange(1206, 1678), random.randrange(867, 951))
        pyautogui.moveTo(p1.x, p1.y)
        input.enter()
        self.pause_until_window_change('')

    def find_odds(self):
        odds = list(range(1, 11))+list(range(12, 31))
        racers_region = (int(.09375*self.screen.right), int(.29629*self.screen.bot), int(.04062*self.screen.right), int(.62962*self.screen.bot))
        shot = pyautogui.screenshot(region=racers_region)
        shot.save('./horses.png')
        # Checks each pic of odds 1/1, 2/1, etc
        req_conf = .9
        horses = []
        while len(horses) != 6:
            req_conf += .01
            horses = []
            for i in odds:
                if len(horses) < 7:
                    for rider_with_odd in list(pyautogui.locateAll('./odds/' + str(i) + '.png', './horses.png', confidence=req_conf)):
                        horses.append(rider_with_odd)
                    else:
                        break
            if len(horses) < 6:
                req_conf -= .015

        # Calculates percentage from the present contestant's odds and sums them all
        high = horses[0]
        total_odds = 0
        for contestant in horses:
            percent = 100 / float(contestant[0] + 1)
            if percent > (100 / float(high[0] + 1)):
                high = contestant
            total_odds += percent
        return high, total_odds

    def select_best_odds(self):
        favored, total_odds = self.find_odds()
        ftop = favored[1][1]
        fleft = favored[1][0]
        p2 = Point(random.randrange(fleft, fleft + favored[1][2]), random.randrange(ftop, ftop + favored[1][3]))
        pyautogui.moveTo(p2.x, p2.y)
        input.enter()

    def adjust_and_place_bet(self, total_odds):
        if total_odds < 95:
            input.tab()
        p3 = Point(random.randrange(976, 1586), random.randrange(751, 839))
        pyautogui.moveTo(p3.x, p3.y)
        input.enter()
        time.sleep(34)

    def back_to_starting_screen(self):
        if not pyautogui.locateOnScreen('./resources/bet_again.png', confidence=.95):
            input.esc()
            input.enter()
        else:
            p4 = Point(random.randrange(724, 1198), random.randrange(955, 1039))
            pyautogui.moveTo(p4.x, p4.y)
            input.enter()

    def main_or_single(self):
        return pyautogui.locateOnScreen('./resources/single_event.png', confidence=.9)


    def betting_menu(self):
        return True

    def bet_selection(self):
        return True

    def loading_race(self):
        return True

    def race_results(self):
        return True

if __name__ == "__main__":
    s = Session()
    time.sleep(3)



    #time.sleep(5)
    #print(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
