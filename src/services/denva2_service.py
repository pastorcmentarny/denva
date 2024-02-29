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
from datetime import datetime

import dom_utils

from common import data_loader, data_files
from reports import d2_report_service
from services import sensor_warnings_service, denva_sensors_service
from services import barometric_service, spectrometer_service, motion_service, gps_service

logger = logging.getLogger('app')


def get_all_stats_for_today():
    return denva_sensors_service.load_data_for_today()


def get_warnings_for(year, month, day):
    return sensor_warnings_service.get_warnings_for(year, month, day)


def count_warnings():
    path = config.get_today_warnings()
    return data_files.count_lines(path)


def count_warnings_for(selected_date):
    path = config.get_warnings_path_for(selected_date)
    return data_files.count_lines(path)


def get_current_warnings(measurement):
    warnings = []
    warnings.extend(barometric_service.get_warnings(measurement))
    warnings.extend(gps_service.get_warnings(measurement))
    warnings.extend(motion_service.get_warnings(measurement))
    warnings.extend(spectrometer_service.get_warnings(measurement))
    return warnings


def get_warnings_for_today():
    return data_loader.load_json_data_as_dict_from(config.get_today_warnings())


def get_averages():
    return data_loader.load_json_data_as_dict_from(config.get_averages_as_one_path())


def get_records_for_today():
    return data_loader.load_json_data_as_dict_from(config.get_all_records_as_one_path())


def get_last_measurement_from_all_sensors():
    return data_loader.load_json_data_as_dict_from(config.get_all_mesaurements_as_one_path())


def get_report_for_today():
    report_file_name = dom_utils.get_date_as_filename('report', 'txt', datetime.now())
    return data_loader.load_json_data_as_dict_from(f'{config.PI_DATA_PATH}{report_file_name}')


def get_report_for_yesterday():
    return d2_report_service.get_report_for(
        f"{config.PI_DATA_PATH}{dom_utils.get_date_as_filename('report', 'json', dom_utils.get_yesterday_datetime())}",
        dom_utils.get_yesterday_datetime())
