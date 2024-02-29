import re

import config as config

from common import commands, loggy, data_loader

COLUMN_D1_GAS_RESISTANCE = 5

COLUMN_D1_HUMIDITY = 4

COLUMN_D1_PRESSURE = 3

COLUMN_D1_TEMPERATURE = 2

COLUMN_D1_TIMESTAMP = 0


def load_data_for_today() -> list:
    data_as_list = data_loader.load_data_as_list_from_csv(config.get_sensor_log_file())
    data = []
    for row in data_as_list:
        add_denva_row(data, row)
    return data


def add_denva_row(data, row):
    data.append(
        {
            config.FIELD_TIMESTAMP: row[config.DENVA_DATA_COLUMN_TIMESTAMP],
            config.FIELD_TEMPERATURE: row[config.DENVA_DATA_COLUMN_TEMP],
            config.FIELD_PRESSURE: row[config.DENVA_DATA_COLUMN_PRESSURE],
            config.FIELD_HUMIDITY: row[config.DENVA_DATA_COLUMN_HUMIDITY],
            config.FIELD_RELATIVE_HUMIDITY: row[config.DENVA_DATA_COLUMN_RELATIVE_HUMIDITY],
            config.FIELD_GAS_RESISTANCE: row[config.DENVA_DATA_COLUMN_GAS_RESISTANCE],
            config.FIELD_CO2: row[config.DENVA_DATA_COLUMN_CO2],
            config.FIELD_CO2_TEMPERATURE: row[config.DENVA_DATA_COLUMN_CO2_TEMPERATURE],
            config.FIELD_MEASUREMENT_TIME: row[config.DENVA_DATA_COLUMN_MEASUREMENT_TIME],
            config.FIELD_CPU_TEMP: row[config.DENVA_DATA_COLUMN_CPU_TEMP],
            config.FIELD_ECO2: row[config.DENVA_DATA_COLUMN_ECO2],
            config.FIELD_TVOC: row[config.DENVA_DATA_COLUMN_TVOC],
            config.FIELD_GPS_NUM_SATS: row[config.DENVA_DATA_COLUMN_GPS_NUM_SATS],
        }
    )


def get_last_new_measurement():
    entry = commands.get_last_line_from_log(config.get_sensor_log_file())
    data = entry.split(',')
    return get_new_data_row(data)


def get_new_data_row(row) -> dict:
    return {
        config.FIELD_TIMESTAMP: row[0],
        config.FIELD_TEMPERATURE: row[2],
        config.FIELD_PRESSURE: row[3],
        config.FIELD_HUMIDITY: f'{float(row[4]):0.2f}',
        config.FIELD_GAS_RESISTANCE: f'{float(row[5]):0.2f}',
        config.FIELD_COLOUR: row[6],
        config.FIELD_RED: row[7],
        config.FIELD_GREEN: row[8],
        config.FIELD_BLUE: row[9],
        config.FIELD_CO2: row[10],
        config.FIELD_CO2_TEMPERATURE: row[11],
        config.FIELD_CO2_TEMPERATURE: row[11],
        config.FIELD_RELATIVE_HUMIDITY: f'{float(row[12]):0.2f}',
        config.FIELD_CPU_TEMP: row[13],
        config.FIELD_ECO2: row[14],
        config.FIELD_TVOC: row[15],
        config.FIELD_UVA: row[16],
        config.FIELD_UVB: row[17],
        config.FIELD_UV: row[18],
    }


