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
import csv
import logging
from datetime import datetime
from datetime import timedelta
from timeit import default_timer as timer

import config
import dom_utils
from gateways import local_data_gateway
from reports import averages, records
from services import information_service, denva_service

warnings_logger = logging.getLogger('warnings')
logger = logging.getLogger('app')

report = {
    'report_date': 'today',
    "tube": {
        "stats_counter": {
            'Bakerloo': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Central': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Circle': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'District': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Hammersmith-city': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Jubilee': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Metropolitan': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Northern': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Piccadilly': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Victoria': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Waterloo-city': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,
            }
        }
    }
}

denva_report = {
    'report_date': 'today',
    config.FIELD_MEASUREMENT_COUNTER: 0,
    'warning_counter': 0,
    "records": {
        'temperature': {
            'min': 0,
            'max': -0
        },
        config.FIELD_PRESSURE: {
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
}


def generate_for_yesterday() -> dict:
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return generate_for(yesterday)


def generate_for(date: datetime) -> dict:
    try:
        year = date.year
        month = date.month
        day = date.day
        data = load_data(year, month, day)
        logger.info(f'data length: {len(data)}')
        denva_report[config.FIELD_MEASUREMENT_COUNTER] = len(data)
        denva_report['report_date'] = f"{day}.{month}'{year}"
        logger.info('Getting records..')
        denva_report['records'] = records.get_records(data)
        logger.info('Getting averages..')
        denva_report['avg'] = averages.get_averages(data)
        denva_report['warning_counter'] = denva_service.count_warnings_for(date)
        denva_report['warnings'] = denva_service.count_warnings_for(date)
        return denva_report
    except Exception as exception:
        logger.error(f"Unable to generate  report due to {exception}. Data {denva_report}", exc_info=True)
        return {}


def load_data(year, month, day) -> list:
    csv_data = read_data_as_list_from_csv_file(day, month, year, 'sensor-log')
    data = []
    for row in csv_data:
        data.append(
            {
                config.FIELD_TIMESTAMP: row[config.DENVA_DATA_COLUMN_TIMESTAMP],
                config.FIELD_MEASUREMENT_TIME: row[config.DENVA_DATA_COLUMN_MEASUREMENT_TIME],
                config.FIELD_TEMPERATURE: row[config.DENVA_DATA_COLUMN_TEMP],
                config.FIELD_PRESSURE: row[config.DENVA_DATA_COLUMN_PRESSURE],
                config.FIELD_HUMIDITY: row[config.DENVA_DATA_COLUMN_HUMIDITY],
                config.FIELD_GAS_RESISTANCE: row[config.DENVA_DATA_COLUMN_GAS_RESISTANCE],
                config.FIELD_COLOUR: row[config.DENVA_DATA_COLUMN_COLOUR],
                config.FIELD_RED: row[config.DENVA_DATA_COLUMN_R],
                config.FIELD_GREEN: row[config.DENVA_DATA_COLUMN_G],
                config.FIELD_BLUE: row[config.DENVA_DATA_COLUMN_B],
                config.FIELD_CO2: row[config.DENVA_DATA_COLUMN_CO2],
                config.FIELD_CO2_TEMPERATURE: row[config.DENVA_DATA_COLUMN_CO2_TEMPERATURE],
                config.FIELD_RELATIVE_HUMIDITY: row[config.DENVA_DATA_COLUMN_RELATIVE_HUMIDITY],
                config.FIELD_CPU_TEMP: row[config.DENVA_DATA_COLUMN_CPU_TEMP],
                config.FIELD_ECO2: row[config.DENVA_DATA_COLUMN_ECO2],
                config.FIELD_TVOC: row[config.DENVA_DATA_COLUMN_TVOC],
                # config.FIELD_GPS_NUM_SATS: row[config.DENVA_DATA_COLUMN_GPS_NUM_SATS]
                # config.FIELD_GPS_NUM_SATS: -1  # FIXME
            }
        )
    return data


def read_data_as_list_from_csv_file(day, month, year, log_file_name: str) -> list:
    path = dom_utils.get_filename_from_year_month_day(log_file_name, 'csv', year, month, day)
    sensor_log_file = dom_utils.fix_nulls(open(f'{config.PI_DATA_PATH}{path}', 'r',
                                               newline=''))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    sensor_log_file.close()
    return csv_data


def generate():
    logger.info('Preparing to send denva report email')
    start_time = timer()
    email_data = {
        'report': {
            'denva': local_data_gateway.get_yesterday_report_for_denva(),
            config.KEY_DENVA_TWO: local_data_gateway.get_yesterday_report_for_denva_two(),
            'aircraft': local_data_gateway.get_yesterday_report_for_aircraft(),
            'rickmansworth': information_service.get_data_about_rickmansworth(),
        },
        'status': local_data_gateway.get_data_for('http://192.168.0.200:5000/shc/get', 3)
    }
    end_time = timer()
    logger.info(f'It took {int((end_time - start_time) * 1000)} ms to generate data')
    return email_data
