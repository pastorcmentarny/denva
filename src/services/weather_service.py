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
import os
from datetime import datetime

import config_service
from common import app_timer, data_files
from gateways import web_data_gateway

logger = logging.getLogger('app')


def save_weather_to_file(weather_data: list, weather_file: str):
    now = datetime.now()
    weather_timestamp = str('{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))

    logger.info('Saving updated weather to file using timestamp: {}'.format(weather_timestamp))

    weather_data.append(weather_timestamp)
    data_files.save_list_to_file(weather_data, weather_file)


def is_weather_data_expired(date: str) -> bool:
    last_check = date.split('-')
    return app_timer.is_time_to_run_every_6_hours(datetime(int(last_check[0]), int(last_check[1]), int(last_check[2]),
                                                           int(last_check[3]), int(last_check[4]), int(last_check[5])))


# FIXME
def get_weather() -> list:
    logger.info('Getting weather')
    weather_file = config_service.get_data_path() + 'weather.txt'
    if not os.path.exists(weather_file):
        logger.info('File not exists. Getting weather from the web')
        weather_data = cleanup_weather_data(web_data_gateway.get_weather())
    else:
        logger.info('loading data from the file')
        weather_data = data_files.load_weather(weather_file)
        if is_weather_data_expired(weather_data[len(weather_data) - 1]):
            logger.info('Weather in the file is out of date, Getting weather from the web')
            weather_data = cleanup_weather_data(web_data_gateway.get_weather())
        else:
            logger.info('returning weather from the file')
            return weather_data
    if weather_data != ['Weather data N/A']:
        save_weather_to_file(weather_data, weather_file)
        logger.info('returning updated weather')
        return weather_data
    logger.error('Something went badly wrong')
    return ['Weather data N/A']


def cleanup_weather_data(weather: str) -> list:
    result = weather.split(';')
    result_list = []
    for x in result:
        y = x.split('.')
        for z in y:
            z = z.replace('Maximum ', 'Max').replace('Minimum ', 'Min').replace('temperature', ' temp.').replace(
                'daytime ', '').replace('nighttime ', '').replace('degrees Celsius', '°C')
            if z:
                result_list.append(z.strip())
    result_list.remove('Today')
    return result_list
