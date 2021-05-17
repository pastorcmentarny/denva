import logging
import random
import time

from overseer import overseer_config, knight_rider_effect

logger = logging.getLogger('overseer')

def default_mode(mote):
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

def daydream(mote):
    logger.info('Daydream mode')
    color = overseer_config.colors_names[random.randint(0, len(overseer_config.colors_names) - 1)]
    if color in [overseer_config.RED, overseer_config.BLACK]:
        color = overseer_config.PURPLE
    selected_color = overseer_config.colors.get(color)
    knight_rider_effect.show_on_display(selected_color[0], selected_color[1], selected_color[2], mote)


def night_mode(mote):
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