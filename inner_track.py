
import keyboard
import input
from pyautogui import *
import random


def find_odds():
    pre_odds = list(range(1, 31))
    pre_odds.pop(10)
    print(pre_odds)
    odds = pre_odds
    shot = screenshot(region=(180, 320, 78, 680))
    shot.save('./horses.png')
    # Checks each pic of odds 1/1, 2/1, etc
    horses = []
    for n in odds:
        for odd in list(locateAll('./odds/'+str(n)+'.png', './horses.png', confidence=.92)):
            add_horse = True
            for horse in horses:
                if abs(horse[1][1] - (odd.top + 320)) < 30:
                    add_horse = False
            if add_horse is True:
                adjusted_odd = (odd.left+180, odd.top+320, odd.width, odd.height)
                horses.append((n, adjusted_odd))
                print(str(n))
    # Calculates percentage from the present contestant's odds and sums them all
    high = horses[0]
    total_odds = 0
    for contestant in horses:
        percent = 100 / float(contestant[0] + 1)
        if percent > (100 / float(high[0] + 1)):
            high = contestant
        total_odds += percent
    # Ensures no contestant was missed
    if len(horses) != 6:
        return high, 322
    return high, total_odds


def enter_betting_menu():
    p1 = Point(random.randrange(1206, 1678), random.randrange(867, 951))
    moveTo(p1.x, p1.y)
    input.enter()
    time.sleep(.1)


def pause_until_odds_load():
    while not locateOnScreen('./single_bet_black.png', confidence=.9):
        pass


def select_best_odds():
    favored, total_odds = find_odds()
    ftop = favored[1][1]
    fleft = favored[1][0]
    p2 = Point(random.randrange(fleft, fleft + favored[1][2]), random.randrange(ftop, ftop + favored[1][3]))
    moveTo(p2.x, p2.y)
    input.enter()
    return total_odds


def adjust_and_place_bet(total_odds):
    if total_odds < 95:
        input.tab()
    p3 = Point(random.randrange(976, 1586), random.randrange(751, 839))
    moveTo(p3.x, p3.y)
    input.enter()
    time.sleep(34)


def back_to_starting_screen():
    if not locateOnScreen('./resources/bet_again.png', confidence=.95):
        input.esc()
        input.enter()
    else:
        p4 = Point(random.randrange(724, 1198), random.randrange(955, 1039))
        moveTo(p4.x, p4.y)
        input.enter()


def main():
    while True:
        if keyboard.is_pressed('1'):
            print('dfdfdfd')
            break
    time.sleep(1)
    while not keyboard.is_pressed('0'):
        enter_betting_menu()
        pause_until_odds_load()
        total_odds = select_best_odds()
        print(str(total_odds))
        print(time.time())
        adjust_and_place_bet(total_odds)
        back_to_starting_screen()


if __name__ == "__main__":
    main()



