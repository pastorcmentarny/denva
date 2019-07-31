#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime

import commands


def get_sensor_log_file() -> str:
    today = datetime.datetime.now()
    return '/home/pi/logs/sensor-log' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '.csv'


def get_sensor_log_file_for(year: int, month: int, day: int) -> str:
    return '/home/pi/logs/sensor-log' + str(year) + '-' + str(month) + '-' + str(day) + '.csv'


def load_data_for_today() -> list:
    today = datetime.datetime.now()
    return load_data(today.year, today.month, today.day)


def load_data(year: int, month: int, day: int) -> list:
    sensor_log_file = open(get_sensor_log_file_for(year, month, day), 'r', newline='')
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []
    for row in csv_data:
        try:
            row[19] == '?'
        except IndexError:
            row.insert(19, '?')
            row.insert(20, '?')
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
            'cpu_temp': row[20]
        }
    )


def get_data_row(row):
    data_row = {
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
        'cpu_temp': commands.get_cpu_temp()
    }
    return data_row


def get_last_measurement() -> dict:
    entry = commands.get_last_line_from_log(get_sensor_log_file())
    data = entry.split(',')
    return get_data_row(data)
