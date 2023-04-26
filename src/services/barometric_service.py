import config
from common import data_files


def check_warning(measurement: dict) -> list:
    warnings = []
    if measurement[config.FIELD_TEMPERATURE] < 16:
        message = 'Temperature is too low [tle]. Current temperature is: {}'.format(
            str(measurement[config.FIELD_TEMPERATURE]))
        warnings.append(message)
    elif measurement[config.FIELD_TEMPERATURE] < 18:
        message = 'Temperature is low [tlw]. Current temperature is: {}'.format(
            str(measurement[config.FIELD_TEMPERATURE]))
        warnings.append(message)
    elif measurement[config.FIELD_TEMPERATURE] > 25:
        message = 'Temperature is high [thw]. Current temperature is: {}'.format(
            str(measurement[config.FIELD_TEMPERATURE]))
        warnings.append(message)
    elif measurement[config.FIELD_TEMPERATURE] > 30:
        message = 'Temperature is too high  [the]. Current temperature is: {}'.format(
            str(measurement[config.FIELD_TEMPERATURE]))
        warnings.append(message)

    if measurement[config.FIELD_PRESSURE] > 1020:
        warnings.append(f'Pressure is high {measurement[config.FIELD_PRESSURE]}')
    elif measurement[config.FIELD_PRESSURE] < 985:
        warnings.append(f'Pressure is low {measurement[config.FIELD_PRESSURE]}')

    return warnings


def get_last_measurement():
    return data_files.load_json_data_as_dict_from('/home/ds/data/barometric-last-measurement.txt')