def get_new_warnings(data) -> list:
    warnings = []
    if type(data[config.FIELD_TEMPERATURE]) is not float:
        data[config.FIELD_TEMPERATURE] = float(data[config.FIELD_TEMPERATURE])
    if data[config.FIELD_TEMPERATURE] < config.get_temp_too_low_level():
        warnings.append(f'Temperature is too low. Current temperature is: {str(data[config.FIELD_TEMPERATURE])}')
    elif data[config.FIELD_TEMPERATURE] < config.get_temp_low_level():
        warnings.append(f'Temperature is low. Current temperature is: {str(data[config.FIELD_TEMPERATURE])}')
    elif data[config.FIELD_TEMPERATURE] > config.get_temp_high_level():
        warnings.append(f'Temperature is high. Current temperature is: {str(data[config.FIELD_TEMPERATURE])}')
    elif data[config.FIELD_TEMPERATURE] > config.get_temp_too_high_level():
        warnings.append(f'Temperature is too high. Current temperature is: {str(data[config.FIELD_TEMPERATURE])}')

    if type(data[config.FIELD_CO2_TEMPERATURE]) is not float:
        data[config.FIELD_CO2_TEMPERATURE] = float(data[config.FIELD_CO2_TEMPERATURE])
    if data[config.FIELD_CO2_TEMPERATURE] < config.get_temp_too_low_level():
        warnings.append(
            f'Temperature (CO2) is too low. Current temperature is: {str(data[config.FIELD_CO2_TEMPERATURE])}')
    elif data[config.FIELD_CO2_TEMPERATURE] < config.get_temp_low_level():
        warnings.append(f'Temperature (CO2) is low. Current temperature is: {str(data[config.FIELD_CO2_TEMPERATURE])}')
    elif data[config.FIELD_CO2_TEMPERATURE] > config.get_temp_high_level():
        warnings.append(f'Temperature (CO2) is high. Current temperature is: {str(data[config.FIELD_CO2_TEMPERATURE])}')
    elif data[config.FIELD_CO2_TEMPERATURE] > config.get_temp_too_high_level():
        warnings.append(
            f'Temperature (CO2) is too hig. Current temperature is: {str(data[config.FIELD_CO2_TEMPERATURE])}')

    data[config.FIELD_HUMIDITY] = float(data[config.FIELD_HUMIDITY])

    if data[config.FIELD_HUMIDITY] < config.get_humidity_too_low_level():
        warnings.append(f'Humidity is too low. Current humidity is: {str(data[config.FIELD_HUMIDITY])}')
    elif data[config.FIELD_HUMIDITY] < config.get_humidity_low_level():
        warnings.append(f'Humidity is low. Current humidity is: {str(data[config.FIELD_HUMIDITY])}')
    elif data[config.FIELD_HUMIDITY] > config.get_humidity_high_level():
        warnings.append(f'Humidity is high. Current humidity is: {str(data[config.FIELD_HUMIDITY])}')
    elif data[config.FIELD_HUMIDITY] > config.get_humidity_too_high_level():
        warnings.append(f'Humidity is too high. Current humidity is: {str(data[config.FIELD_HUMIDITY])}')

    data[config.FIELD_RELATIVE_HUMIDITY] = float(data[config.FIELD_RELATIVE_HUMIDITY])

    if data[config.FIELD_RELATIVE_HUMIDITY] < config.get_humidity_too_low_level():
        warnings.append(f'Humidity (CO2) is too low. Current humidity is: {str(data[config.FIELD_RELATIVE_HUMIDITY])}')
    elif data[config.FIELD_RELATIVE_HUMIDITY] < config.get_humidity_low_level():
        warnings.append(f'Humidity (CO2) is low. Current humidity is: {str(data[config.FIELD_RELATIVE_HUMIDITY])}')
    elif data[config.FIELD_RELATIVE_HUMIDITY] > config.get_humidity_high_level():
        warnings.append(f'Humidity (CO2) is high. Current humidity is: {str(data[config.FIELD_RELATIVE_HUMIDITY])}')
    elif data[config.FIELD_RELATIVE_HUMIDITY] > config.get_humidity_too_high_level():
        warnings.append(f'Humidity (CO2) is too high. Current humidity is: {str(data[config.FIELD_RELATIVE_HUMIDITY])}')

    data[config.FIELD_CPU_TEMP] = float(re.sub('[^0-9.]', '', data[config.FIELD_CPU_TEMP]))

    sensor_config_data = config.load_cfg()

    if data[config.FIELD_CPU_TEMP] > sensor_config_data[config.KEY_SYSTEM]['cpu_temp_fatal']:
        warnings.append(f'CPU temperature is too high. Current temperature is: {str(data[config.FIELD_CPU_TEMP])}')
    elif data[config.FIELD_CPU_TEMP] > sensor_config_data[config.KEY_SYSTEM]['cpu_temp_error']:
        warnings.append(f'CPU temperature is very high. Current temperature is: {str(data[config.FIELD_CPU_TEMP])}')
    elif data[config.FIELD_CPU_TEMP] > sensor_config_data[config.KEY_SYSTEM]['cpu_temp_warn']:
        warnings.append(f'CPU temperature is high. Current temperature is: {str(data[config.FIELD_CPU_TEMP])}')

    if int(data[config.FIELD_CO2]) > config.get_co2_danger_level():
        warnings.append(f'DANGEROUS CO2 level. Value {data[config.FIELD_CO2]}')
    elif int(data[config.FIELD_CO2]) > config.get_co2_high_level():
        warnings.append(f'Very High CO2 level. Value {data[config.FIELD_CO2]}')
    elif int(data[config.FIELD_CO2]) > config.get_co2_above_level():
        warnings.append(f'Above typical level CO2 level. Value {data[config.FIELD_CO2]}')

    # using same number for co2, eco2 and tvoc
    if float(data[config.FIELD_ECO2]) > config.get_co2_danger_level():
        warnings.append(f'High (E)CO2 level: {data[config.FIELD_ECO2]}')
    elif float(data[config.FIELD_ECO2]) > config.get_co2_danger_level():
        warnings.append(f'Very High (E)CO2 level. Value {data[config.FIELD_CO2]}')

    # using same number for co2, eco2 and tvoc
    if float(data[config.FIELD_TVOC]) > config.get_co2_danger_level():
        warnings.append(f'Air Quality DANGEROUS: {data[config.FIELD_TVOC]}')
    elif float(data['tvoc']) > config.get_co2_high_level():
        warnings.append(f'Air Quality POOR: {data[config.FIELD_TVOC]}')
    elif float(data['tvoc']) > config.get_co2_above_level():
        warnings.append(f'Air Quality NOT GOOD: {data[config.FIELD_TVOC]}')
    loggy.log_error_count(warnings)

    return warnings
