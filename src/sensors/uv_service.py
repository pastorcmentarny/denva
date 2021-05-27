#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import logging

import smbus
import veml6075

from gateways import local_data_gateway

bus = smbus.SMBus(1)

logger = logging.getLogger('app')
# Set up UV sensor
uv_sensor = veml6075.VEML6075(i2c_dev=bus)
uv_sensor.set_shutdown(False)
uv_sensor.set_high_dynamic_range(False)
uv_sensor.set_integration_time('100ms')


def get_measurements():
    try:
        uva, uvb = uv_sensor.get_measurements()
        uv_comp1, uv_comp2 = uv_sensor.get_comparitor_readings()
        local_data_gateway.post_metrics_update('uv', 'ok')
        return uv_sensor.convert_to_index(uva, uvb, uv_comp1, uv_comp2)
    except Exception as exception:
        logger.error(f' Unable to take measurement from uv sensor due to {exception}')
        local_data_gateway.post_metrics_update('uv', 'errors')
        # TODO add reboot sensor
        return 0, 0, 0
