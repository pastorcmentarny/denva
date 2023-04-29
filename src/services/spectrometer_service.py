import dom_utils
from common import data_files


def get_warnings(measurement: dict) -> list:
    warnings = []
    if float(measurement['red']) < 1 and float(measurement['orange']) < 1 and float(measurement['yellow']) < 1 and float(measurement['green']) < 1 and float(measurement['blue']) < 1 and float(measurement['violet']) < 1:
        warnings.append(
            f"Spectrometer returns zeros only Red:{measurement['red']} | Orange:{measurement['orange']} | Yellow:{measurement['yellow']} | Green:{measurement['green']} | Blue:{measurement['blue']} | Violet:{measurement['violet']}|")
    return warnings


def get_last_measurement():
    return data_files.load_json_data_as_dict_from('/home/ds/data/spectrometer-last-measurement.txt')


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
            a_key = field_key.replace('spectrometer_','').replace("slowest_", "").replace("highest_", "").replace("fastest_", "")
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


def update_for_spectrometer(averages:dict, records:dict):
    spectrometer_result = data_files.load_list_of_dict_for(
        f"/home/ds/data/spectrometer-data-{dom_utils.get_date_for_today()}.csv")
    # spectrometer is not here as this do not have sense
    records.update(get_records_as_dict(spectrometer_result))
    spectrometer_result.clear()
