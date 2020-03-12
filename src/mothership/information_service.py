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
import config_serivce
import data_files
import utils
import web_data

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
    information['weather'] = web_data.get_weather()
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
    information['weather'] = web_data.get_weather()


if __name__ == '__main__':
    try:
        utils.setup_test_logging()
        refresh_all()
        data_files.save_dict_data_as_json(config_serivce.get_information_path(), information)
        print(data_files.load_json_data_as_dict_from(config_serivce.get_information_path()))
        data_files.backup_information_data(information)
    except Exception as e:
        print(information)
        print('Something went badly wrong\n{}'.format(e))
