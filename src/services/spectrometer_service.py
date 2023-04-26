from common import data_files


def get_warnings(measurement: dict) -> list:
    warnings = []
    if float(measurement['red']) < 1 and float(measurement['orange']) < 1 and float(measurement['yellow']) < 1 and float(measurement['green']) < 1 and float(measurement['blue']) < 1 and float(measurement['violet']) < 1:
        warnings.append(
            f"Spectrometer returns zeros only Red:{measurement['red']} | Orange:{measurement['orange']} | Yellow:{measurement['yellow']} | Green:{measurement['green']} | Blue:{measurement['blue']} | Violet:{measurement['violet']}|")
    return warnings


def get_last_measurement():
    return data_files.load_json_data_as_dict_from('/home/ds/data/spectrometer-last-measurement.txt')