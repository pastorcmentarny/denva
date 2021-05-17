import logging
import time
import random

logger = logging.getLogger('overseer')

def show_on_display(mote):
    logger.info('We are the Borg. Resistance is futile')
    blink_speed = 0.5
    mote.set_brightness(0.1)
    for times in range(10):
        for led_index in range(0, 16):
            for led_line in range(1, 5):
                mote.set_pixel(led_line, led_index, 0, random.randint(0, 255), 0)
        mote.set_pixel(random.randint(1, 4), random.randint(0, 15), 0, 255, 0, random.randint(1, 10) / 10)
        mote.show()
        time.sleep(blink_speed)