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

from scd4x import SCD4X

logger = logging.getLogger('app')


def setup():
    logger.debug("Setting up CO2 Sensor")
    device = SCD4X(quiet=False)
    device.start_periodic_measurement()
    return device


co2_sensor = setup()


def get_measurement():
    try:
        result = co2_sensor.measure()
        logger.debug(result)
        return result  # co2, temperature, relative_humidity, timestamp
    except Exception as exception:
        logger.error(
            f'Unable to read data from scd4x (co2 sensor) sensor due to {type(exception).__name__} throws : {exception}',
            exc_info=True)
        setup()
        raise exception
