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
import logging
from datetime import datetime
from timeit import default_timer as timer

import config
from common import app_timer, data_files
from gateways import web_data_gateway
from services import weather_service

logger = logging.getLogger('app')

every_five_minutes = datetime.now()
every_hour = datetime.now()
every_six_hour = datetime.now()

no = 'No information available yet'
information = {
    'weather': no,
    'o2': no,
    'crime': no,
    'pollution': {
        'wroclaw': no,
        'tianjin': no,
    },
    'train': no,
    'tube': no,
    config.FIELD_MEASUREMENT_TIME: no
}


def get_information():
    return information


# noinspection PyTypeChecker
def refresh_all():
    start_time = timer()
    information['pollution']['tianjin'] = web_data_gateway.get_pollution_for('tianjin')
    information['pollution']['wroclaw'] = web_data_gateway.get_pollution_for('wroclaw')
    information['weather'] = weather_service.get_weather()
    information['crime'] = web_data_gateway.get_crime()
    information['o2'] = web_data_gateway.get_o2_status()
    information['flood'] = web_data_gateway.get_flood()
    information['tube'] = web_data_gateway.get_tube(False)
    information['train'] = web_data_gateway.get_train()
    end_time = timer()
    data_files.save_dict_data_as_json("/home/pi/data/information.json",information)
    information[config.FIELD_MEASUREMENT_TIME] = str(int((end_time - start_time) * 1000))  # in ms
    return information


def should_refresh(count:int):
    global every_five_minutes
    global every_hour
    global every_six_hour
    logger.debug(f'Refreshing information for count no. {count}')
    if app_timer.is_time_to_run_every_6_hours(every_six_hour):
        logger.info('Running Refreshing everything (every 6 hours) tasks')
        refresh_all()
        every_six_hour = datetime.now()
        logger.info('Refresh "every 6 hours" complete')

    if app_timer.is_time_to_run_every_hour(every_hour):
        logger.info('Running Refreshing hourly tasks')
        refresh_hourly()
        data_files.backup_information_data(information)
        every_hour = datetime.now()
        logger.info('Refresh "every hour" complete')

    if app_timer.is_time_to_run_every_5_minutes(every_five_minutes):
        logger.info('Running Refreshing every 5 minutes tasks')
        refresh_every_5_minutes()
        every_five_minutes = datetime.now()
        logger.info('Refresh "every 5 minutes" complete')

def refresh_every_5_minutes():
    information['tube'] = web_data_gateway.get_tube(False)
    information['train'] = web_data_gateway.get_train()


# noinspection PyTypeChecker
def refresh_hourly():
    information['pollution']['tianjin'] = web_data_gateway.get_pollution_for('tianjin')
    information['pollution']['wroclaw'] = web_data_gateway.get_pollution_for('wroclaw')
    information['weather'] = weather_service.get_weather()
