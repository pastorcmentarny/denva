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
from common import commands
from denviro import denviro_sensors_service
from reports import averages, records, report_service
from services import sensor_warnings_service


# TODO refactor name
def get_current_measurement(host: str) -> dict:
    measurement = denviro_sensors_service.get_last_measurement()
    measurement['host'] = host
    measurement['system'] = commands.get_system_info()
    return measurement


def get_report_for_yesterday():
    return report_service.generate_enviro_report_for_yesterday()


def get_averages_for_today():
    return averages.get_enviro_averages_for_today()


def get_last_measurement():
    return denviro_sensors_service.get_last_measurement()


def get_records_for_today():
    return records.get_enviro_records_for_today()


def get_current_warnings():
    return sensor_warnings_service.get_current_warnings_for_enviro()


def get_current_warnings_count():
    return sensor_warnings_service.count_warning_today()  # TODO is it right call ?
