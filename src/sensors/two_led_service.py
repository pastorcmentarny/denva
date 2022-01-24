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


# Set up light sensor
from gateways import local_data_gateway

logger = logging.getLogger('app')
bh1745 = BH1745()
bh1745.setup()
bh1745.set_leds(1)


def warn_if_dom_shakes_his_legs(motion):
    if motion > config_service.get_shaking_level():
        for i in range(5):
            bh1745.set_leds(1)
            time.sleep(0.25)
            bh1745.set_leds(0)
            time.sleep(0.15)


def led_startup_show():
    for i in range(5):
        bh1745.set_leds(1)
        time.sleep(0.2)
        bh1745.set_leds(0)
        time.sleep(0.05)
    bh1745.set_leds(0)


def on():
    bh1745.set_leds(1)


def off():
    bh1745.set_leds(0)


def get_measurement():
    try:
        result = bh1745.get_rgb_scaled()
        local_data_gateway.post_metrics_update('rgb', 'ok')
        return result
    except Exception as exception:
        logger.error(f' Unable to take measurement from uv sensor due to {exception}')
        local_data_gateway.post_metrics_update('rgb', 'errors')
        # TODO add reboot sensor
        return 0, 0, 0


def switch_led(led_status):
    bh1745.set_leds(led_status)
    if led_status == 1:
        return 0
    else:
        return 1
