import logging
import random
import time

from mote import Mote

logger = logging.getLogger('overseer')

# import fasting_timer
PARADISE = 'paradise'
FLAME = 'flame'
YELLOW_GREEN = 'yellow_green'
MAGENTA = 'magenta'
CYAN = 'cyan'
YELLOW = 'yellow'
BROWN = 'brown'
BLACK = 'black'
WHITE = 'white'
PURPLE = 'purple'
BLUE = 'blue'
GREEN = 'green'
ORANGE = 'orange'
RED = 'red'
RED_RGB_COLOUR = [255, 0, 0]
ORANGE_RGB_COLOUR = [224, 64, 0]
GREEN_RGB_COLOUR = [0, 255, 0]
YELLOW_GREEN_RGB_COLOUR = [153, 204, 0]
BLUE_RGB_COLOUR = [0, 0, 255]
PURPLE_RGB_COLOUR = [75, 0, 130]
WHITE_RGB_COLOUR = [255, 255, 255]
BLACK_RGB_COLOUR = [1, 1, 1]
BROWN_RGB_COLOUR = [160, 96, 32]
YELLOW_RGB_COLOUR = [255, 255, 0]
CYAN_RGB_COLOUR = [0, 255, 255]
MAGENTA_RGB_COLOUR = [192, 0, 192]
FLAME_RGB_COLOUR = [242, 85, 44]
PARADISE_RGB_COLOUR = [144, 222, 227]
colors = {
    RED: RED_RGB_COLOUR,
    ORANGE: ORANGE_RGB_COLOUR,
    GREEN: GREEN_RGB_COLOUR,
    BLUE: BLUE_RGB_COLOUR,
    PURPLE: PURPLE_RGB_COLOUR,
    WHITE: WHITE_RGB_COLOUR,
    BLACK: BLACK_RGB_COLOUR,
    BROWN: BROWN_RGB_COLOUR,
    YELLOW: YELLOW_RGB_COLOUR,
    CYAN: CYAN_RGB_COLOUR,
    MAGENTA: MAGENTA_RGB_COLOUR,
    YELLOW_GREEN: YELLOW_GREEN_RGB_COLOUR,
    FLAME: FLAME_RGB_COLOUR,
    PARADISE: PARADISE_RGB_COLOUR
}

colors_names = [RED, ORANGE, GREEN, BLUE, PURPLE, WHITE, BLACK, BROWN, YELLOW, CYAN, MAGENTA,
                YELLOW_GREEN, FLAME, PARADISE]


def random_rain(mote):
    light_rain(mote)


def light_rain(mote):
    logger.info('Rain mode')
    mote.clear()
    mote.set_brightness(0.2)
    for times in range(100):
        speed = (random.randint(0, 20) / 100) + 0.01
        rain_colors = [RED_RGB_COLOUR, ORANGE_RGB_COLOUR, GREEN_RGB_COLOUR, BLUE_RGB_COLOUR, PURPLE_RGB_COLOUR,
                       WHITE_RGB_COLOUR, BLACK_RGB_COLOUR, BROWN_RGB_COLOUR, YELLOW_RGB_COLOUR, CYAN_RGB_COLOUR,
                       MAGENTA_RGB_COLOUR, YELLOW_GREEN_RGB_COLOUR,
                       FLAME_RGB_COLOUR, PARADISE_RGB_COLOUR]

        red, green, blue = rain_colors[random.randint(0, len(rain_colors) - 1)]
        line = random.randint(1, 4)
        for index in range(0, 16):
            mote.clear()
            mote.set_pixel(line, index, red, green, blue, 0.4)
            if index > 0:
                mote.set_pixel(line, index - 1, red, green, blue, 0.3)
            if index > 1:
                mote.set_pixel(line, index - 2, int(red / 2), int(green / 2), int(blue / 2), 0.2)
            if index > 2:
                mote.set_pixel(line, index - 3, int(red / 4), int(green / 4), int(blue / 4), 0.1)
            mote.show()
            time.sleep(speed)


def draw(mote, red: int, green: int, blue: int, brightness=0.4, speed=1):
    line = random.randint(1, 4)
    for index in range(0, 16):
        mote.clear()
        mote.set_pixel(line, index, red, green, blue, brightness)
        if index > 0:
            mote.set_pixel(line, index - 1, red, green, blue, brightness - 0.1)
        if index > 1:
            mote.set_pixel(line, index - 2, int(red / 2), int(green / 2), int(blue / 2), brightness - 0.2)
        mote.show()
        time.sleep(speed / 100)


def rain_storm(mote):
    rain_colors = [RED_RGB_COLOUR, ORANGE_RGB_COLOUR, GREEN_RGB_COLOUR, BLUE_RGB_COLOUR, PURPLE_RGB_COLOUR,
                   WHITE_RGB_COLOUR, BLACK_RGB_COLOUR, BROWN_RGB_COLOUR, YELLOW_RGB_COLOUR, CYAN_RGB_COLOUR,
                   MAGENTA_RGB_COLOUR, YELLOW_GREEN_RGB_COLOUR,
                   FLAME_RGB_COLOUR, PARADISE_RGB_COLOUR]

    while True:
        for s in range(25, 1, -1):
            b = (random.randint(3, 10) / 10)
            red, green, blue = rain_colors[random.randint(0, len(rain_colors) - 1)]
            draw(mote, red, green, blue, b, s)
        for s in range(2, 24, 1):
            b = (random.randint(3, 10) / 10)
            red, green, blue = rain_colors[random.randint(0, len(rain_colors) - 1)]
            draw(mote, red, green, blue, b, s)


if __name__ == '__main__':
    mote = Mote()
    mote.configure_channel(1, 16, False)
    mote.configure_channel(2, 16, False)
    mote.configure_channel(3, 16, False)
    mote.configure_channel(4, 16, False)

    mote.clear()
    rain_storm(mote)
