import config
from common import data_files


def get_warnings(measurement: dict) -> list:
    warnings = []
    if float(measurement[config.FIELD_GPS_NUM_SATS]) < 1:
        warnings.append(f"GPS not detecting any satellites.")

    return warnings

def get_last_measurement():
    return data_files.load_json_data_as_dict_from('/home/ds/data/gps-last-measurement.txt')