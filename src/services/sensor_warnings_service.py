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
import re

import config_service
from denva import denva_sensors_service
from denviro import denviro_sensors_service
from common import commands, dom_utils, get_description_for, data_files

warnings_logger = logging.getLogger('warnings')

shaking_level = config_service.load_cfg()['sensors']['motion']['sensitivity']

config = config_service.load_cfg()


def get_warnings_for(year: str, month: str, day: str) -> list:
    date = dom_utils.get_filename_for_warnings(year, month, day)
    return data_files.load_warnings('/home/pi/logs/' + date)


def get_warnings_for_today() -> list:
    return data_files.load_warnings('/home/pi/logs/warnings.log')


def get_current_warnings() -> dict:
    data = denva_sensors_service.get_last_measurement()
    return denva_sensors_service.get_warnings(data)


def count_warning_today() -> dict:
    return denva_sensors_service.count_warnings(get_warnings_for_today())


# soruce: https://ec.europa.eu/environment/air/quality/standards.htm
def get_current_warnings_for_enviro() -> dict:
    data = denviro_sensors_service.get_last_measurement()
    warnings = {}

    data['cpu_temp'] = float(re.sub('[^0-9.]', '', data['cpu_temp']))

    if data['cpu_temp'] > config['sensor']['cpu_temp_fatal']:
        message = 'CPU temperature is too high [cthf]. Current temperature is: {}'.format(str(data['cpu_temp']))
        warnings['cpu_temp'] = message
        warnings_logger.error(message)

    elif data['cpu_temp'] > config['sensor']['cpu_temp_error']:
        message = 'CPU temperature is very high [cthe]. Current temperature is: {}'.format(str(data['cpu_temp']))
        warnings['cpu_temp'] = message
        warnings_logger.error(message)
    elif data['cpu_temp'] > config['sensor']['cpu_temp_warn']:
        message = 'CPU temperature is high [cthw]. Current temperature is: {}'.format(str(data['cpu_temp']))
        warnings['cpu_temp'] = message
        warnings_logger.warning(message)

    data['temperature'] = float(data['temperature'])

    if type(data['temperature']) is not float:
        data['temperature'] = float(data['temperature'])
    if data['temperature'] < 16:
        message = 'Temperature is too low [tle]. Current temperature is: {}'.format(str(data['temperature']))
        warnings['temperature'] = message
        warnings_logger.error(message)
    elif data['temperature'] < 18:
        message = 'Temperature is low [tlw]. Current temperature is: {}'.format(str(data['temperature']))
        warnings['temperature'] = message
        warnings_logger.warning(message)
    elif data['temperature'] > 25:
        message = 'Temperature is high [thw]. Current temperature is: {}'.format(str(data['temperature']))
        warnings['temperature'] = message
        warnings_logger.warning(message)
    elif data['temperature'] > 30:
        message = 'Temperature is too high  [the]. Current temperature is: {}'.format(str(data['temperature']))
        warnings['temperature'] = message
        warnings_logger.error(message)

    '''carbon monoxide (reducing), nitrogen dioxide (oxidising), and ammonia (NH3),
    Nitrogen dioxide (NO2) - 40 µg/m3 Carbon monoxide (CO) - 10 mg/m3
    Data from sensor is in kilo-Ohms
    data['oxidised']: '{:0.2f}'.format(float(row[6])),  # "oxidised"    unit = "kO"
    data['reduced']: '{:0.2f}'.format(float(row[7])),  # unit = 'kO'
    data['nh3']: '{:0.2f}'.format(float(row[8])),  # unit = 'kO'
    data['pm1']: row[9],  # unit = 'ug/m3'
    need to convert between format
    '''

    data['pm1'] = float(data['pm1'])

    if data['pm1'] > 25:
        message = 'Particle 1 amount is too high [p1w]. Current PM1 amount is {} ug/m3'.format(str(data['pm25']))
        warnings['pm1'] = message
        warnings_logger.error(message)

    data['pm25'] = float(data['pm25'])

    if data['pm25'] > 25:
        message = 'Particle 2.5 amount is too high [p2w]. Current PM2.5 amount is {} ug/m3'.format(str(data['pm25']))
        warnings['pm2_5'] = message
        warnings_logger.error(message)

    data['pm10'] = float(data['pm10'])

    if data['pm10'] > 40:
        message = 'Particle 10 amount is too high [pTw]. Current PM10 amount is {} ug/m3'.format(str(data['pm25']))
        warnings['pm10'] = message
        warnings_logger.error(message)

    data['light'] = float(data['light'])

    if data['light'] > 3000:
        message = 'It is too bright in the room. Current value: {} lux.'.format(str(data['light']))
        warnings['lhe'] = message
        warnings_logger.error(message)
    elif data['light'] > 2000:
        message = 'It is very bright in the room. Current value: {} lux.'.format(str(data['light']))
        warnings['lhw'] = message
        warnings_logger.warning(message)

    return warnings


