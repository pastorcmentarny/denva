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
from timeit import default_timer as timer

import time
import config
from common import data_files
from denva import denva_sensors_service

config.FIELD_TEMPERATURE = 'temp'


def get_averages_for_today() -> dict:
    return get_averages(denva_sensors_service.load_data_for_today())


def get_enviro_averages_for_today() -> dict:
    return get_enviro_averages(data_files.load_enviro_data_for_today())


def get_enviro_averages(data_records: list) -> dict:
    start_time = timer()
    result = {
        config.FIELD_TEMPERATURE: 0,
        config.FIELD_LIGHT: 0,
        config.FIELD_OXIDISED: 0,
        config.FIELD_REDUCED: 0,
        config.FIELD_NH3: 0,
        config.FIELD_PM1: 0,
        config.FIELD_PM25: 0,
        config.FIELD_PM10: 0,
        config.FIELD_MEASUREMENT_TIME: 0
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
        temperature += float(data_record[config.FIELD_TEMPERATURE])
        light += float(data_record[config.FIELD_LIGHT])
        oxidised += float(data_record[config.FIELD_OXIDISED])
        reduced += float(data_record[config.FIELD_REDUCED])
        nh3 += float(data_record[config.FIELD_NH3])
        pm1 += float(data_record[config.FIELD_PM1])
        pm25 += float(data_record[config.FIELD_PM25])
        pm10 += float(data_record[config.FIELD_PM10])
        measurement_time += float(data_record[config.FIELD_MEASUREMENT_TIME])

    records = len(data_records)
    if records != 0:
        result[config.FIELD_TEMPERATURE] = '{:.2f}'.format(temperature / records)
        result[config.FIELD_LIGHT] = '{:.2f}'.format(light / records)
        result[config.FIELD_OXIDISED] = '{:.2f}'.format(oxidised / records)
        result[config.FIELD_REDUCED] = '{:.2f}'.format(reduced / records)
        result[config.FIELD_NH3] = '{:.2f}'.format(nh3 / records)
        result[config.FIELD_PM1] = '{:.2f}'.format(pm1 / records)
        result[config.FIELD_PM25] = '{:.2f}'.format(pm25 / records)
        result[config.FIELD_PM10] = '{:.2f}'.format(pm10 / records)
        result[config.FIELD_MEASUREMENT_TIME] = '{:.2f}'.format(measurement_time / records)
    else:
        result['info'] = 'No records'
    end_time = timer()
    result['execution_time'] = str(
        end_time - start_time) + ' ns.'  # TODO FIXME  "execution_time": "0.15859715300007338 ns.",
    return result


def get_averages(data_records) -> dict:
    start = time.perf_counter()
    result = {
        config.FIELD_TEMPERATURE: 0,
        config.FIELD_PRESSURE: 0,
        config.FIELD_HUMIDITY: 0,
        config.FIELD_GAS_RESISTANCE: 0,
        config.FIELD_CPU_TEMP: 0,
        config.FIELD_MEASUREMENT_TIME: 0
    }

    temperature = 0
    pressure = 0
    humidity = 0
    gas_resistance = 0
    cpu_temperature = 0
    measurement_time = 0

    for data_record in data_records:
        temperature += float(data_record[config.FIELD_TEMPERATURE])
        pressure += float(data_record[config.FIELD_PRESSURE])
        humidity += float(data_record[config.FIELD_HUMIDITY])
        cpu_temperature += float(re.sub('[^0-9.]', '', data_record[config.FIELD_CPU_TEMP]))
        gas_resistance += float(data_record[config.FIELD_GAS_RESISTANCE])

        # TODO remove it as this temporary due to other bug in v2
        try:
            measurement_time += float(re.sub('[^0-9.]', '', data_record[config.FIELD_MEASUREMENT_TIME]))
        except ValueError:
            measurement_time += float(1000)
    records = len(data_records)
    if records != 0:
        result[config.FIELD_TEMPERATURE] = '{:.2f}'.format(temperature / records)
        result[config.FIELD_PRESSURE] = '{:.2f}'.format(pressure / records)
        result[config.FIELD_HUMIDITY] = '{:.2f}'.format(humidity / records)
        result[config.FIELD_GAS_RESISTANCE] = '{:.2f}'.format(gas_resistance / records)
        result[config.FIELD_CPU_TEMP] = '{:.2f}'.format(cpu_temperature / records)
        result[config.FIELD_MEASUREMENT_TIME] = '{:.2f}'.format(measurement_time / records)
    else:
        result['info'] = 'No records'  # TODO check how is it used
    end = time.perf_counter()
    result['execution_time'] = str(end - start) + ' s.'  # TODO check how is it used
    return result
