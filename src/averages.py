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
from timeit import default_timer as timer


import sensor_log_reader


def get_averages_for_today() -> dict:
    return get_averages(sensor_log_reader.load_data_for_today())

def get_enviro_averages_for_today() -> dict:
    return get_enviro_averages(sensor_log_reader.load_enviro_data_for_today())

def get_enviro_averages(data_records: list) -> dict:
    start_time = timer()
    result = {
        'temperature': 0,
        'light': 0,
        'oxidised': 0,
        'reduced': 0,
        'nh3': 0,
        'pm1': 0,
        'pm25': 0,
        'pm10':  0,
        'measurement_time': 0
    }

    temperature = 0
    light = 0
    oxidised = 0
    reduced = 0
    nh3 = 0
    pm1 = 0
    pm25 = 0
    pm10 = 0
    measurement_time = 0

    for data_record in data_records:
        temperature += float(data_record['temperature'])
        light += float(data_record['light'])
        oxidised += float(data_record['oxidised'])
        reduced += float(data_record['reduced'])
        nh3 += float(data_record['nh3'])
        pm1 += float(data_record['pm1'])
        pm25 += float(data_record['pm25'])
        pm10 += float(data_record['pm10'])
        measurement_time += float(data_record['measurement_time'])

    records = len(data_records)
    if records != 0:
        result['temperature'] = '{:.2f}'.format(temperature / records)
        result['light'] = '{:.2f}'.format(light / records)
        result['oxidised'] = '{:.2f}'.format(oxidised / records)
        result['reduced'] = '{:.2f}'.format(reduced / records)
        result['nh3'] = '{:.2f}'.format(nh3 / records)
        result['pm1'] = '{:.2f}'.format(pm1 / records)
        result['pm25'] = '{:.2f}'.format(pm25 / records)
        result['pm10'] = '{:.2f}'.format(pm10 / records)
        result['measurement_time'] = '{:.2f}'.format(measurement_time / records)
    else:
        result['info'] = 'No records'
    end_time = timer()
    result['execution_time'] = str(end_time - start_time) + ' ns.' #TODO FIXME  "execution_time": "0.15859715300007338 ns.",
    return result


def get_averages(data_records) -> dict:
    start = time.time_ns()
    result = {
        'temperature': 0,
        'pressure': 0,
        'humidity': 0,
        'gas_resistance': 0,
        'uva': 0,
        'uvb': 0,
        'cpu_temperature': 0,
        'motion': 0,
        'measurement_time': 0
    }

    temperature = 0
    pressure = 0
    humidity = 0
    gas_resistance = 0
    uva = 0
    uvb = 0
    cpu_temperature = 0
    motion = 0
    measurement_time = 0

    for data_record in data_records:
        temperature += float(data_record['temp'])
        pressure += float(data_record['pressure'])
        humidity += float(data_record['humidity'])
        cpu_temperature += float(re.sub('[^0-9.]', '', data_record['cpu_temp']))
        gas_resistance += float(data_record['gas_resistance'])
        uva += float(data_record['uva_index'])
        uvb += float(data_record['uvb_index'])
        motion += float(data_record['motion'])
        # TODO remove it as this temporary due to other bug in v2
        try:
            measurement_time += float(re.sub('[^0-9.]', '', data_record['measurement_time']))
        except ValueError:
            measurement_time += float(1000)
    records = len(data_records)
    if records != 0:
        result['temperature'] = '{:.2f}'.format(temperature / records)
        result['pressure'] = '{:.2f}'.format(pressure / records)
        result['humidity'] = '{:.2f}'.format(humidity / records)
        result['gas_resistance'] = '{:.2f}'.format(gas_resistance / records)
        result['uva'] = '{:.2f}'.format(uva / records)
        result['uvb'] = '{:.2f}'.format(uvb / records)
        result['cpu_temperature'] = '{:.2f}'.format(cpu_temperature / records)
        result['motion'] = '{:.2f}'.format(motion / records)
        result['measurement_time'] = '{:.2f}'.format(measurement_time / records)
    else:
        result['info'] = 'No records'
    end = time.time_ns()
    result['execution_time'] = str(end - start) + ' ns.'
    return result
