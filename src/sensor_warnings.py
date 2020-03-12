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
import re
import logging

import commands
import data_files
import iqa_utils
import sensor_log_reader
import utils
import config_serivce
warnings_logger = logging.getLogger('warnings')

shaking_level = config_serivce.load_cfg()['sensors']['motion']['sensitivity']

config = config_serivce.load_cfg()


def get_warnings_for(year: str, month: str, day: str) -> list:
    date = utils.get_filename_for_warnings(year, month, day)
    return data_files.load_warnings('/home/pi/logs/' + date)


def get_warnings_for_today() -> list:
    return data_files.load_warnings('/home/pi/logs/warnings.log')


def get_current_warnings() -> dict:
    data = sensor_log_reader.get_last_measurement()
    return get_warnings(data)


def get_warnings(data) -> dict:
    warnings = {}
    if type(data['temp']) is not float:
        data['temp'] = float(data['temp'])
    if data['temp'] < 16:
        warnings['temp'] = 'Temperature is too low [tle]. Current temperature is: {}'.format(str(data['temp']))
    elif data['temp'] < 18:
        warnings['temp'] = 'Temperature is low [tlw]. Current temperature is: {}'.format(str(data['temp']))
    elif data['temp'] > 25:
        warnings['temp'] = 'Temperature is high [thw]. Current temperature is: {}'.format(str(data['temp']))
    elif data['temp'] > 30:
        warnings['temp'] = 'Temperature is too high  [the]. Current temperature is: {}'.format(str(data['temp']))

    data['humidity'] = float(data['humidity'])

    if data['humidity'] < 30:
        warnings['humidity'] = 'Humidity is too low [hle]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] < 40:
        warnings['humidity'] = 'Humidity is low [hlw]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] > 60:
        warnings['humidity'] = 'Humidity is high [hhw]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] > 70:
        warnings['humidity'] = 'Humidity is too high [hhe]. Current humidity is: {}'.format(str(data['humidity']))

    data['uva_index'] = float(data['uva_index'])

    if data['uva_index'] > 6:
        warnings['uva_index'] = 'UV A is too high [uvae]. Current UV A is: {}'.format(str(data['uva_index']))

    data['uvb_index'] = float(data['uvb_index'])

    if data['uvb_index'] > 6:
        warnings['uvb_index'] = 'UV B is too high [uvbe]. Current UV B is: {}'.format(str(data['uvb_index']))

    data['cpu_temp'] = float(re.sub('[^0-9.]', '', data['cpu_temp']))

    if data['cpu_temp'] > config['sensor']['cpu_temp_fatal']:
        warnings['cpu_temp'] = 'CPU temperature is too high [cthf]. Current temperature is: {}'.format(
            str(data['cpu_temp']))
    elif data['cpu_temp'] > config['sensor']['cpu_temp_error']:
        warnings['cpu_temp'] = 'CPU temperature is very high [cthe]. Current temperature is: {}'.format(
            str(data['cpu_temp']))
    elif data['cpu_temp'] > config['sensor']['cpu_temp_warn']:
        warnings['cpu_temp'] = 'CPU temperature is high [cthw]. Current temperature is: {}'.format(
            str(data['cpu_temp']))

    data['motion'] = float(data['motion'])

    if data['motion'] > 1000:
        warnings['motion'] = 'Dom is shaking his legs [slw]. Value: {}'.format(str(data['motion']))

    if int(commands.get_space_available()) < 500:
        warnings['free_space'] = 'Low Free Space: {}'.format(commands.get_space_available() + 'MB')

    if int(data['eco2']) > 1000:
        warnings['eco2'] = 'High CO2 level: {}'.format(data['eco2'])

    if int(data['tvoc']) > 5000:
        warnings['tvoc'] = 'Air Quality BAD: {}'.format(data['tvoc'])
    elif int(data['tvoc']) > 1500:
        warnings['tvoc'] = 'Air Quality POOR: {}'.format(data['tvoc'])

    return warnings


def count_warning_today() -> dict:
    return count_warnings(get_warnings_for_today())

#TODO replace mocked data with real one
def get_current_warnings_for_enviro() -> dict:
    return  {
        'test' : 'crazy pollution'
    }
def count_warnings(warnings) -> dict:
    warning_counter = {
        'the': 0,
        'thw': 0,
        'tle': 0,
        'tlw': 0,
        'hhe': 0,
        'hhw': 0,
        'hle': 0,
        'hlw': 0,
        'cthf': 0,
        'cthe': 0,
        'cthw': 0,
        'uvaw': 0,
        'uvbw': 0,
        'fsl': 0,
        'dfsl': 0,
        'dsl': 0,
        'cow' :0,
        'iqe' :0,
        'iqw' :0
    }

    for warning in warnings:
        if '[cthf]' in warning:
            warning_counter['cthf'] += 1
        elif '[cthe]' in warning:
            warning_counter['cthe'] += 1
        elif '[cthw]' in warning:
            warning_counter['cthw'] += 1
        elif '[the]' in warning:
            warning_counter['the'] += 1
        elif '[thw]' in warning:
            warning_counter['thw'] += 1
        elif '[tlw]' in warning:
            warning_counter['tlw'] += 1
        elif '[tle]' in warning:
            warning_counter['tle'] += 1
        elif '[hhe]' in warning:
            warning_counter['hhe'] += 1
        elif '[hhw]' in warning:
            warning_counter['hhw'] += 1
        elif '[hlw]' in warning:
            warning_counter['hlw'] += 1
        elif '[hle]' in warning:
            warning_counter['hle'] += 1
        elif '[uvaw]' in warning:
            warning_counter['uvaw'] += 1
        elif '[uvbw]' in warning:
            warning_counter['uvbw'] += 1
        elif '[fsl]' in warning:
            warning_counter['fsl'] += 1
        elif '[dfsl]' in warning:
            warning_counter['dfsl'] += 1
        elif '[dsl]' in warning:
            warning_counter['dsl'] += 1
        elif '[cow]' in warning:
            warning_counter['cow'] += 1
        elif '[iqw]' in warning:
            warning_counter['iqw'] += 1
        elif '[iqe]' in warning:
            warning_counter['iqe'] += 1

    return warning_counter


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

    tvoc = iqa_utils.get_iqa_for_tvoc(data['tvoc'])
    if tvoc['value'] > 5000:
        warnings.append('{} with value {}'.format(tvoc['information'],tvoc['value']))
        warnings_logger.error('[iqe] {} with value {}'.format(tvoc['information'],tvoc['value']))
    elif tvoc['value'] > 1500:
        warnings.append('{} with value {}'.format(tvoc['information'],tvoc['value']))
        warnings_logger.warning('[iqw] {} with value {}'.format(tvoc['information'],tvoc['value']))

    return warnings
