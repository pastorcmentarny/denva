import logging
import os
from datetime import datetime

import config_service
from common import app_timer, data_files
from gateways import web_data_gateway

weather_file = config_service.get_data_path() + 'weather.txt'
logger_app = logging.getLogger('app')
logger_server = logging.getLogger('server')


def save_weather_to_file(weather_data: list):
    now = datetime.now()
    weather_data.append(str('{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)))
    data_files.save_list_to_file(weather_data, weather_file)


def is_weather_data_expired(date: str) -> bool:
    last_check = date.split('-')
    return app_timer.is_time_to_run_every_6_hours(datetime(int(last_check[0]), int(last_check[1]), int(last_check[2]),
                                                           int(last_check[3]), int(last_check[4]), int(last_check[5])))


def get_weather() -> list:
    log_info('Getting weather')
    if not os.path.exists(weather_file):
        log_info('File not exists. Getting weather from the web')
        weather_data = web_data_gateway.get_weather()
    else:
        log_info('loading data from the file')
        weather_data = data_files.load_weather(weather_file)
        if is_weather_data_expired(weather_data[len(weather_data) - 1]):
            log_info('weather in the file is out of date, Getting weather from the web')
            weather_data = web_data_gateway.get_weather()
        else:
            log_info('returning weather from the file')
            return weather_data
    if weather_data != ['Weather data N/A']:
        save_weather_to_file(weather_data)
        return weather_data
    log_error('Something went badly wrong')
    return ['Weather data N/A']


# FIXME due to crap design
def log_info(msg: str):
    # logger_app.info(msg)
    logger_server.info(msg)


# FIXME due to crap design
def log_error(msg: str):
    # logger_app.warning(msg)
    logger_server.warning(msg)
