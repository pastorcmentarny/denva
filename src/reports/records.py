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
from common import data_files
from denva import denva_sensors_service

logger = logging.getLogger('app')


def get_records_for_today() -> dict:
    return get_records(denva_sensors_service.load_data_for_today())


# noinspection PyTypeChecker
def get_records(data_records: list) -> dict:
    start = time.perf_counter()
    result = {
        config.FIELD_TEMPERATURE: {
            'min': 100,
            'max': -100
        },
        config.FIELD_CO2_TEMPERATURE: {
            'min': 100,
            'max': -100
        },
        config.FIELD_PRESSURE: {
            'min': 10000,
            'max': 0
        },
        config.FIELD_HUMIDITY: {
            'min': 100,
            'max': -100
        },
        config.FIELD_RELATIVE_HUMIDITY: {
            'min': 100,
            'max': -100
        },
        config.FIELD_CPU_TEMP: {
            'min': 100,
            'max': -100
        },
        'highest_eco2': 0,
        'highest_tvoc': 0,
        'highest_gps_num_sats': 0
    }

    for data_record in data_records:
        if float(data_record[config.FIELD_TEMPERATURE]) > float(result[config.FIELD_TEMPERATURE]['max']):
            result[config.FIELD_TEMPERATURE]['max'] = data_record[config.FIELD_TEMPERATURE]
        if float(data_record[config.FIELD_TEMPERATURE]) < float(result[config.FIELD_TEMPERATURE]['min']):
            result[config.FIELD_TEMPERATURE]['min'] = data_record[config.FIELD_TEMPERATURE]

        if float(data_record[config.FIELD_CO2_TEMPERATURE]) > float(result[config.FIELD_CO2_TEMPERATURE]['max']):
            result[config.FIELD_CO2_TEMPERATURE]['max'] = data_record[config.FIELD_CO2_TEMPERATURE]
        if float(data_record[config.FIELD_CO2_TEMPERATURE]) < float(result[config.FIELD_CO2_TEMPERATURE]['min']):
            result[config.FIELD_CO2_TEMPERATURE]['min'] = data_record[config.FIELD_CO2_TEMPERATURE]

        if float(data_record[config.FIELD_PRESSURE]) > float(result[config.FIELD_PRESSURE]['max']):
            result[config.FIELD_PRESSURE]['max'] = data_record[config.FIELD_PRESSURE]
        if float(data_record[config.FIELD_PRESSURE]) < float(result[config.FIELD_PRESSURE]['min']):
            result[config.FIELD_PRESSURE]['min'] = data_record[config.FIELD_PRESSURE]

        if float(data_record[config.FIELD_HUMIDITY]) > float(result[config.FIELD_HUMIDITY]['max']):
            result[config.FIELD_HUMIDITY]['max'] = data_record[config.FIELD_HUMIDITY]
        if float(data_record[config.FIELD_HUMIDITY]) < float(result[config.FIELD_HUMIDITY]['min']):
            result[config.FIELD_HUMIDITY]['min'] = data_record[config.FIELD_HUMIDITY]

        if float(data_record[config.FIELD_RELATIVE_HUMIDITY]) > float(result[config.FIELD_RELATIVE_HUMIDITY]['max']):
            result[config.FIELD_RELATIVE_HUMIDITY]['max'] = data_record[config.FIELD_RELATIVE_HUMIDITY]
        if float(data_record[config.FIELD_RELATIVE_HUMIDITY]) < float(result[config.FIELD_RELATIVE_HUMIDITY]['min']):
            result[config.FIELD_RELATIVE_HUMIDITY]['min'] = data_record[config.FIELD_RELATIVE_HUMIDITY]

        if data_record[config.FIELD_CPU_TEMP] != '?':
            data_record[config.FIELD_CPU_TEMP] = re.sub('[^0-9.]', '', data_record[config.FIELD_CPU_TEMP])
            if float(data_record[config.FIELD_CPU_TEMP]) > float(result[config.FIELD_CPU_TEMP]['max']):
                result[config.FIELD_CPU_TEMP]['max'] = data_record[config.FIELD_CPU_TEMP]
            if float(data_record[config.FIELD_CPU_TEMP]) < float(result[config.FIELD_CPU_TEMP]['min']):
                result[config.FIELD_CPU_TEMP]['min'] = data_record[config.FIELD_CPU_TEMP]

        if int(data_record[config.FIELD_ECO2]) > int(result['highest_eco2']):
            result['highest_eco2'] = data_record[config.FIELD_ECO2]

        if int(data_record[config.FIELD_TVOC]) > int(result['highest_tvoc']):
            result['highest_tvoc'] = data_record[config.FIELD_TVOC]

    end = time.perf_counter()
    result['log entries counter'] = len(data_records)
    result["execution_time"] = str(end - start) + ' ns.'
    return result
