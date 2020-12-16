import time

from ltp305 import LTP305

display = LTP305()


def change_red_to(switch: bool):
    for x in range(0, 5):
        for y in range(0, 7):
            display.set_pixel(x, y, switch)
    display.show()


def blinking_red():
    for _ in range(0, 3):
        change_red_to(True)
        time.sleep(0.2)
        change_red_to(False)
        time.sleep(0.2)


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
