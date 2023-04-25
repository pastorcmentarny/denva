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

from bme280 import BME280

import config
from common import commands
from gateways import local_data_gateway

logger = logging.getLogger('app')
bme280 = BME280()

cpu_temps = []
factor = 0.8
temps = []


def warm_up():
    global cpu_temps
    global temps
    cpu_temps = [commands.get_cpu_temp_as_number()] * config.get_warm_up_measurement_counter()
    temps = [get_temperature()] * config.get_warm_up_measurement_counter()


def get_temperature() -> int:
    try:
        return bme280.get_temperature()
    except Exception as bme_exception:
        logger.error(
            f'Unable to read data from bme280 (humidity) sensor due to {type(bme_exception).__name__} throws : {bme_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('humidity', 'errors')
        return -1


def get_pressure():
    try:
        return bme280.get_pressure()
    except Exception as bme_exception:
        logger.error(
            f'Unable to read data from bme280 (humidity) sensor due to {type(bme_exception).__name__} throws : {bme_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('humidity', 'errors')
        return -1


def get_humidity():
    try:
        return bme280.get_humidity()
    except Exception as bme_exception:
        logger.error(
            f'Unable to read data from bme280 (humidity) sensor due to {type(bme_exception).__name__} throws : {bme_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('humidity', 'errors')
        return -1


# TODO add altitude
# TODO provide sea level pressure
def get_altitude():
    try:
        return bme280.get_altitude()
    except Exception as bme_exception:
        logger.error(
            f'Unable to read data from bme280 (humidity) sensor due to {type(bme_exception).__name__} throws : {bme_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('light', 'errors')
        return -1
