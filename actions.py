
from pyautogui import *
import random
import collections

point = collections.namedtuple("Point", "x y")


def num(_min, _max):
    return random.randint(_min, _max)


def area(p1, p2):
    points = []
    for y in range(p1.y, p2.y):
        for x in range(p1.x, p2.x):
            points.append(Point(x, y))
    return points


def click_in(points):
    click(random.choice(points))


def delay_rand():
    modifier = num(0, 10)
    delay = .1 * modifier
    time.sleep(delay)



