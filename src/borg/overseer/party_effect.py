import logging
import random
import time

import overseer_utils, overseer_config

logger = logging.getLogger('overseer')


def random_color_mode(mote):
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
        overseer_utils.set_color_for(mote, overseer_config.BLACK)
        mote.show()
        time.sleep(blink_speed)
    logger.info('Party is over.')
