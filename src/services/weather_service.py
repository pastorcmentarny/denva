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
import os
from datetime import datetime

import config
from common import app_timer, data_files
from gateways import web_data_gateway

NO_WEATHER_DATA_MESSAGE = 'Weather data N/A'

logger = logging.getLogger('app')


def save_weather_to_file(weather_data: list, weather_file: str):
    now = datetime.now()
    weather_timestamp = str('{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))

    logger.info('Saving updated weather to file using timestamp: {}'.format(weather_timestamp))

    weather_data.append(weather_timestamp)
    data_files.save_list_to_file(weather_data, weather_file)


def get_weather() -> list:
    logger.info('Getting weather')
    weather_file = config.PI_DATA_PATH + 'weather.txt'
    if not os.path.exists(weather_file):
        logger.info('File not exists. Getting weather from the web')
        weather_data = __cleanup_weather_data(web_data_gateway.get_weather())
    else:
        logger.info('loading data from the file')
        weather_data = data_files.load_weather(weather_file)
        if __is_weather_data_expired(weather_data[len(weather_data) - 1]):
            logger.info('Weather in the file is out of date, Getting weather from the web')
            weather_data = __cleanup_weather_data(web_data_gateway.get_weather())
        else:
            logger.info('returning weather from the file')
            return weather_data
    if weather_data != [NO_WEATHER_DATA_MESSAGE]:
        save_weather_to_file(weather_data, weather_file)
        logger.info('returning updated weather')
        return weather_data
    logger.error('Something went badly wrong')
    return [NO_WEATHER_DATA_MESSAGE]


def __is_weather_data_expired(date: str) -> bool:
    last_check = date.split('-')
    return app_timer.is_time_to_run_every_6_hours(datetime(int(last_check[0]), int(last_check[1]), int(last_check[2]),
                                                           int(last_check[3]), int(last_check[4]), int(last_check[5])))


def __cleanup_weather_data(weather: str) -> list:
    result = weather.split(';')
    result_list = []
    for lines in result:
        line = lines.split('.')
        for z in line:
            z = z.replace("\n", " ")\
                .replace('Maximum ', 'Max')\
                .replace('Minimum ', 'Min')\
                .replace('temperature', ' temp.')\
                .replace('daytime ', '')\
                .replace('nighttime ', '')\
                .replace('degrees Celsius', '°C')
            if z:
                result_list.append(z.strip())
    if 'Today' in result_list:
        result_list.remove('Today')
    return result_list
