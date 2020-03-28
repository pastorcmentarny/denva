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
from datetime import timedelta

import averages
import records
import sensor_warnings
import tubes_train_service
import utils
import web_data

warnings_logger = logging.getLogger('warnings')
stats_log = logging.getLogger('stats')
logger = logging.getLogger('app')

report = {
    'report_date': 'today',
    'measurement_counter': 0,
    'warning_counter': 0,
    'warnings': {},  # TODO i believe i don't need specify anything as this dict will be overwritten
    "records": {
        'temperature': {
            'min': 0,
            'max': -0
        },
        'pressure': {
            'min': 0,
            'max': 0
        },
        'humidity': {
            'min': 0,
            'max': 0
        },
        'max_uv_index': {
            'uva': 0,
            'uvb': 0
        },
        'cpu_temperature': {
            'min': 0,
            'max': 0
        },
        'biggest_motion': 0,
        'highest_eco2': 0,
        'highest_tvoc': 0
    },
    "tube": {
        "delays": {
            'BakerlooMD': 0,
            'BakerlooSD': 0,
            'BakerlooPS': 0,
            'BakerlooFS': 0,
            'BakerlooTotalTime': 0,
            'CentralMD': 0,
            'CentralSD': 0,
            'CentralPS': 0,
            'CentralFS': 0,
            'CentralTotalTime': 0,
            'CircleMD': 0,
            'CircleSD': 0,
            'CirclePS': 0,
            'CircleFS': 0,
            'CircleTotalTime': 0,
            'DistrictMD': 0,
            'DistrictSD': 0,
            'DistrictPS': 0,
            'DistrictFS': 0,
            'DistrictTotalTime': 0,
            'HammersmithMD': 0,
            'HammersmithSD': 0,
            'HammersmithPS': 0,
            'HammersmithFS': 0,
            'HammersmithTotalTime': 0,
            'JubileeMD': 0,
            'JubileeSD': 0,
            'JubileePS': 0,
            'JubileeFS': 0,
            'JubileeTotalTime': 0,
            'MetropolitanMD': 0,
            'MetropolitanSD': 0,
            'MetropolitanPS': 0,
            'MetropolitanFS': 0,
            'MetropolitanTotalTime': 0,
            'NorthernMD': 0,
            'NorthernSD': 0,
            'NorthernPS': 0,
            'NorthernFS': 0,
            'NorthernTotalTime': 0,
            'PiccadillyMD': 0,
            'PiccadillySD': 0,
            'PiccadillyPS': 0,
            'PiccadillyFS': 0,
            'PiccadillyTotalTime': 0,
            'VictoriaMD': 0,
            'VictoriaSD': 0,
            'VictoriaPS': 0,
            'VictoriaFS': 0,
            'VictoriaTotalTime': 0,
            'WaterlooMD': 0,
            'WaterlooSD': 0,
            'WaterlooPS': 0,
            'WaterlooFS': 0,
            'WaterlooTotalTime': 0
        }
    }
}


def generate_for_yesterday() -> dict:
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return generate_for(yesterday)


def generate_for(date: datetime) -> dict:
    try:
        # is below 2 lines looks stupid? yes, because it is
        warnings_logger.info("")
        stats_log.info("")
        '''
        why? as report is generated on next day, you need add log entry 
        logger can trigger TimedRotatingFileHandler event  and create file
        that is used by report service. 
        Why I used logger to store data? because I am lazy and i used most efficient way
        to store data I do analyse over later.
        '''
        year = date.year
        month = date.month
        day = date.day
        data = load_data(year, month, day)
        report['measurement_counter'] = len(data)
        report['report_date'] = "{}.{}'{}".format(day, month, year)
        warnings = sensor_warnings.get_warnings_for(year, month, day)
        report['warning_counter'] = len(warnings)
        report['warnings'] = sensor_warnings.count_warnings(warnings)
        report['records'] = records.get_records(data)
        report['avg'] = averages.get_averages(data)
        report['tube']['delays'] = tubes_train_service.count_tube_problems_for(year, month, day) # move to separate function
        return report
    except:
        logger.error("Unable to generate  report.", exc_info=True)
        return {}


def load_data(year, month, day) -> list:
    csv_data = read_data_as_list_from_csv_file(day, month, year,'sensor-log')
    data = []
    for row in csv_data:
        try:
            row[19] == '?'
        except IndexError:
            logger.warning("no data for ")
            row.insert(19, '?')
            row.insert(20, '?')
        try:
            row[21] == '?'
        except IndexError:
            logger.warning("no eco2 or tvoc data")
            row.insert(21, 0)
            row.insert(22, 0)
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
                'tvoc': row[22],
            }
        )
    return data

def load_enviro_data(year, month, day) -> list:
    csv_data = read_data_as_list_from_csv_file(day, month, year,'sensor-enviro-log')
    data = []
    for row in csv_data:
        data.append({
            'timestamp' : row[0],
            'temperature' : '{:0.1f}'.format(float(row[1])),  # unit = "C"
            'light' : '{:0.1f}'.format(float(row[4])),
            "oxidised" : '{:0.2f}'.format(float(row[6])),  # "oxidised"    unit = "kO"
            'reduced' : '{:0.2f}'.format(float(row[7])),  # unit = "kO"
            "nh3" : '{:0.2f}'.format(float(row[8])),  # unit = "kO"
            "pm1" : row[9],  # unit = "ug/m3"
            "pm25" : row[10],  # unit = "ug/m3"
            "pm10" :  row[11],  # unit = "ug/m3"
            "measurement_time" :  row[12],
        })
    return data


def read_data_as_list_from_csv_file(day, month, year, log_file_name:str) -> list:
    path = utils.get_filename_from_year_month_day(log_file_name, 'csv', year, month, day)
    sensor_log_file = utils.fix_nulls(open('/home/pi/logs/' + path, 'r',
                                           newline=''))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    sensor_log_file.close()
    return csv_data


def generate_enviro_report_for_yesterday() -> dict:
    yesterday = datetime.now() - timedelta(days=1)
    evniro_report ={}

    try:
        # is below 2 lines looks stupid? yes, because it is
        warnings_logger.info("")
        stats_log.info("")
        '''
        why? as report is generated on next day, you need add log entry 
        logger can trigger TimedRotatingFileHandler event  and create file
        that is used by report service. 
        Why I used logger to store data? because I am lazy and i used most efficient way
        to store data I do analyse over later.
        '''
        year = yesterday.year
        month = yesterday.month
        day = yesterday.day
        data = load_enviro_data(year, month, day)
        evniro_report['measurement_counter'] = len(data)
        evniro_report['report_date'] = "{}.{}'{}".format(day, month, year)
        warnings = sensor_warnings.get_warnings_for(year, month, day)
        evniro_report['warning_counter'] = len(warnings)
        evniro_report['avg'] = averages.get_enviro_averages(data)
        evniro_report['records'] = records.get_enviro_records(data)
        return evniro_report
    except Exception as exception:
        logger.error("Unable to generate  report.", exc_info=True)
        return {'error' : exception}

