import logging
import random

from overseer import overseer_config

logger = logging.getLogger('overseer')


def set_color_for(mote, color_name: str):
    if color_name in overseer_config.colors:
        red, green, blue = overseer_config.colors.get(color_name)
        change_to(mote, red, green, blue)
    else:
        logger.warning(f'I need supported color not {color_name}')
        return 'rubbish'


def change_to(mote, red: int, green: int, blue: int, brightness=0.4):
    for led_index in range(0, 16):
        for led_line in range(1, 5):
            mote.set_pixel(led_line, led_index, red, green, blue, brightness)
    mote.show()


def transform(mote):
    for r in range(0, 255):
        change_to(mote, int(r), 0, 0, 0.4)

    for r in range(255, 160, -1):
        change_to(mote, int(r), 0, 0, 0.3)

    for r in range(160, 255):
        change_to(mote, int(r), 0, 0, 0.4)

    for r in range(255, 32, -1):
        change_to(mote, int(r), 0, 0, 0.2)

    repeat = random.randint(1, 10)
    for _ in range(0, repeat):
        for _ in range(32, 128):
            change_to(mote, _, int(_ / 2), 0, 0.3)
        for _ in range(128, 32):
            change_to(mote, _, int(_ / 2), 0, 0.2)

    repeat = random.randint(1, 20)
    for _ in range(0, repeat):
        for r in range(64, 224):
            change_to(mote, int(r), int(r * 2 / 3), 0, 0.3)

        for r in range(224, 64, -1):
            change_to(mote, int(r), int(r * 2 / 3), 0, 0.2)
