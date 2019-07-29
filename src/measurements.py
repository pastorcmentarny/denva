#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime

import sensor_log_reader
import utils


def store(data, motion):
    timestamp = datetime.datetime.now()
    sensor_log_file = open(sensor_log_reader.get_sensor_log_file(), 'a+', newline='')
    csv_writer = csv.writer(sensor_log_file)
    csv_writer.writerow([timestamp,
                         data['temp'], data['pressure'], data['humidity'], data['gas_resistance'],
                         data['colour'], data['aqi'],
                         data['uva_index'], data['uvb_index'],
                         data['motion'],
                         motion['ax'], motion['ay'], motion['az'],
                         motion['gx'], motion['gy'], motion['gz'],
                         motion['mx'], motion['my'], motion['mz'],
                         data['measurement_time'],
                         utils.get_float_number_from_text(data['cpu_temp'])
                         ])
    sensor_log_file.close()
