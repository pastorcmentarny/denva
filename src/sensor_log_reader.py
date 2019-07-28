#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime
import time
import re

import commands
import warning_utils


def get_sensor_log_file() -> str:
    today = datetime.datetime.now()
    return '/home/pi/logs/sensor-log' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '.csv'


def get_sensor_log_file_for(year: int, month: int, day: int) -> str:
    return '/home/pi/logs/sensor-log' + str(year) + '-' + str(month) + '-' + str(day) + '.csv'


def get_records() -> dict:
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
        'biggest_motion': 0
    }

    data_records = load_data()
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

    end = time.time_ns()
    result['log entries counter'] = len(data_records)
    result["execution_time"] = str(end - start) + ' ns.'
    return result


def get_averages() -> dict:
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

    data_records = load_data()
    for data_record in data_records:
        temperature += float(data_record['temp'])
        pressure += float(data_record['pressure'])
        humidity += float(data_record['humidity'])
        cpu_temperature += float(re.sub('[^0-9.]', '', data_record['cpu_temp']))
        gas_resistance += float(data_record['gas_resistance'])
        uva += float(data_record['uva_index'])
        uvb += float(data_record['uvb_index'])
        motion += float(data_record['motion'])
        measurement_time += float(re.sub('[^0-9.]', '', data_record['measurement_time']))

    records = len(data_records)
    if records != 0:
        result['temperature'] = "{:.2f}".format(temperature / records)
        result['pressure'] = "{:.2f}".format(pressure / records)
        result['humidity'] = "{:.2f}".format(humidity / records)
        result['gas_resistance'] = "{:.2f}".format(gas_resistance / records)
        result['uva'] = "{:.2f}".format(uva / records)
        result['uvb'] = "{:.2f}".format(uvb / records)
        result['cpu_temperature'] = "{:.2f}".format(cpu_temperature / records)
        result['motion'] = "{:.2f}".format(motion / records)
        result['measurement_time'] = "{:.2f}".format(measurement_time / records)
    else:
        result['info'] = 'No records'
    end = time.time_ns()
    result["execution_time"] = str(end - start) + ' ns.'
    return result


def get_current_measurement() -> dict:
    data = load_data()
    return data[len(data) - 1]


def load_warning_from_today() -> list:
    file_data = open('/home/pi/logs/warnings.log', 'r', newline='')
    return file_data.readlines()


def count_warning_today():
    data = load_warning_from_today()
    return warning_utils.count_warnings(data)


def get_current_warnings() -> dict:
    data = get_current_measurement()
    return warning_utils.get_warnings(data)


def load_data() -> list:
    sensor_log_file = open(get_sensor_log_file(), 'r', newline='')
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
    entry = commands.get_last_line_from_log('/home/pi/logs/sensor-log.csv');
    data = entry.split(',')
    return get_data_row(data)
