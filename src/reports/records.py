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
import re
import time

import config
from common import data_files
from denva import denva_sensors_service


def get_records_for_today() -> dict:
    return get_records(denva_sensors_service.load_data_for_today())


def get_enviro_records_for_today() -> dict:
    return get_enviro_records(data_files.load_enviro_data_for_today())


def get_enviro_records(data_records: list) -> dict:
    start = time.perf_counter()
    result = {
        config.FIELD_TEMPERATURE: {
            'min': 1000,
            'max': -1000
        },
        'highest_light': 0,
        'highest_oxidised': 0,
        'highest_reduced': 0,
        'highest_nh3': 0,
        'highest_pm1': 0,
        'highest_pm25': 0,
        'highest_pm10': 0,
        config.FIELD_MEASUREMENT_TIME: {
            'min': 100000000,
            'max': -1
        }
    }

    for data_record in data_records:
        if float(data_record[config.FIELD_TEMPERATURE]) > float(result[config.FIELD_TEMPERATURE]['max']):
            result[config.FIELD_TEMPERATURE]['max'] = data_record[config.FIELD_TEMPERATURE]
        if float(data_record[config.FIELD_TEMPERATURE]) < float(result[config.FIELD_TEMPERATURE]['min']):
            result[config.FIELD_TEMPERATURE]['min'] = data_record[config.FIELD_TEMPERATURE]

        if float(data_record[config.FIELD_LIGHT]) > float(result['highest_light']):
            result['highest_light'] = data_record[config.FIELD_LIGHT]

        if float(data_record[config.FIELD_NH3]) > float(result['highest_nh3']):
            result['highest_nh3'] = data_record[config.FIELD_NH3]

        if float(data_record[config.FIELD_OXIDISED]) > float(result['highest_oxidised']):
            result['highest_oxidised'] = data_record[config.FIELD_OXIDISED]

        if float(data_record[config.FIELD_REDUCED]) > float(result['highest_reduced']):
            result['highest_reduced'] = data_record[config.FIELD_REDUCED]

        if float(data_record[config.FIELD_PM1]) > float(result['highest_pm1']):
            result['highest_pm1'] = data_record[config.FIELD_PM1]

        if float(data_record[config.FIELD_PM25]) > float(result['highest_pm25']):
            result['highest_pm25'] = data_record[config.FIELD_PM25]

        if float(data_record[config.FIELD_PM10]) > float(result['highest_pm10']):
            result['highest_pm10'] = data_record[config.FIELD_PM10]

        if float(data_record[config.FIELD_MEASUREMENT_TIME]) > float(result[config.FIELD_MEASUREMENT_TIME]['max']):
            result[config.FIELD_MEASUREMENT_TIME]['max'] = data_record[config.FIELD_MEASUREMENT_TIME]
        if float(data_record[config.FIELD_MEASUREMENT_TIME]) < float(result[config.FIELD_MEASUREMENT_TIME]['min']):
            result[config.FIELD_MEASUREMENT_TIME]['min'] = data_record[config.FIELD_MEASUREMENT_TIME]

    end = time.perf_counter()
    result['log entries counter'] = len(data_records)
    result["execution_time"] = str(end - start) + ' ns.'
    return result


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
        'max_uv_index': {
            'uva': -100,
            'uvb': -100
        },
        config.FIELD_CPU_TEMP: {
            'min': 100,
            'max': -100
        },
        'biggest_motion': 0,
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

        result['biggest_motion'] = str(int((float(result['biggest_motion']))))

        if int(data_record[config.FIELD_ECO2]) > int(result['highest_eco2']):
            result['highest_eco2'] = data_record[config.FIELD_ECO2]

        if int(data_record[config.FIELD_TVOC]) > int(result['highest_tvoc']):
            result['highest_tvoc'] = data_record[config.FIELD_TVOC]
        if int(data_record[config.FIELD_GPS_NUM_SATS]) > int(float(result['highest_gps_num_sats'])):
            result['highest_gps_num_sats'] = int(data_record[config.FIELD_GPS_NUM_SATS])
    end = time.perf_counter()
    result['log entries counter'] = len(data_records)
    result["execution_time"] = str(end - start) + ' ns.'
    return result
