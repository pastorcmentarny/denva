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
import logging
from datetime import datetime
from timeit import default_timer as timer

import app_timer
import data_files
import web_data
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
    'measurement_time': no
}


def get_information():
    return information


def refresh_all():
    start_time = timer()
    information['pollution']['tianjin'] = web_data.get_pollution_for('tianjin')
    information['pollution']['wroclaw'] = web_data.get_pollution_for('wroclaw')
    information['weather'] = weather_service.get_weather()
    information['crime'] = web_data.get_crime()
    information['o2'] = web_data.get_o2_status()
    information['flood'] = web_data.get_flood()
    information['tube'] = web_data.get_tube(False)
    information['train'] = web_data.get_train()
    end_time = timer()
    information['measurement_time'] = str(int((end_time - start_time) * 1000))  # in ms


def should_refresh():
    global every_five_minutes
    global every_hour
    global every_six_hour

    if app_timer.is_time_to_run_every_6_hours(every_six_hour):
        refresh_all()
        every_six_hour = datetime.now()
        return

    if app_timer.is_time_to_run_every_hour(every_hour):
        refresh_hourly()
        data_files.backup_information_data(information)
        every_hour = datetime.now()

    if app_timer.is_time_to_run_every_5_minutes(every_five_minutes):
        refresh_every_5_minutes()
        every_five_minutes = datetime.now()


def refresh_every_5_minutes():
    information['tube'] = web_data.get_tube(False)
    information['train'] = web_data.get_train()


def refresh_hourly():
    information['pollution']['tianjin'] = web_data.get_pollution_for('tianjin')
    information['pollution']['wroclaw'] = web_data.get_pollution_for('wroclaw')
    information['weather'] = weather_service.get_weather()
