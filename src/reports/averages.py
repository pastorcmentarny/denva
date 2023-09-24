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
from denva import denva_sensors_service

logger = logging.getLogger('app')


def get_averages_for_today() -> dict:
    return get_averages(denva_sensors_service.load_data_for_today())


def get_averages(data_records) -> dict:
    start = time.perf_counter()
    result = {
        config.FIELD_TEMPERATURE: 0,
        config.FIELD_CO2_TEMPERATURE: 0,
        config.FIELD_PRESSURE: 0,
        config.FIELD_HUMIDITY: 0,
        config.FIELD_RELATIVE_HUMIDITY: 0,
        config.FIELD_GAS_RESISTANCE: 0,
        config.FIELD_CPU_TEMP: 0,
        config.FIELD_MEASUREMENT_TIME: 0,
        config.FIELD_ECO2: 0,
        config.FIELD_TVOC: 0
    }

    temperature = 0
    co2_temperature = 0
    pressure = 0
    humidity = 0
    relative_humidity = 0
    gas_resistance = 0
    cpu_temperature = 0
    measurement_time = 0
    eco2 = 0
    tvoc = 0

    for data_record in data_records:
        temperature += float(data_record[config.FIELD_TEMPERATURE])
        co2_temperature += float(data_record[config.FIELD_CO2_TEMPERATURE])
        pressure += float(data_record[config.FIELD_PRESSURE])
        humidity += float(data_record[config.FIELD_HUMIDITY])
        relative_humidity += float(data_record[config.FIELD_RELATIVE_HUMIDITY])
        cpu_temperature += float(re.sub('[^0-9.]', '', data_record[config.FIELD_CPU_TEMP]))
        gas_resistance += float(data_record[config.FIELD_GAS_RESISTANCE])
        eco2 += float(data_record[config.FIELD_ECO2])
        tvoc += float(data_record[config.FIELD_TVOC])

        # TODO remove it as this temporary due to other bug in v2
        try:
            measurement_time += float(re.sub('[^0-9.]', '', data_record[config.FIELD_MEASUREMENT_TIME]))
        except ValueError:
            measurement_time += float(1000)
    records = len(data_records)
    if records != 0:
        result[config.FIELD_TEMPERATURE] = '{:.2f}'.format(temperature / records)
        result[config.FIELD_CO2_TEMPERATURE] = '{:.2f}'.format(co2_temperature / records)
        result[config.FIELD_PRESSURE] = '{:.2f}'.format(pressure / records)
        result[config.FIELD_HUMIDITY] = '{:.2f}'.format(humidity / records)
        result[config.FIELD_RELATIVE_HUMIDITY] = '{:.2f}'.format(relative_humidity / records)
        result[config.FIELD_GAS_RESISTANCE] = '{:.2f}'.format(gas_resistance / records)
        result[config.FIELD_ECO2] = '{:.2f}'.format(eco2 / records)
        result[config.FIELD_TVOC] = '{:.2f}'.format(tvoc / records)
        result[config.FIELD_CPU_TEMP] = '{:.2f}'.format(cpu_temperature / records)
        result[config.FIELD_MEASUREMENT_TIME] = '{:.2f}'.format(measurement_time / records)
    else:
        result['info'] = 'No records'  # TODO check how is it used
    end = time.perf_counter()
    result['execution_time'] = str(end - start) + ' s.'  # TODO check how is it used
    return result
