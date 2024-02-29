import config
from common import data_loader

KEY_VIOLET = 'violet'

KEY_BLUE = 'blue'

KEY_GREEN = 'green'

KEY_YELLOW = 'yellow'

KEY_ORANGE = 'orange'

KEY_RED = 'red'


def get_warnings(measurement: dict) -> list:
    warnings = []
    if (float(measurement[KEY_RED]) < 1 and float(measurement[KEY_ORANGE]) < 1
            and float(measurement[KEY_YELLOW]) < 1 and float(measurement[KEY_GREEN]) < 1
            and float(measurement[KEY_BLUE]) < 1 and float(measurement[KEY_VIOLET]) < 1):
        warnings.append(
            f"Spectrometer returns zeros only Red:{measurement[KEY_RED]} | Orange:{measurement[KEY_ORANGE]}"
            f" | Yellow:{measurement[KEY_YELLOW]} | Green:{measurement[KEY_GREEN]}"
            f" | Blue:{measurement[KEY_BLUE]} | Violet:{measurement[KEY_VIOLET]}|")
    return warnings


def get_last_measurement():
    return data_loader.load_json_data_as_dict_from(config.get_spectrometer_last_measurement())


def get_records_as_dict(spectrometer_list):
    spectrometer_records = {
        "spectrometer_highest_red": -16777216,
        "spectrometer_highest_orange": -16777216,
        "spectrometer_highest_yellow": -16777216,
        "spectrometer_highest_green": -16777216,
        "spectrometer_highest_blue": -16777216,
        "spectrometer_highest_violet": -16777216,
        'spectrometer_fastest_measurement_time': 16777216,
        'spectrometer_slowest_measurement_time': 0
    }

    for entry in spectrometer_list:
        for field_key in spectrometer_records.keys():
            a_key = field_key.replace('spectrometer_', '').replace("slowest_", "").replace("highest_", "").replace(
                "fastest_", "")
            if field_key.startswith("spectrometer_fastest_"):
                if spectrometer_records[field_key] > entry[a_key]:
                    spectrometer_records[field_key] = entry[a_key]
            elif field_key.startswith("spectrometer_slowest_"):
                if spectrometer_records[field_key] < entry[a_key]:
                    spectrometer_records[field_key] = entry[a_key]
            elif field_key.startswith("spectrometer_highest_"):
                if entry[a_key] > spectrometer_records[field_key]:
                    spectrometer_records[field_key] = entry[a_key]
            else:
                print(
                    f'Interesting. field {field_key} with data {spectrometer_records[field_key]} :: key {a_key} with data {entry[a_key]}')
    return spectrometer_records


def update_for_spectrometer(averages: dict, records: dict, measurement_date: str):
    spectrometer_result = data_loader.load_list_of_dict_for(config.get_spectrometer_data_for_date(measurement_date))
    # spectrometer is not here as this do not have sense
    records.update(get_records_as_dict(spectrometer_result))
    spectrometer_result.clear()
    return averages, records
