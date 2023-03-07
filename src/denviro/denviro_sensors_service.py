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
from datetime import datetime

import config as config
from common import commands
import dom_utils


def get_sensor_log_file():
    return config.PI_DATA_PATH + dom_utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def get_last_measurement():
    entry = commands.get_last_line_from_log(get_sensor_log_file())
    data = entry.split(',')
    return get_data_row(data)


def get_data_row(row) -> dict:
    data_row = {
        config.FIELD_TIMESTAMP: row[0],
        config.FIELD_TEMPERATURE: '{:0.1f}'.format(float(row[1])),  # unit = "C"
        config.FIELD_OXIDISED: '{:0.2f}'.format(float(row[6])),  # config.FIELD_OXIDISED    unit = "kO"
        config.FIELD_REDUCED: '{:0.2f}'.format(float(row[7])),  # unit = "kO"
        config.FIELD_NH3: '{:0.2f}'.format(float(row[8])),  # unit = "kO"
        config.FIELD_PM1: row[9],  # unit = "ug/m3"
        config.FIELD_PM25: row[10],  # unit = "ug/m3"
        config.FIELD_PM10: row[11],  # unit = "ug/m3"
        config.FIELD_MEASUREMENT_TIME: row[12],
        config.FIELD_CPU_TEMP: row[13],
        config.FIELD_LIGHT: '{:0.1f}'.format(float(row[4])),
    }
    return data_row
