import random
import time

from mote import Mote

import fasting_timer

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()
mote.set_brightness(0.4)

RED = [255, 0, 0]
ORANGE = [144, 77, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
PURPLE = [75, 0, 130]
WHITE = [255, 255, 255]
BLACK = [1, 1, 1]
BROWN = [160, 96, 64]

colors = {
    'red': RED,
    'orange': ORANGE,
    'green': GREEN,
    'blue': BLUE,
    'purple': PURPLE,
    'white': WHITE,
    'black': BLACK,
    'brown': BROWN,
}

colors_names = ['red', 'orange', 'green', 'blue', 'purple', 'white', 'black', 'brown']


def set_busy_mode():
    set_color_for('red')


def set_color_for(color_name: str):
    if color_name in colors:
        red, green, blue = colors.get(color_name)
        change_to(red, green, blue)
    else:
        return 'rubbish'


def change_to(red: int, green: int, blue: int):
    for led_index in range(0, 16):
        for led_line in range(1, 5):
            mote.set_pixel(led_line, led_index, red, green, blue)
    mote.show()


def red_alert():
    mote.set_brightness(0)
    for i in range(0, 16):
        for c in range(1, 5):
            mote.set_pixel(c, i, 255, 0, 0)

    for counter in range(0, 5):
        for b in range(0, 100):
            brightness = b / 100
            mote.set_brightness(brightness)
            time.sleep(0.02)
            mote.show()
        for d in range(99, -1, -1):
            brightness = d / 100
            mote.set_brightness(brightness)
            time.sleep(0.02)
            mote.show()


def default_mode():
    mote.clear()
    mote.set_brightness(0.2)
    for times in range(100):
        speed = (random.randint(0, 20) / 100) + 0.01
        xmas_snow_colors = [[255, 0, 0], [0, 255, 0], [255, 255, 255]]
        red, green, blue = xmas_snow_colors[random.randint(0, len(xmas_snow_colors) - 1)]
        line = random.randint(1, 4)
        for led_index in range(0, 16):
            mote.clear()
            mote.set_pixel(line, led_index, red, green, blue, 0.4)
            if led_index > 0:
                mote.set_pixel(line, led_index - 1, red, green, blue, 0.3)
            if led_index > 1:
                mote.set_pixel(line, led_index - 2, int(red / 2), int(green / 2), int(blue / 2), 0.2)
            if led_index > 2:
                mote.set_pixel(line, led_index - 3, int(red / 4), int(green / 4), int(blue / 4), 0.1)
            mote.show()
            time.sleep(speed)


def party_mode():
    mote.set_brightness(0.6)
    for times in range(1000):
        for led_index in range(0, 16):
            for led_line in range(1, 5):
                mote.set_pixel(led_line, led_index, random.randint(0, 256), random.randint(0, 256),
                               random.randint(0, 256))
        mote.show()
        time.sleep(0.02)
        set_color_for('black')
        mote.show()
        time.sleep(0.02)


def knight_rider(red: int, green: int, blue: int):
    mote.clear()
    mote.set_brightness(0.2)
    for times in range(10):
        for line_index in range(0, 16):
            mote.clear()
            for line_led in range(1, 5):
                mote.set_pixel(line_led, line_index, red, green, blue, 0.4)
                if line_index > 0:
                    mote.set_pixel(line_led, line_index - 1, red, green, blue, 0.3)
                if line_index > 1:
                    mote.set_pixel(line_led, line_index - 2, int(red / 2), int(green / 2), int(blue / 2), 0.2)
                if line_index > 2:
                    mote.set_pixel(line_led, line_index - 3, int(red / 2), int(green / 2), int(blue / 2), 0.1)
            mote.show()
            time.sleep(0.1)

        for line_index in range(15, -1, -1):
            mote.clear()
            for line_led in range(1, 5):
                mote.set_pixel(line_led, line_index, red, green, blue, 0.4)
                if line_index < 15:
                    mote.set_pixel(line_led, line_index + 1, red, green, blue, 0.3)
                if line_index < 14:
                    mote.set_pixel(line_led, line_index + 2, int(red / 2), int(green / 2), int(blue / 2), 0.2)
                if line_index < 13:
                    mote.set_pixel(line_led, line_index + 3, int(red / 2), int(green / 2), int(blue / 2), 0.1)
            mote.show()
            time.sleep(0.1)


def daydream():
    color = colors_names[random.randint(0, len(colors_names) - 1)]
    if color in ['red', 'black']:
        color = 'purple'
    selected_color = colors.get(color)
    knight_rider(selected_color[0], selected_color[1], selected_color[2])


def night_mode():
    for _ in range(60):
        for _ in range(2):
            color = colors_names[random.randint(0, len(colors_names) - 1)]
            selected_color = colors.get(color)
            mote.set_pixel(random.randint(1, 4), random.randint(0, 15), selected_color[0], selected_color[1],
                           selected_color[2],
                           0.4)

        for led_index in range(0, 16):
            for led_line in range(1, 5):
                pixel = mote.get_pixel(led_line, led_index)
                if pixel[3] <= 0.1:
                    mote.set_pixel(led_line, led_index, 0, 0, 0, 0)
                else:
                    mote.set_pixel(led_line, led_index, pixel[0], pixel[1], pixel[2], (pixel[3] - 0.1))

        mote.show()
        time.sleep(1)


def display_fasting_status():
    mote.clear()
    leds = 0
    all_pixels = RED
    time_left_pixels = ORANGE
    if fasting_timer.is_default_fasting_time():
        all_pixels = ORANGE
        time_left_pixels = GREEN
        leds = fasting_timer.get_timer_for_fasting()
    else:
        leds = fasting_timer.get_timer_for_eating()

    for led_index in range(0, 16):
        mote.set_pixel(1, led_index, all_pixels[0], all_pixels[1], all_pixels[2], 0.2)
    for led_index in range(0, leds):
        mote.set_pixel(1, led_index, time_left_pixels[0], time_left_pixels[1], time_left_pixels[2], 0.3)
    mote.show()
    time.sleep(0.25)

    for _ in range(10):
        mote.set_pixel(1, leds, all_pixels[0], all_pixels[1], all_pixels[2], 0.2)
        mote.show()
        time.sleep(0.25)
        mote.set_pixel(1, leds, time_left_pixels[0], time_left_pixels[1], time_left_pixels[2], 0.3)
        mote.show()
        time.sleep(0.25)
    mote.clear()
