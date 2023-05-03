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
import config
import logging

from common import data_files
from denva import denva_sensors_service
from reports import averages, records, report_service
from services import sensor_warnings_service

logger = logging.getLogger('app')


def get_all_stats_for_today():
    return denva_sensors_service.load_data_for_today()


def get_warnings_for(year, month, day):
    return sensor_warnings_service.get_warnings_for(year, month, day)


def count_warnings():
    path = config.get_warnings_path_for_today()
    try:
        with open(path, 'r') as fp:
            for count, line in enumerate(fp):
                pass
    except Exception as exception:
        logging.warning(f'Unable to warning file due to: ${exception}', exc_info=True)
    return count + 1


def count_warnings_for(datetime):
    path = config.get_warnings_path_for(datetime)
    try:
        with open(path, 'r') as fp:
            for count, line in enumerate(fp):
                pass
    except Exception as exception:
        logging.warning(f'Unable to warning file due to: ${exception}', exc_info=True)
    return count + 1


def get_current_warnings():
    return sensor_warnings_service.get_current_warnings()


def get_warnings_for_today():
    return data_files.load_json_data_as_dict_from('/home/ds/data/all-warnings.txt')


def get_averages():
    return {}


def get_records_for_today():
    return records.get_records_for_today()


def get_last_measurement_from_all_sensors():
    return data_files.load_json_data_as_dict_from('/home/ds/data/all-measurement.json')


def get_last_report():
    return report_service.generate_for_yesterday()



