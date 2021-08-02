# busy mode
# orange mode
# borg mode


import random

import time
from mote import Mote

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()

pixels = []

MAX = 6


def generate():
    for x in range(1, 5):
        for y in range(0, 16):
            pixels.append([x, y, random.randint(0, MAX) / 10])


def change_brightness(brightness_value):
    if brightness_value == 0.0:
        return 0.1
    if brightness_value >= 0.4:
        return 0.3
    if brightness_value == 0.1:
        return change_randomly_to_one_of(0.2, 0.0)
    if brightness_value == 0.2:
        return change_randomly_to_one_of(0.3, 0.1)
    if brightness_value == 0.3:
        return change_randomly_to_one_of(0.4, 0.2)
    if brightness_value == 0.4:
        return change_randomly_to_one_of(0.5, 0.3)
    return random.randint(0, MAX) / 10


def change_randomly_to_one_of(higher_value, lower_value):
    if bool(random.getrandbits(1)):
        return higher_value
    else:
        return lower_value


def update():
    for led_line in range(1, 5):
        for led_index in range(0, 16):
            pixel = mote.get_pixel(led_line, led_index)
            brightness = change_brightness(pixel[3])
            if bool(random.getrandbits(1)):
                mote.set_pixel(led_line, led_index, 224, 64, 0, brightness)
            elif bool(random.getrandbits(1)):
                mote.set_pixel(led_line, led_index, 192, 48, 0, brightness)
            else:
                mote.set_pixel(led_line, led_index, 112, 32, 0, brightness / 2)
    mote.show()


if __name__ == '__main__':
    generate()
    while True:
        update()
        wait_time = random.randint(1, 100) / 1000
        time.sleep(wait_time)
