import logging
import random
import time

from mote import Mote

from overseer import lighting_effect, knight_rider_effect, borg_effect, rain_effect, alert_effect, overseer_utils, \
    overseer_config

logger = logging.getLogger('overseer')

mote = Mote()
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()


def set_busy_mode():
    overseer_utils.set_color_for(overseer_config.RED)


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
        overseer_utils.set_color_for(overseer_config.BLACK)
        mote.show()
        time.sleep(blink_speed)
    logger.info('Party is over.')


def daydream():
    logger.info('Daydream mode')
    color = overseer_config.colors_names[random.randint(0, len(overseer_config.colors_names) - 1)]
    if color in [overseer_config.RED, overseer_config.BLACK]:
        color = overseer_config.PURPLE
    selected_color = overseer_config.colors.get(color)
    knight_rider_effect.show_on_display(selected_color[0], selected_color[1], selected_color[2], mote)


def night_mode():
    logger.info('In night mode')
    for _ in range(10):
        for _ in range(2):
            color = overseer_config.colors_names[random.randint(0, len(overseer_config.colors_names) - 1)]
            selected_color = overseer_config.colors.get(color)
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
