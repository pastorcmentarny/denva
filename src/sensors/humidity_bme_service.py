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

from bme280 import BME280

import config_service
from common import commands

bme280 = BME280()

cpu_temps = []
factor = 0.8
temps = []


def warm_up():
    global cpu_temps
    global temps
    cpu_temps = [commands.get_cpu_temp_as_number()] * config_service.get_warm_up_measurement_counter()
    temps = [get_temperature()] * config_service.get_warm_up_measurement_counter()


def get_temperature() -> int:
    return bme280.get_temperature()


def get_pressure():
    return bme280.get_pressure()


def get_humidity():
    return bme280.get_humidity()


# TODO add altitude
# TODO provide sea level pressure
def get_altitude():
    return bme280.get_altitude()
