from common import data_files


def get_averages_as_dict(measurements_list) -> dict:
    measurements_data = {
        'ax': 0, 'ay': 0, 'az': 0,
        'gx': 0, 'gy': 0, 'gz': 0,
        'mx': 0, 'my': 0, 'mz': 0,
        'measurement_time': 0
    }

    for entry in measurements_list:
        for field_key in measurements_data.keys():
            measurements_data[field_key] = measurements_data[field_key] + entry[field_key]

    size = len(measurements_list)
    if size > 0:
        for field_key in measurements_data.keys():
            measurements_data[field_key] = measurements_data[field_key] / size
    else:
        measurements_data = {
            'ax': 0, 'ay': 0, 'az': 0,
            'gx': 0, 'gy': 0, 'gz': 0,
            'mx': 0, 'my': 0, 'mz': 0,
            'measurement_time': 0
        }

    for field_key in measurements_data.keys():
        measurements_data[field_key] = f"{measurements_data[field_key]:.2f}"

    return measurements_data


def get_records_as_dict(measurements_list) -> dict:
    measurements_data = {
        'lowest_ax': 16777216,
        'highest_ax': -16777216,
        'lowest_ay': 16777216,
        'highest_ay': -16777216,
        'lowest_az': 16777216,
        'highest_az': -16777216,
        'lowest_gx': 16777216,
        'highest_gx': -16777216,
        'lowest_gy': 16777216,
        'highest_gy': -16777216,
        'lowest_gz': 16777216,
        'highest_gz': -16777216,
        'lowest_mx': 16777216,
        'highest_mx': -16777216,
        'lowest_my': 16777216,
        'highest_my': -16777216,
        'lowest_mz': 16777216,
        'highest_mz': -16777216,
        'fastest_measurement_time': 16777216,
        'slowest_measurement_time': 0
    }

    for entry in measurements_list:
        for field_key in measurements_data.keys():
            a_key = field_key.replace("slowest_", "").replace("highest_", "").replace("fastest_", "").replace("lowest_",
                                                                                                              "")
            if field_key.startswith("fastest_"):
                if measurements_data[field_key] > entry[a_key]:
                    measurements_data[field_key] = entry[a_key]
            elif field_key.startswith("slowest_"):
                if measurements_data[field_key] < entry[a_key]:
                    measurements_data[field_key] = entry[a_key]
            elif field_key.startswith("highest_"):
                if entry[a_key] > measurements_data[field_key]:
                    measurements_data[field_key] = entry[a_key]
            elif field_key.startswith("lowest_"):
                if entry[a_key] < measurements_data[field_key]:
                    measurements_data[field_key] = entry[a_key]
            else:
                print(
                    f'Interesting. field {field_key} with data {measurements_data[field_key]} :: key {a_key} with data {entry[a_key]}')
    return measurements_data


def check_warning(measurement: dict) -> list:
    warnings = []
    if measurement['ax'] > 1 or measurement['ax'] < -1:
        warnings.append(f"AX is high {measurement['ax']}")
    if measurement['ay'] > 1 or measurement['ay'] < -1:
        warnings.append(f"AY is high {measurement['ay']}")
    if measurement['az'] > 1 or measurement['az'] < -1:
        warnings.append(f"AZ is high {measurement['az']}")
    if measurement['gx'] > 1 or measurement['gx'] < -1:
        warnings.append(f"GX is high {measurement['gx']}")
    if measurement['gy'] > 1 or measurement['gy'] < -1:
        warnings.append(f"GY is high {measurement['gy']}")
    if measurement['gz'] > 1 or measurement['gz'] < -1:
        warnings.append(f"GZ is high {measurement['gz']}")
    if measurement['mx'] > -65 or measurement['mx'] < -95:
        warnings.append(f"MX is high {measurement['mx']}")
    if measurement['my'] > 140 or measurement['my'] < 120:
        warnings.append(f"MY is high {measurement['my']}")
    if measurement['mz'] > -350 or measurement['mz'] < -380:
        warnings.append(f"MZ is high {measurement['mz']}")

    return warnings

def get_last_measurement():
    return data_files.load_json_data_as_dict_from('/home/ds/data/motion-last-measurement.txt')