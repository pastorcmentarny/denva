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

import bme680

TEMP_OFFSET = 0.0

logger = logging.getLogger('app')

# Set up weather sensor
weather_sensor = bme680.BME680()
weather_sensor.set_humidity_oversample(bme680.OS_2X)
weather_sensor.set_pressure_oversample(bme680.OS_4X)
weather_sensor.set_temperature_oversample(bme680.OS_8X)
weather_sensor.set_filter(bme680.FILTER_SIZE_3)
weather_sensor.set_temp_offset(TEMP_OFFSET)


def get_measurement():
    if weather_sensor.get_sensor_data():
        return {
            'temp': weather_sensor.data.temperature,
            'pressure': weather_sensor.data.pressure,
            'humidity': weather_sensor.data.humidity,
            'gas_resistance': weather_sensor.data.gas_resistance
        }
    else:
        logger.warning("Weather sensor did't return data")
        return {
            'temp': 0,
            'pressure': 0,
            'humidity': 0,
            'gas_resistance': 0
        }
