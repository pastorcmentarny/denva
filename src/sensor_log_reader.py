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
import csv
import logging
from datetime import datetime

import config_service as config
import utils
from denva import denva_sensors_service
from denviro import denviro_sensors_service

logger = logging.getLogger('server')


def get_enviro_sensor_log_file() -> str:
    return denviro_sensors_service.get_sensor_log_file()


def get_sensor_log_file_at_server() -> str:
    return config.NETWORK_PATH + 'denva/' + utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def get_enviro_sensor_log_file_at_server() -> str:
    return config.NETWORK_PATH + 'enviro/' + utils.get_date_as_filename('sensor-enviro-log', 'csv', datetime.now())


def load_data_for_today() -> list:
    today = datetime.now()
    return load_data(today.year, today.month, today.day)


# TODO move this to different place
def load_data(year: int, month: int, day: int) -> list:
    sensor_log_file = utils.fix_nulls(
        open(config.get_sensor_log_file_for(year, month, day), 'r', newline='', encoding='utf-8'))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []
    for row in csv_data:
        try:
            row[19] == '?'
        except IndexError:
            row.insert(19, '?')
            row.insert(20, '?')
        try:
            row[21] == '?'
        except IndexError:
            row.insert(21, '?')
            row.insert(22, '?')
        add_row(data, row)
    sensor_log_file.close()
    return data


def add_row(data, row):
    data.append(
        {
            'timestamp': row[0],
            'temp': row[1],
            'pressure': row[2],
            'humidity': row[3],
            'gas_resistance': row[4],
            'colour': row[5],
            'aqi': row[6],
            'uva_index': row[7],
            'uvb_index': row[8],
            'motion': row[9],
            'ax': row[10],
            'ay': row[11],
            'az': row[12],
            'gx': row[13],
            'gy': row[14],
            'gz': row[15],
            'mx': row[16],
            'my': row[17],
            'mz': row[18],
            'measurement_time': row[19],
            'cpu_temp': row[20],
            'eco2': row[21],
            'tvoc': row[22]
        }
    )


def get_last_measurement() -> dict:
    return denva_sensors_service.get_last_measurement()


def get_last_enviro_measurement() -> dict:
    return denviro_sensors_service.get_last_measurement()
