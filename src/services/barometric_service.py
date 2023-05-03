import config
import dom_utils
from common import data_files


def get_warnings(measurement: dict) -> list:
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


def get_averages_as_dict(barometric_list):
    barometric_data = {
        "pressure": 0,
        "temperature": 0,
        "altitude": 0
    }
    for entry in barometric_list:
        for field_key in barometric_data.keys():
            barometric_data[field_key] = barometric_data[field_key] + entry[field_key]

    size = len(barometric_list)
    if size > 0:
        for field_key in barometric_data.keys():
            barometric_data[field_key] = barometric_data[field_key] / size

    return barometric_data


def get_records_as_dict(barometric_list):
    barometric_records = {
        "barometric_highest_pressure": -16777216,
        "barometric_lowest_pressure": 16777216,
        "barometric_highest_temperature": -16777216,
        "barometric_lowest_temperature": 16777216,
        "barometric_highest_altitude": -16777216,
        "barometric_lowest_altitude": 16777216,
        'barometric_fastest_measurement_time': 16777216,
        'barometric_slowest_measurement_time': 0
    }

    for entry in barometric_list:
        for field_key in barometric_records.keys():
            a_key = field_key.replace('barometric_','').replace("slowest_", "").replace("highest_", "").replace("fastest_", "").replace("lowest_","")
            if field_key.startswith("barometric_fastest_"):
                if barometric_records[field_key] > entry[a_key]:
                    barometric_records[field_key] = entry[a_key]
            elif field_key.startswith("barometric_slowest_"):
                if barometric_records[field_key] < entry[a_key]:
                    barometric_records[field_key] = entry[a_key]
            elif field_key.startswith("barometric_highest_"):
                if entry[a_key] > barometric_records[field_key]:
                    barometric_records[field_key] = entry[a_key]
            elif field_key.startswith("barometric_lowest_"):
                if entry[a_key] < barometric_records[field_key]:
                    barometric_records[field_key] = entry[a_key]
            else:
                print(
                    f'Interesting. field {field_key} with data {barometric_records[field_key]} :: key {a_key} with data {entry[a_key]}')
    return barometric_records


def update_for_barometric_sensor(averages:dict,records:dict,measurement_date:str):
    barometric_result = data_files.load_list_of_dict_for(
        f"/home/ds/data/barometric-data-{measurement_date}.txt")
    averages.update(get_averages_as_dict(barometric_result))
    records.update(get_records_as_dict(barometric_result))
    barometric_result.clear()
    return averages,records
