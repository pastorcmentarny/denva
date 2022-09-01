import re
from datetime import datetime

import config as config
import dom_utils
from common import data_files, commands, loggy


def load_data_for_today() -> list:
    return data_files.load_data(get_sensor_log_file())


def get_sensor_log_file():
    return config.PI_DATA_PATH + dom_utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def get_sensor_log_file_at_server() -> str:
    return config.PI_SENSORS_DATA_PATH + 'denva/' + dom_utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def get_last_new_measurement():
    entry = commands.get_last_line_from_log(get_sensor_log_file())
    data = entry.split(',')
    return get_new_data_row(data)


def get_new_data_row(row) -> dict:
    return {
        config.FIELD_TIMESTAMP: row[0],
        config.FIELD_TEMPERATURE: row[2],
        config.FIELD_PRESSURE: row[3],
        config.FIELD_HUMIDITY: '{:0.2f}'.format(float(row[4])),
        config.FIELD_GAS_RESISTANCE: '{:0.2f}'.format(float(row[5])),
        config.FIELD_COLOUR: row[6],
        config.FIELD_RED: row[7],
        config.FIELD_GREEN: row[8],
        config.FIELD_BLUE: row[9],
        config.FIELD_CO2: row[10],
        config.FIELD_CO2_TEMPERATURE: row[11],
        config.FIELD_RELATIVE_HUMIDITY: '{:0.2f}'.format(float(row[12])),
        config.FIELD_CPU_TEMP: row[13],
        config.FIELD_ECO2: row[14],
        config.FIELD_TVOC: row[15],
        config.FIELD_GPS_NUM_SATS: row[22],
    }


def get_new_warnings(data) -> dict:
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

    if type(data['co2_temperature']) is not float:
        data['co2_temperature'] = float(data['co2_temperature'])
    if data['co2_temperature'] < 16:
        warnings['co2_temperature'] = 'Temperature (CO2) is too low [tle]. Current temperature is: {}'.format(
            str(data['co2_temperature']))
    elif data['co2_temperature'] < 18:
        warnings['co2_temperature'] = 'Temperature (CO2) is low [tlw]. Current temperature is: {}'.format(
            str(data['co2_temperature']))
    elif data['co2_temperature'] > 25:
        warnings['co2_temperature'] = 'Temperature (CO2) is high [thw]. Current temperature is: {}'.format(
            str(data['co2_temperature']))
    elif data['co2_temperature'] > 30:
        warnings['co2_temperature'] = 'Temperature (CO2) is too high  [the]. Current temperature is: {}'.format(
            str(data['co2_temperature']))

    data['humidity'] = float(data['humidity'])

    if data['humidity'] < 30:
        warnings['humidity'] = 'Humidity is too low [hle]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] < 40:
        warnings['humidity'] = 'Humidity is low [hlw]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] > 60:
        warnings['humidity'] = 'Humidity is high [hhw]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] > 70:
        warnings['humidity'] = 'Humidity is too high [hhe]. Current humidity is: {}'.format(str(data['humidity']))

    data['relative_humidity'] = float(data['relative_humidity'])

    if data['relative_humidity'] < 30:
        warnings['relative_humidity'] = 'Humidity (CO2) is too low [hle]. Current humidity is: {}'.format(
            str(data['relative_humidity']))
    elif data['relative_humidity'] < 40:
        warnings['relative_humidity'] = 'Humidity (CO2) is low [hlw]. Current humidity is: {}'.format(
            str(data['relative_humidity']))
    elif data['relative_humidity'] > 60:
        warnings['relative_humidity'] = 'Humidity (CO2) is high [hhw]. Current humidity is: {}'.format(
            str(data['relative_humidity']))
    elif data['relative_humidity'] > 70:
        warnings['relative_humidity'] = 'Humidity (CO2) is too high [hhe]. Current humidity is: {}'.format(
            str(data['relative_humidity']))

    data['cpu_temp'] = float(re.sub('[^0-9.]', '', data['cpu_temp']))

    sensor_config_data = config.load_cfg()

    if data['cpu_temp'] > sensor_config_data['system']['cpu_temp_fatal']:
        warnings['cpu_temp'] = 'CPU temperature is too high [cthf]. Current temperature is: {}'.format(
            str(data['cpu_temp']))
    elif data['cpu_temp'] > sensor_config_data['system']['cpu_temp_error']:
        warnings['cpu_temp'] = 'CPU temperature is very high [cthe]. Current temperature is: {}'.format(
            str(data['cpu_temp']))
    elif data['cpu_temp'] > sensor_config_data['system']['cpu_temp_warn']:
        warnings['cpu_temp'] = 'CPU temperature is high [cthw]. Current temperature is: {}'.format(
            str(data['cpu_temp']))

    if int(data['co2']) > 5000:
        warnings['co2'] = 'DANGEROUS CO2 level [cdl]. Value {}'.format(data['co2'])
    elif int(data['co2']) > 2000:
        warnings['co2'] = 'Very High CO2 level [cwl]. Value {}'.format(data['co2'])
    elif int(data['co2']) > 900:
        warnings['co2'] = 'Above typical level CO2 level [cal]. Value {}'.format(data['co2'])

    if float(data['eco2']) > 1000:
        warnings['eco2'] = 'High CO2 level: {}'.format(data['eco2'])

    if float(data['tvoc']) > 5000:
        warnings['tvoc'] = 'Air Quality BAD: {}'.format(data['tvoc'])
    elif float(data['tvoc']) > 1500:
        warnings['tvoc'] = 'Air Quality POOR: {}'.format(data['tvoc'])
    loggy.log_error_count(warnings)
    return warnings


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
        'cow': 0,
        'iqe': 0,
        'iqw': 0,
        'cal': 0,  # co2 above level
        'cwl': 0,
        'cdl': 0
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
        elif '[cal]' in warning:
            warning_counter['cal'] += 1
        elif '[cwl]' in warning:
            warning_counter['cwl'] += 1
        elif '[cdl]' in warning:
            warning_counter['cdl'] += 1

    return warning_counter
