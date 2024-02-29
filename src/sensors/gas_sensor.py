#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import logging

from mics6814 import MICS6814

logger = logging.getLogger('app')

#TODO IMPLEMENT THIS SENSOR
def setup():
    logger.debug("Setting up Gas Sensor")
    gas = MICS6814()
    gas.set_pwm_period(4096)

    gas.set_brightness(0)
    gas.set_led(16, 16, 16)
    return gas


gas = setup()


def get_measurement():
    try:
        data = gas.read_all()
        oxidising = data.oxidising / 1000
        reducing = data.reducing / 1000
        nh3 = data.nh3 / 1000
        return oxidising, reducing, nh3
    except Exception as exception:
        logger.error(
            f'Unable to read data from mics6814 (gas sensor) sensor due to {type(exception).__name__} throws : {exception}',
            exc_info=True)
        setup()
        raise exception


colors = {
    'measurement': [0, 0, 255],
    'process': [0, 255, 255],
    'wait': [255, 255, 0],
    'idle': [0, 255, 0],
    'start': [255, 255, 255],
    'error': [255, 0, 0],
    'end': [128, 255, 192]
}


def set_colour_to(color_type: str):
    if color_type in colors:
        color = colors[color_type]
        try:
            gas.set_led(color[0], color[1], color[2])
        except Exception as exception:
            logger.error(f'Unable to led colour due to {type(exception).__name__} throws : {exception}')
    else:
        logger.warning(f'You forgot set color for {color_type}')
        gas.set_led(255, 128, 192)
