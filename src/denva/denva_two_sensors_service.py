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


def get_new_warnings(data) -> list:
    warnings = []
    if type(data[config.FIELD_TEMPERATURE]) is not float:
        data[config.FIELD_TEMPERATURE] = float(data[config.FIELD_TEMPERATURE])
    if data[config.FIELD_TEMPERATURE] < 16:
        warnings.append('Temperature is too low. Current temperature is: {}'.format(
            str(data[config.FIELD_TEMPERATURE])))
    elif data[config.FIELD_TEMPERATURE] < 18:
        warnings.append('Temperature is low. Current temperature is: {}'.format(
            str(data[config.FIELD_TEMPERATURE])))
    elif data[config.FIELD_TEMPERATURE] > 25:
        warnings.append('Temperature is high. Current temperature is: {}'.format(
            str(data[config.FIELD_TEMPERATURE])))
    elif data[config.FIELD_TEMPERATURE] > 30:
        warnings.append('Temperature is too high. Current temperature is: {}'.format(
            str(data[config.FIELD_TEMPERATURE])))

    if type(data[config.FIELD_CO2_TEMPERATURE]) is not float:
        data[config.FIELD_CO2_TEMPERATURE] = float(data[config.FIELD_CO2_TEMPERATURE])
    if data[config.FIELD_CO2_TEMPERATURE] < 16:
        warnings.append('Temperature (CO2) is too low. Current temperature is: {}'.format(
            str(data[config.FIELD_CO2_TEMPERATURE])))
    elif data[config.FIELD_CO2_TEMPERATURE] < 18:
        warnings.append('Temperature (CO2) is low. Current temperature is: {}'.format(
            str(data[config.FIELD_CO2_TEMPERATURE])))
    elif data[config.FIELD_CO2_TEMPERATURE] > 25:
        warnings.append('Temperature (CO2) is high. Current temperature is: {}'.format(
            str(data[config.FIELD_CO2_TEMPERATURE])))
    elif data[config.FIELD_CO2_TEMPERATURE] > 30:
        warnings.append('Temperature (CO2) is too hig. Current temperature is: {}'.format(
            str(data[config.FIELD_CO2_TEMPERATURE])))

    data[config.FIELD_HUMIDITY] = float(data[config.FIELD_HUMIDITY])

    if data[config.FIELD_HUMIDITY] < 30:
        warnings.append('Humidity is too low. Current humidity is: {}'.format(
            str(data[config.FIELD_HUMIDITY])))
    elif data[config.FIELD_HUMIDITY] < 40:
        warnings.append('Humidity is low. Current humidity is: {}'.format(
            str(data[config.FIELD_HUMIDITY])))
    elif data[config.FIELD_HUMIDITY] > 60:
        warnings.append('Humidity is high. Current humidity is: {}'.format(
            str(data[config.FIELD_HUMIDITY])))
    elif data[config.FIELD_HUMIDITY] > 70:
        warnings.append('Humidity is too high. Current humidity is: {}'.format(
            str(data[config.FIELD_HUMIDITY])))

    data['relative_humidity'] = float(data['relative_humidity'])

    if data['relative_humidity'] < 30:
        warnings.append('Humidity (CO2) is too low. Current humidity is: {}'.format(
            str(data['relative_humidity'])))
    elif data['relative_humidity'] < 40:
        warnings.append('Humidity (CO2) is low. Current humidity is: {}'.format(
            str(data['relative_humidity'])))
    elif data['relative_humidity'] > 60:
        warnings.append('Humidity (CO2) is high. Current humidity is: {}'.format(
            str(data['relative_humidity'])))
    elif data['relative_humidity'] > 70:
        warnings.append('Humidity (CO2) is too high. Current humidity is: {}'.format(
            str(data['relative_humidity'])))

    data[config.FIELD_CPU_TEMP] = float(re.sub('[^0-9.]', '', data[config.FIELD_CPU_TEMP]))

    sensor_config_data = config.load_cfg()

    if data[config.FIELD_CPU_TEMP] > sensor_config_data[config.FIELD_SYSTEM]['cpu_temp_fatal']:
        warnings.append('CPU temperature is too high. Current temperature is: {}'.format(
            str(data[config.FIELD_CPU_TEMP])))
    elif data[config.FIELD_CPU_TEMP] > sensor_config_data[config.FIELD_SYSTEM]['cpu_temp_error']:
        warnings.append('CPU temperature is very high. Current temperature is: {}'.format(
            str(data[config.FIELD_CPU_TEMP])))
    elif data[config.FIELD_CPU_TEMP] > sensor_config_data[config.FIELD_SYSTEM]['cpu_temp_warn']:
        warnings.append('CPU temperature is high. Current temperature is: {}'.format(
            str(data[config.FIELD_CPU_TEMP])))

    if int(data['co2']) > 5000:
        warnings.append('DANGEROUS CO2 level. Value {}'.format(data['co2']))
    elif int(data['co2']) > 2000:
        warnings.append('Very High CO2 level. Value {}'.format(data['co2']))
    elif int(data['co2']) > 900:
        warnings.append('Above typical level CO2 level. Value {}'.format(data['co2']))

    if float(data['eco2']) > 1000:
        warnings.append('High CO2 level: {}'.format(data['eco2']))

    if float(data['tvoc']) > 5000:
        warnings.append('Air Quality BAD: {}'.format(data['tvoc']))
    elif float(data['tvoc']) > 1500:
        warnings.append('Air Quality POOR: {}'.format(data['tvoc']))
    loggy.log_error_count(warnings)
    return warnings