def get_warnings_as_list(data) -> list:
    warnings = []
    if data['temp'] < 16:
        warnings.append('Temp. is TOO LOW')
        warnings_logger.error('[tle] Temperature is too low. Current temperature is: {}'.format(str(data['temp'])))
    elif data['temp'] < 18:
        warnings.append('Temp. is low')
        warnings_logger.warning('[tlw] Temperature is low. Current temperature is: {}'.format(str(data['temp'])))
    elif data['temp'] > 25:
        warnings.append('Temp. is high')
        warnings_logger.warning('[thw] Temperature is high. Current temperature is: {}'.format(str(data['temp'])))
    elif data['temp'] > 30:
        warnings.append('Temp. is TOO HIGH')
        warnings_logger.error('[the] Temperature is too high. Current temperature is: {}'.format(str(data['temp'])))

    if data['humidity'] < 30:
        warnings.append('Humidity is TOO LOW')
        warnings_logger.error('[hle] Humidity is too low. Current humidity is: {}'.format(str(data['humidity'])))
    elif data['humidity'] < 40:
        warnings.append('Humidity is low')
        warnings_logger.warning('[hlw] Humidity is low. Current humidity is: {}'.format(str(data['humidity'])))
    elif data['humidity'] > 60:
        warnings.append('Humidity is high')
        warnings_logger.warning('[hhw] Humidity is high. Current humidity is: {}'.format(str(data['humidity'])))
    elif data['humidity'] > 70:
        warnings.append('Humidity is TOO HIGH')
        warnings_logger.error('[hhe] Humidity is too high. Current humidity is: {}'.format(str(data['humidity'])))

    if data['uva_index'] > 6:
        warnings.append('UV A is TOO HIGH')
        warnings_logger.error('[uvae] UV A is too high. Current UV A is: {}'.format(str(data['uva_index'])))

    if data['uvb_index'] > 6:
        warnings.append('UV B is TOO HIGH')
        warnings_logger.error('[uvbe] UV B is too high. Current UV B is: {}'.format(str(data['uvb_index'])))

    if data['motion'] > shaking_level:
        warnings_logger.info('[dsl] Dom is shaking his legs. Value: {} [mhe]'.format(str(data['motion'])))

    if type(data['cpu_temp']) != float:
        data['cpu_temp'] = float(re.sub('[^0-9.]', '', data['cpu_temp']))

    if data['cpu_temp'] > config['sensor']['cpu_temp_fatal']:
        warnings.append('CPU temp. TOO HIGH!')
        warnings_logger.error(
            '[cthf] CPU temperature is too high. Current temperature is: {}'.format(str(data['cpu_temp'])))
    elif data['cpu_temp'] > config['sensor']['cpu_temp_error']:
        warnings.append('CPU temp. VERY HIGH')
        warnings_logger.error(
            '[cthe] CPU temperature is very high. Current temperature is: {}'.format(str(data['cpu_temp'])))
    elif data['cpu_temp'] > config['sensor']['cpu_temp_warn']:
        warnings.append('CPU temp. is high')
        warnings_logger.warning(
            '[cthw] CPU temperature is high. Current temperature is: {}'.format(str(data['cpu_temp'])))

    free_space = int(commands.get_space_available())
    if free_space < 500:
        warnings.append('Low Free Space: {}'.format(str(free_space) + 'MB'))
        warnings_logger.warning('[fsl] Low Free Space: {}'.format(str(free_space) + 'MB'))

    data_free_space = int(commands.get_data_space_available())
    if data_free_space < 500:
        warnings.append('Low Free Space on Data Partition: {}'.format(str(data_free_space) + 'MB'))
        warnings_logger.warning('[dfsl] Low Free Space on Data Partition: {}'.format(str(data_free_space) + 'MB'))

    eco2 = int(data['eco2'])
    if eco2 > 1000:
        warnings.append('High CO2 level (Time to open window?): {}'.format(str(eco2)))
        warnings_logger.warning('[cow] High CO2 level (Time to open window?): {}'.format(str(eco2)))

    tvoc = get_description_for.iqa_from_tvoc(data['tvoc'])
    if tvoc['value'] > 5000:
        warnings.append('{} with value {}'.format(tvoc['information'], tvoc['value']))
        warnings_logger.error('[iqe] {} with value {}'.format(tvoc['information'], tvoc['value']))
    elif tvoc['value'] > 1500:
        warnings.append('{} with value {}'.format(tvoc['information'], tvoc['value']))
        warnings_logger.warning('[iqw] {} with value {}'.format(tvoc['information'], tvoc['value']))
    dom_utils.log_error_count(warnings)
    return warnings
