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

import time
from bh1745 import BH1745

import config
import logging

from gateways import local_data_gateway

LED_OFF = 0

LED_ON = 1

logger = logging.getLogger('app')


def get_new_instance():
    bh1745 = BH1745()
    bh1745.setup()
    bh1745.set_leds(1)
    return bh1745


bh1745 = get_new_instance()


def warn_if_dom_shakes_his_legs(motion):
    if motion > config.get_shaking_level():
        for i in range(5):
            bh1745.set_leds(LED_ON)
            time.sleep(0.25)
            bh1745.set_leds(LED_OFF)
            time.sleep(0.15)


def led_startup_show():
    for i in range(5):
        bh1745.set_leds(LED_ON)
        time.sleep(0.2)
        bh1745.set_leds(LED_OFF)
        time.sleep(0.05)
    bh1745.set_leds(LED_OFF)


def on():
    bh1745.set_leds(LED_ON)


def off():
    bh1745.set_leds(LED_OFF)


def get_measurement():
    global bh1745
    try:
        result = bh1745.get_rgb_scaled()
        return result
    except Exception as exception:
        logger.error(f' Unable to take measurement from uv sensor due to {exception}')
        local_data_gateway.post_metrics_update('rgb', 'errors')
        bh1745 = get_new_instance()
        return 0, 0, 0


def switch_led(led_status):
    bh1745.set_leds(led_status)
    if led_status == 1:
        return LED_OFF
    else:
        return LED_ON


def error_blink():
    blink_length = [0.1, 0.16, 0.25, 0.36, 0.49, 0.64]
    for i in range(5):
        bh1745.set_leds(LED_ON)
        time.sleep(blink_length[i])
        bh1745.set_leds(LED_OFF)
        time.sleep(blink_length[i])
    bh1745.set_leds(LED_OFF)
