#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import logging

warnings_logger = logging.getLogger('warnings')

shaking_level = 1000  # extract to config file


def get_warnings(data) -> dict:
    warnings = {}
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

    print(data['cpu_temp'])
    data['cpu_temp'] = float(re.sub('[^0-9.]', '', data['cpu_temp']))

    if data['cpu_temp'] > 75:
        warnings['cpu_temp'] = 'CPU temperature is too high [cthf]. Current temperature is: {}'.format(
            str(data['cpu_temp']))
    elif data['cpu_temp'] > 60:
        warnings['cpu_temp'] = 'CPU temperature is very high [cthe]. Current temperature is: {}'.format(
            str(data['cpu_temp']))
    elif data['cpu_temp'] > 50:
        warnings['cpu_temp'] = 'CPU temperature is high [cthw]. Current temperature is: {}'.format(
            str(data['cpu_temp']))

    data['motion'] = float(data['motion'])

    if data['motion'] > 1000:
        warnings['motion'] = 'Dom is shaking his legs [slw]. Value: {}'.format(str(data['motion']))

    return warnings


def get_warnings_as_list(data) -> list:
    warnings = []
    if data['temp'] < 16:
        warnings.append("Temp. is TOO LOW")
        warnings_logger.error('Temperature is too low. Current temperature is: {}'.format(str(data['temp'])))
    elif data['temp'] < 18:
        warnings.append("Temp. is low")
        warnings_logger.warning('Temperature is low. Current temperature is: {}'.format(str(data['temp'])))
    elif data['temp'] > 25:
        warnings.append("Temp. is high")
        warnings_logger.warning('Temperature is high. Current temperature is: {}'.format(str(data['temp'])))
    elif data['temp'] > 30:
        warnings.append("Temp. is TOO HIGH")
        warnings_logger.error('Temperature is too high. Current temperature is: {}'.format(str(data['temp'])))

    if data['humidity'] < 30:
        warnings.append("Humidity is TOO LOW")
        warnings_logger.error('Humidity is too low. Current humidity is: {}'.format(str(data['humidity'])))
    elif data['humidity'] < 40:
        warnings.append("Humidity is low")
        warnings_logger.warning('Humidity is low. Current humidity is: {}'.format(str(data['humidity'])))
    elif data['humidity'] > 60:
        warnings.append("Humidity is high")
        warnings_logger.warning('Humidity is high. Current humidity is: {}'.format(str(data['humidity'])))
    elif data['humidity'] > 70:
        warnings.append("Humidity is TOO HIGH")
        warnings_logger.error('Humidity is too high. Current humidity is: {}'.format(str(data['humidity'])))

    if data['uva_index'] > 6:
        warnings.append("UV A is TOO HIGH")
        warnings_logger.error('UV A is too high. Current UV A is: {}'.format(str(data['uva_index'])))

    if data['uvb_index'] > 6:
        warnings.append("UV B is TOO HIGH")
        warnings_logger.error('UV B is too high. Current UV B is: {}'.format(str(data['uvb_index'])))

    if data['motion'] > shaking_level:
        warnings_logger.info('Dom is shaking his legs. Value: {} [mhe]'.format(str(data["motion"])))

    if type(data['cpu_temp']) != float:
        data['cpu_temp'] = float(re.sub('[^0-9.]', '', data['cpu_temp']))

    if data['cpu_temp'] > 75:
        warnings.append("CPU temp. TOO HIGH!")
        warnings_logger.error('CPU temperature is too high. Current temperature is: {}'.format(str(data['cpu_temp'])))
    elif data['cpu_temp'] > 60:
        warnings.append("CPU temp. VERY HIGH")
        warnings_logger.error('CPU temperature is very high. Current temperature is: {}'.format(str(data['cpu_temp'])))
    elif data['cpu_temp'] > 50:
        warnings.append("CPU temp. is high")
        warnings_logger.warning('CPU temperature is high. Current temperature is: {}'.format(str(data['cpu_temp'])))

    return warnings
