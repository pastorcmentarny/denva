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
from datetime import datetime

import commands
import utils

PI_PATH = '/home/pi/logs/'
NETWORK_PATH = '/mnt/data/sensors/'


def get_sensor_log_file() -> str:
    return PI_PATH + utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def get_enviro_sensor_log_file() -> str:
    return PI_PATH + utils.get_date_as_filename('sensor-enviro-log', 'csv', datetime.now())


def get_sensor_log_file_at_server() -> str:
    return NETWORK_PATH + 'denva/' + utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def get_enviro_sensor_log_file_at_server() -> str:
    return NETWORK_PATH + 'enviro/' + utils.get_date_as_filename('sensor-enviro-log', 'csv', datetime.now())


def get_sensor_log_file_for(year: int, month: int, day: int,sensor_filename:str = 'sensor-log') -> str:
    path = '/home/pi/logs/' + utils.get_filename_from_year_month_day(sensor_filename, 'csv', year, month, day)
    return path


def load_data_for_today() -> list:
    today = datetime.now()
    return load_data(today.year, today.month, today.day)

def load_enviro_data_for_today() -> list:
    today = datetime.now()
    return load_enviro_data(today.year, today.month, today.day)

def load_enviro_data(year: int, month: int, day: int) -> list:
    sensor_log_file = utils.fix_nulls(
        open(get_sensor_log_file_for(year, month, day,'sensor-enviro-log'), 'r', newline='', encoding='utf-8'))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []
    for row in csv_data:
        try:
            row[12] == '?'
        except IndexError:
            row.insert(12, 0) #measurement time
        add_row(data, row)
    sensor_log_file.close()
    return data

#TODO move this to different place
def load_data(year: int, month: int, day: int) -> list:
    sensor_log_file = utils.fix_nulls(
        open(get_sensor_log_file_for(year, month, day), 'r', newline='', encoding='utf-8'))
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


def get_data_row(row) -> dict:
    data_row = {
        'timestamp': row[0],
        'temp': row[1],
        'pressure': row[2],
        'humidity': row[3],
        'gas_resistance': row[4],
        'colour': row[5],
        'aqi': row[6],
        'uva_index': '{:0.2f}'.format(float(row[7])),
        'uvb_index': '{:0.2f}'.format(float(row[8])),
        'motion': row[9],
        'ax': '{:0.2f}'.format(float(row[10])),
        'ay': '{:0.2f}'.format(float(row[11])),
        'az': '{:0.2f}'.format(float(row[12])),
        'gx': '{:0.2f}'.format(float(row[13])),
        'gy': '{:0.2f}'.format(float(row[14])),
        'gz': '{:0.2f}'.format(float(row[15])),
        'mx': '{:0.2f}'.format(float(row[16])),
        'my': '{:0.2f}'.format(float(row[17])),
        'mz': '{:0.2f}'.format(float(row[18])),
        'cpu_temp': commands.get_cpu_temp(),
        'eco2': row[21],
        'tvoc': row[22]
    }
    return data_row


def get_data_row_for_enviro(row) -> dict:
    data_row = {
        'timestamp': row[0],
        'temperature': '{:0.1f}'.format(float(row[1])),  # unit = "C"
        "oxidised": '{:0.2f}'.format(float(row[6])),  # "oxidised"    unit = "kO"
        'reduced': '{:0.2f}'.format(float(row[7])),  # unit = "kO"
        "nh3": '{:0.2f}'.format(float(row[8])),  # unit = "kO"
        "pm1": row[9],  # unit = "ug/m3"
        "pm25": row[10],  # unit = "ug/m3"
        "pm10": row[11],  # unit = "ug/m3"
        'cpu_temp': commands.get_cpu_temp(),
        'light': '{:0.1f}'.format(float(row[4])),
    }
    return data_row


def get_last_measurement() -> dict:
    entry = commands.get_last_line_from_log(get_sensor_log_file())
    data = entry.split(',')
    return get_data_row(data)


def get_last_enviro_measurement() -> dict:
    entry = commands.get_last_line_from_log(get_enviro_sensor_log_file())
    data = entry.split(',')
    return get_data_row_for_enviro(data)
