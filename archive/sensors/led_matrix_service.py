import time
from datetime import datetime

from ltp305 import LTP305

display = LTP305()


def display_fasting_mode():
    clock = datetime.now()
    if clock.hour > 18 or clock.hour <= 12:
        blinking_red()
        set_red()
        if clock.hour == 12:
            end_of_red_timer()
    else:
        top_up_green()
        set_green()
    update_led_matrix()


def change_red_to(switch: bool):
    for x in range(0, 5):
        for y in range(0, 7):
            display.set_pixel(x, y, switch)
    display.show()


def blinking_red():
    for _ in range(0, 5):
        change_red_to(True)
        time.sleep(0.05)
        change_red_to(False)
        time.sleep(0.05)


def top_up_green():
    for y in range(6, -1, -1):
        for x in range(0, 5):
            display.set_pixel(x, y, True)
            display.set_pixel(x + 5, y, False)
        time.sleep(0.1)


def end_of_red_timer():
    for end_timer in range(9, -1, -1):
        display.set_character(0, str(end_timer))
        display.show()
        if end_timer == 0:
            time.sleep(0.30)
        else:
            time.sleep(0.20)


def set_red():
    for x in range(0, 5):
        for y in range(0, 7):
            display.set_pixel(x, y, True)
            display.set_pixel(x + 5, y, False)


def red():
    set_red()
    blinking_red()
    set_red()
    end_of_red_timer()
    set_green()


def set_green():
    for x in range(0, 5):
        for y in range(0, 7):
            display.set_pixel(x, y, False)
            display.set_pixel(x + 5, y, True)


def update_led_matrix():
    display.show()
