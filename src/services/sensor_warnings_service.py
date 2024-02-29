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
import re

import config
from common import commands, get_description_for, data_files, loggy
import dom_utils
from services import denva_sensors_service

#TODO clean up file
warnings_logger = logging.getLogger('warnings')

shaking_level = config.load_cfg()['sensors']['motion']['sensitivity']

cfg = config.load_cfg()


def get_warnings_for(year: str, month: str, day: str) -> list:
    date = dom_utils.get_filename_for_warnings(year, month, day)
    return data_files.load_warnings('/home/ds/logs/' + date)


def get_warnings_for_today() -> list:
    return data_files.load_warnings('/home/ds/logs/warnings.log')


def get_current_warnings() -> list:
    data = denva_sensors_service.get_last_new_measurement()
    return denva_sensors_service.get_new_warnings(data)


def get_warnings_as_list(data) -> list:
    warnings = []
    if data['temp'] < 16:
        warnings.append('Temp. is TOO LOW')
        warnings_logger.error(f'[tle] Temperature is too low. Current temperature is: {str(data["temp"])}')
    elif data['temp'] < 18:
        warnings.append('Temp. is low')
        warnings_logger.warning(f'[tlw] Temperature is low. Current temperature is: {str(data["temp"])}')
    elif data['temp'] > 25:
        warnings.append('Temp. is high')
        warnings_logger.warning(f'[thw] Temperature is high. Current temperature is: {str(data["temp"])}')
    elif data['temp'] > 30:
        warnings.append('Temp. is TOO HIGH')
        warnings_logger.error(f'[the] Temperature is too high. Current temperature is: {str(data["temp"])}')

    if data['humidity'] < 30:
        warnings.append('Humidity is TOO LOW')
        warnings_logger.error(f'[hle] Humidity is too low. Current humidity is: {str(data["humidity"])}')
    elif data['humidity'] < 40:
        warnings.append('Humidity is low')
        warnings_logger.warning(f'[hlw] Humidity is low. Current humidity is: {str(data["humidity"])}')
    elif data['humidity'] > 60:
        warnings.append('Humidity is high')
        warnings_logger.warning(f'[hhw] Humidity is high. Current humidity is: {str(data["humidity"])}')
    elif data['humidity'] > 70:
        warnings.append('Humidity is TOO HIGH')
        warnings_logger.error(f'[hhe] Humidity is too high. Current humidity is: {str(data["humidity"])}')

    if data['uva_index'] > 6:
        warnings.append('UV A is TOO HIGH')
        warnings_logger.error(f'[uvae] UV A is too high. Current UV A is: {str(data["uva_index"])}')

    if data['uvb_index'] > 6:
        warnings.append('UV B is TOO HIGH')
        warnings_logger.error(f'[uvbe] UV B is too high. Current UV B is: {str(data["uvb_index"])}')

    if data['motion'] > shaking_level:
        warnings_logger.info(f'[dsl] Dom is shaking his legs. Value: {str(data["motion"])} [mhe]')

    if type(data[config.FIELD_CPU_TEMP]) != float:
        data[config.FIELD_CPU_TEMP] = float(re.sub('[^0-9.]', '', data[config.FIELD_CPU_TEMP]))

    if data[config.FIELD_CPU_TEMP] > cfg['sensor']['cpu_temp_fatal']:
        warnings.append('CPU temp. TOO HIGH!')
        warnings_logger.error(
            f'[cthf] CPU temperature is too high. Current temperature is: {str(data[config.FIELD_CPU_TEMP])}')
    elif data[config.FIELD_CPU_TEMP] > cfg['sensor']['cpu_temp_error']:
        warnings.append('CPU temp. VERY HIGH')
        warnings_logger.error(
            f'[cthe] CPU temperature is very high. Current temperature is: {str(data[config.FIELD_CPU_TEMP])}')
    elif data[config.FIELD_CPU_TEMP] > cfg['sensor']['cpu_temp_warn']:
        warnings.append('CPU temp. is high')
        warnings_logger.warning(
            f'[cthw] CPU temperature is high. Current temperature is: {str(data[config.FIELD_CPU_TEMP])}')

    free_space = int(commands.get_space_available())
    if free_space < 500:
        warnings.append(f'Low Free Space: {str(free_space) + "MB"}')
        warnings_logger.warning(f'[fsl] Low Free Space: {str(free_space) + "MB"}')

    eco2 = int(data['eco2'])
    if eco2 > 1000:
        warnings.append(f'High CO2 level (Time to open window?): {str(eco2)}')
        warnings_logger.warning(f'[cow] High CO2 level (Time to open window?): {str(eco2)}')

    tvoc = get_description_for.iqa_from_tvoc(data['tvoc'])
    if tvoc['value'] > 5000:
        warnings.append(f'{tvoc["information"]} with value {tvoc["value"]}')
        warnings_logger.error(f'[iqe] {tvoc["information"]} with value {tvoc["value"]}')
    elif tvoc['value'] > 1500:
        warnings.append(f'{tvoc["information"]} with value {tvoc["value"]}')
        warnings_logger.warning(f'[iqw] {tvoc["information"]} with value {tvoc["value"]}')
    loggy.log_error_count(warnings)
    return warnings
