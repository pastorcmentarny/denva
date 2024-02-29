# busy mode
# orange mode
# borg mode
import datetime
import random

import time
from mote import Mote

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


def is_all_black() -> bool:
    for led_index in range(0, 16):
        for led_line in range(1, 5):
            pixel = mote.get_pixel(led_line, led_index)
            if pixel[3] >= 0.05:
                return False
    return True


def to_black():
    while not is_all_black():
        for led_index in range(0, 16):
            for led_line in range(1, 5):
                pixel = mote.get_pixel(led_line, led_index)
                if pixel[3] > 0.1:
                    brightness = float("%.2f" % (pixel[3] - 0.1))
                    mote.set_pixel(led_line, led_index, 112, 32, 0, brightness)
                elif pixel[3] > 0:
                    mote.set_pixel(led_line, led_index, 0, 0, 0, 0.0)
            mote.show()
    mote.clear()
    mote.show()


def update(mote):
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


def update_to_next_line(line):
    if line == 1:
        direction = random.randint(1, 2)
        if direction == 2:
            line += 1
    elif line == 4:
        direction = random.randint(1, 2)
        if direction == 1:
            line -= 1
    else:
        direction = random.randint(1, 3)
        if direction == 1:
            line -= 1
        else:
            line += 1
    return line


def orange_lighting():
    pixels = []
    line = random.randint(1, 4)
    for led_index in range(0, 16):
        line = update_to_next_line(line)
        mote.set_pixel(line, led_index, 224, 64, 0, 1)
        mote.show()
        pixels.append([line, led_index, 224, 64, 0, 1])
        time.sleep(0.015)


def lighting():
    lighting_counter = random.randint(3, 100)
    for _ in range(0, lighting_counter):
        if random.randint(1, 10) > 8:
            orange_lighting()
        else:
            line = random.randint(1, 4)
            for led_index in range(0, 16):
                line = update_to_next_line(line)
                mote.set_pixel(line, led_index, 255, 255, 255, 1)
                mote.show()
                time.sleep(0.01)

        mote.clear()
        mote.show()


def app(mote):
    generate()
    update(mote)
    cycle_count = 0
    orange_lighting_count = 0
    lighting_storm_count = 0
    while True:
        cycle_count += 1
        print("Run no." + str(cycle_count) + " " + str(datetime.datetime.now()) + ". " + "Orange lightings:" + str(
            orange_lighting_count) + ". Lighting storms: " + str(lighting_storm_count) + ".")
        times = 10 + random.randint(1, 240)
        for _ in range(1, times):
            update(mote)
            wait_time = random.randint(1, 1000) / 10000
            time.sleep(wait_time)

        if random.randint(1, 10) > 6:
            orange_lighting()
            to_black()
            orange_lighting_count += 1

        if random.randint(1, 1000) > 966:
            lighting()
            to_black()
            lighting_storm_count += 1


# stand-alone version of night mode
if __name__ == '__main__':
    mote = Mote()
    mote.configure_channel(1, 16, False)
    mote.configure_channel(2, 16, False)
    mote.configure_channel(3, 16, False)
    mote.configure_channel(4, 16, False)

    mote.clear()
    generate()
    update(mote)
    cycle = 0
    app(mote)
