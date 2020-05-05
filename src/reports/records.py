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
import re

import time

from common import data_files
from denva import denva_sensors_service


def get_records_for_today() -> dict:
    return get_records(denva_sensors_service.load_data_for_today())


def get_enviro_records_for_today() -> dict:
    return get_enviro_records(data_files.load_enviro_data_for_today())


def get_enviro_records(data_records: list) -> dict:
    start = time.time_ns()
    result = {
        'temperature': {
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
        'measurement_time': {
            'min': 100000000,
            'max': -1
        }
    }

    for data_record in data_records:
        if float(data_record['temperature']) > float(result['temperature']['max']):
            result['temperature']['max'] = data_record['temperature']
        if float(data_record['temperature']) < float(result['temperature']['min']):
            result['temperature']['min'] = data_record['temperature']

        if float(data_record['light']) > float(result['highest_light']):
            result['highest_light'] = data_record['light']

        if float(data_record['nh3']) > float(result['highest_nh3']):
            result['highest_nh3'] = data_record['nh3']

        if float(data_record['oxidised']) > float(result['highest_oxidised']):
            result['highest_oxidised'] = data_record['oxidised']

        if float(data_record['reduced']) > float(result['highest_reduced']):
            result['highest_reduced'] = data_record['reduced']

        if float(data_record['pm1']) > float(result['highest_pm1']):
            result['highest_pm1'] = data_record['pm1']

        if float(data_record['pm25']) > float(result['highest_pm25']):
            result['highest_pm25'] = data_record['pm25']

        if float(data_record['pm10']) > float(result['highest_pm10']):
            result['highest_pm10'] = data_record['pm10']

        if float(data_record['measurement_time']) > float(result['measurement_time']['max']):
            result['measurement_time']['max'] = data_record['measurement_time']
        if float(data_record['measurement_time']) < float(result['measurement_time']['min']):
            result['measurement_time']['min'] = data_record['measurement_time']

    end = time.time_ns()
    result['log entries counter'] = len(data_records)
    result["execution_time"] = str(end - start) + ' ns.'
    return result


def get_records(data_records: list) -> dict:
    start = time.time_ns()
    result = {
        'temperature': {
            'min': 100,
            'max': -100
        },
        'pressure': {
            'min': 10000,
            'max': 0
        },
        'humidity': {
            'min': 100,
            'max': -100
        },
        'max_uv_index': {
            'uva': -100,
            'uvb': -100
        },
        'cpu_temperature': {
            'min': 100,
            'max': -100
        },
        'biggest_motion': 0,
        'highest_eco2': 0,
        'highest_tvoc': 0
    }

    for data_record in data_records:
        if float(data_record['temp']) > float(result['temperature']['max']):
            result['temperature']['max'] = data_record['temp']
        if float(data_record['temp']) < float(result['temperature']['min']):
            result['temperature']['min'] = data_record['temp']

        if float(data_record['pressure']) > float(result['pressure']['max']):
            result['pressure']['max'] = data_record['pressure']
        if float(data_record['pressure']) < float(result['pressure']['min']):
            result['pressure']['min'] = data_record['pressure']

        if float(data_record['humidity']) > float(result['humidity']['max']):
            result['humidity']['max'] = data_record['humidity']
        if float(data_record['humidity']) < float(result['humidity']['min']):
            result['humidity']['min'] = data_record['humidity']

        if data_record['cpu_temp'] != '?':
            data_record['cpu_temp'] = re.sub('[^0-9.]', '', data_record['cpu_temp'])
            if float(data_record['cpu_temp']) > float(result['cpu_temperature']['max']):
                result['cpu_temperature']['max'] = data_record['cpu_temp']
            if float(data_record['cpu_temp']) < float(result['cpu_temperature']['min']):
                result['cpu_temperature']['min'] = data_record['cpu_temp']

        if float(data_record['uva_index']) > float(result['max_uv_index']['uva']):
            result['max_uv_index']['uva'] = data_record['uva_index']

        if float(data_record['uvb_index']) > float(result['max_uv_index']['uvb']):
            result['max_uv_index']['uvb'] = data_record['uvb_index']

        if float(data_record['motion']) > float(result['biggest_motion']):
            result['biggest_motion'] = data_record['motion']

        result['max_uv_index']['uva'] = round(float(result['max_uv_index']['uva']), 2)
        result['max_uv_index']['uvb'] = round(float(result['max_uv_index']['uvb']), 2)
        result['biggest_motion'] = str(int((float(result['biggest_motion']))))

        if int(data_record['eco2']) > int(result['highest_eco2']):
            result['highest_eco2'] = data_record['eco2']

        if int(data_record['tvoc']) > int(result['highest_tvoc']):
            result['highest_tvoc'] = data_record['tvoc']

    end = time.time_ns()
    result['log entries counter'] = len(data_records)
    result["execution_time"] = str(end - start) + ' ns.'
    return result
