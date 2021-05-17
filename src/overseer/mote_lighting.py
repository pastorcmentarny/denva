import logging
import random
import time

from mote import Mote

from overseer import lighting_effect, knight_rider_effect, borg_effect, rain_effect, alert_effect, overseer_utils

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

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()

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
lighting_colors = [RED_RGB_COLOUR, ORANGE_RGB_COLOUR, GREEN_RGB_COLOUR, BLUE_RGB_COLOUR, PURPLE_RGB_COLOUR,
                   WHITE_RGB_COLOUR, BLACK_RGB_COLOUR, BROWN_RGB_COLOUR, YELLOW_RGB_COLOUR, CYAN_RGB_COLOUR,
                   MAGENTA_RGB_COLOUR, YELLOW_GREEN_RGB_COLOUR,
                   FLAME_RGB_COLOUR, PARADISE_RGB_COLOUR]


def set_busy_mode():
    overseer_utils.set_color_for(RED)





def default_mode():
    logger.info('Idle')
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
    logger.info('Party time!')
    blink_speed = 0.02
    mote.set_brightness(0.4)
    for times in range(1000):
        for led_index in range(0, 16):
            for led_line in range(1, 5):
                mote.set_pixel(led_line, led_index, random.randint(0, 256), random.randint(0, 256),
                               random.randint(0, 256))
        mote.show()
        time.sleep(blink_speed)
        overseer_utils.set_color_for(BLACK)
        mote.show()
        time.sleep(blink_speed)
    logger.info('Party is over.')


def daydream():
    logger.info('Daydream mode')
    color = colors_names[random.randint(0, len(colors_names) - 1)]
    if color in [RED, BLACK]:
        color = PURPLE
    selected_color = colors.get(color)
    knight_rider_effect.show_on_display(selected_color[0], selected_color[1], selected_color[2], mote)


def night_mode():
    logger.info('In night mode')
    for _ in range(10):
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

    # add possibility for fire lighting
    result = random.randint(1, 100)
    if result > 88:
        fire_effect_with_lighting()


def turn_light_off():
    logger.info('Switching off light')
    for led_index in range(0, 16):
        for led_line in range(1, 5):
            mote.set_pixel(led_line, led_index, 0, 0, 0, 0)
    mote.clear()
    mote.set_brightness(0.1)


def transform():
    for r in range(0, 255):
        overseer_utils.change_to(int(r), 0, 0, 0.4)

    for r in range(255, 160, -1):
        overseer_utils.change_to(int(r), 0, 0, 0.3)

    for r in range(160, 255):
        overseer_utils.change_to(int(r), 0, 0, 0.4)

    for r in range(255, 32, -1):
        overseer_utils.change_to(int(r), 0, 0, 0.2)

    repeat = random.randint(1, 10)
    for _ in range(0, repeat):
        for _ in range(32, 128):
            overseer_utils.change_to(_, int(_ / 2), 0, 0.3)
        for _ in range(128, 32):
            overseer_utils.change_to(_, int(_ / 2), 0, 0.2)

    repeat = random.randint(1, 20)
    for _ in range(0, repeat):
        for r in range(64, 224):
            overseer_utils.change_to(int(r), int(r * 2 / 3), 0, 0.3)

        for r in range(224, 64, -1):
            overseer_utils.change_to(int(r), int(r * 2 / 3), 0, 0.2)


def fire_effect_with_lighting():
    for _ in range(1, 10):
        for _ in range(1, 3):
            transform()

        probability = random.randint(1, 100)
        if probability > 96:
            for _ in range(1, probability):
                lighting_effect.lighting(mote)
        elif probability > 88:
            lighting_effect.rainbow_lighting(mote)
        elif probability > 80:
            lighting_effect.lighting(mote)


def borg():
    borg_effect.show_on_display(mote)


def red_alert():
    alert_effect.red_alert(mote)


def yellow_alert():
    alert_effect.yellow_alert(mote)


def rain():
    rain_effect.random_rain(mote)
