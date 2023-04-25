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
import config
import bme680

from gateways import local_data_gateway

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
        local_data_gateway.post_metrics_update('weather', 'ok')
        return {
            config.FIELD_TEMPERATURE: weather_sensor.data.temperature,
            config.FIELD_PRESSURE: weather_sensor.data.pressure,
            config.FIELD_HUMIDITY: weather_sensor.data.humidity,
            config.FIELD_GAS_RESISTANCE: weather_sensor.data.gas_resistance
        }
    else:
        logger.warning("Weather sensor didn't return data")
        local_data_gateway.post_metrics_update('weather', 'errors')
        return {
            config.FIELD_TEMPERATURE: 0,
            config.FIELD_PRESSURE: 0,
            config.FIELD_HUMIDITY: 0,
            config.FIELD_GAS_RESISTANCE: 0
        }
