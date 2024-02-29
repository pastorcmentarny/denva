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
import re
import time

import config
from services import denva_sensors_service

MAX_VALUE_KEY = 'max'

MIN_VALUE_KEY = 'min'

logger = logging.getLogger('app')


def get_records_for_today() -> dict:
    return get_records(denva_sensors_service.load_data_for_today())


# noinspection PyTypeChecker
def get_records(data_records: list) -> dict:
    start = time.perf_counter()
    result = {
        config.FIELD_TEMPERATURE: {
            MIN_VALUE_KEY: 100,
            MAX_VALUE_KEY: -100
        },
        config.FIELD_CO2_TEMPERATURE: {
            MIN_VALUE_KEY: 100,
            MAX_VALUE_KEY: -100
        },
        config.FIELD_PRESSURE: {
            MIN_VALUE_KEY: 10000,
            MAX_VALUE_KEY: 0
        },
        config.FIELD_HUMIDITY: {
            MIN_VALUE_KEY: 100,
            MAX_VALUE_KEY: -100
        },
        config.FIELD_RELATIVE_HUMIDITY: {
            MIN_VALUE_KEY: 100,
            MAX_VALUE_KEY: -100
        },
        config.FIELD_CPU_TEMP: {
            MIN_VALUE_KEY: 100,
            MAX_VALUE_KEY: -100
        },
        'highest_eco2': 0,
        'highest_tvoc': 0,
        'highest_gps_num_sats': 0
    }

    for data_record in data_records:
        if float(data_record[config.FIELD_TEMPERATURE]) > float(result[config.FIELD_TEMPERATURE][MAX_VALUE_KEY]):
            result[config.FIELD_TEMPERATURE][MAX_VALUE_KEY] = data_record[config.FIELD_TEMPERATURE]
        if float(data_record[config.FIELD_TEMPERATURE]) < float(result[config.FIELD_TEMPERATURE][MIN_VALUE_KEY]):
            result[config.FIELD_TEMPERATURE][MIN_VALUE_KEY] = data_record[config.FIELD_TEMPERATURE]

        if float(data_record[config.FIELD_CO2_TEMPERATURE]) > float(
                result[config.FIELD_CO2_TEMPERATURE][MAX_VALUE_KEY]):
            result[config.FIELD_CO2_TEMPERATURE][MAX_VALUE_KEY] = data_record[config.FIELD_CO2_TEMPERATURE]
        if float(data_record[config.FIELD_CO2_TEMPERATURE]) < float(
                result[config.FIELD_CO2_TEMPERATURE][MIN_VALUE_KEY]):
            result[config.FIELD_CO2_TEMPERATURE][MIN_VALUE_KEY] = data_record[config.FIELD_CO2_TEMPERATURE]

        if float(data_record[config.FIELD_PRESSURE]) > float(result[config.FIELD_PRESSURE][MAX_VALUE_KEY]):
            result[config.FIELD_PRESSURE][MAX_VALUE_KEY] = data_record[config.FIELD_PRESSURE]
        if float(data_record[config.FIELD_PRESSURE]) < float(result[config.FIELD_PRESSURE][MIN_VALUE_KEY]):
            result[config.FIELD_PRESSURE][MIN_VALUE_KEY] = data_record[config.FIELD_PRESSURE]

        if float(data_record[config.FIELD_HUMIDITY]) > float(result[config.FIELD_HUMIDITY][MAX_VALUE_KEY]):
            result[config.FIELD_HUMIDITY][MAX_VALUE_KEY] = data_record[config.FIELD_HUMIDITY]
        if float(data_record[config.FIELD_HUMIDITY]) < float(result[config.FIELD_HUMIDITY][MIN_VALUE_KEY]):
            result[config.FIELD_HUMIDITY][MIN_VALUE_KEY] = data_record[config.FIELD_HUMIDITY]

        if float(data_record[config.FIELD_RELATIVE_HUMIDITY]) > float(
                result[config.FIELD_RELATIVE_HUMIDITY][MAX_VALUE_KEY]):
            result[config.FIELD_RELATIVE_HUMIDITY][MAX_VALUE_KEY] = data_record[config.FIELD_RELATIVE_HUMIDITY]
        if float(data_record[config.FIELD_RELATIVE_HUMIDITY]) < float(
                result[config.FIELD_RELATIVE_HUMIDITY][MIN_VALUE_KEY]):
            result[config.FIELD_RELATIVE_HUMIDITY][MIN_VALUE_KEY] = data_record[config.FIELD_RELATIVE_HUMIDITY]

        if data_record[config.FIELD_CPU_TEMP] != '?':
            data_record[config.FIELD_CPU_TEMP] = re.sub('[^0-9.]', '', data_record[config.FIELD_CPU_TEMP])
            if float(data_record[config.FIELD_CPU_TEMP]) > float(result[config.FIELD_CPU_TEMP][MAX_VALUE_KEY]):
                result[config.FIELD_CPU_TEMP][MAX_VALUE_KEY] = data_record[config.FIELD_CPU_TEMP]
            if float(data_record[config.FIELD_CPU_TEMP]) < float(result[config.FIELD_CPU_TEMP][MIN_VALUE_KEY]):
                result[config.FIELD_CPU_TEMP][MIN_VALUE_KEY] = data_record[config.FIELD_CPU_TEMP]

        if int(data_record[config.FIELD_ECO2]) > int(result['highest_eco2']):
            result['highest_eco2'] = data_record[config.FIELD_ECO2]

        if int(data_record[config.FIELD_TVOC]) > int(result['highest_tvoc']):
            result['highest_tvoc'] = data_record[config.FIELD_TVOC]

    end = time.perf_counter()
    result['log entries counter'] = len(data_records)
    result["execution_time"] = str(end - start) + ' ns.'
    return result
