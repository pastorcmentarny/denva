import config
from common import data_loader

MZ = "mz"
MY = "my"
MX = "mx"
GZ = "gz"
GY = "gy"
GX = "gx"
AZ = "az"
AY = "ay"
AX = "ax"
POSITIVE_MOTION_ALERT = 1
NEGATIVE_MOTION_ALERT = -1


def get_averages_as_dict(measurements_list) -> dict:
    measurements_data = {
        AX: 0, AY: 0, AZ: 0,
        GX: 0, GY: 0, GZ: 0,
        MX: 0, MY: 0, MZ: 0,
        "measurement_time": 0
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
            AX: 0, AY: 0, AZ: 0,
            GX: 0, GY: 0, GZ: 0,
            MX: 0, MY: 0, MZ: 0,
            "measurement_time": 0
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
        'motion_fastest_measurement_time': 16777216,
        'motion_slowest_measurement_time': 0
    }

    for entry in measurements_list:
        for field_key in measurements_data.keys():
            a_key = field_key.replace("motion_slowest_", "").replace("highest_", "").replace("motion_fastest_",
                                                                                             "").replace("lowest_",
                                                                                                         "")
            if field_key.startswith("motion_fastest_"):
                if measurements_data[field_key] > entry[a_key]:
                    measurements_data[field_key] = entry[a_key]
            elif field_key.startswith("motion_slowest_"):
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


def get_warnings(measurement: dict) -> list:
    warnings = []
    if measurement[AX] > POSITIVE_MOTION_ALERT or measurement[AX] < NEGATIVE_MOTION_ALERT:
        warnings.append(f'AX is high {measurement[AX]}')
    if measurement[AY] > POSITIVE_MOTION_ALERT or measurement[AY] < NEGATIVE_MOTION_ALERT:
        warnings.append(f'AY is high {measurement[AY]}')
    if measurement[AZ] > POSITIVE_MOTION_ALERT or measurement[AZ] < NEGATIVE_MOTION_ALERT:
        warnings.append(f'AZ is high {measurement[AZ]}')
    if measurement[GX] > POSITIVE_MOTION_ALERT or measurement[GX] < NEGATIVE_MOTION_ALERT:
        warnings.append(f'GX is high {measurement[GX]}')
    if measurement[GY] > POSITIVE_MOTION_ALERT or measurement[GY] < NEGATIVE_MOTION_ALERT:
        warnings.append(f'GY is high {measurement[GY]}')
    if measurement[GZ] > POSITIVE_MOTION_ALERT or measurement[GZ] < NEGATIVE_MOTION_ALERT:
        warnings.append(f'GZ is high {measurement[GZ]}')
    # no magnetic warnings

    return warnings


def get_last_measurement():
    return data_loader.load_json_data_as_dict_from(config.get_motion_last_measurement())


def update_for_motion_sensor(averages: dict, records: dict, measurement_date: str):
    motion_result = data_loader.load_list_of_dict_for(config.get_motion_data_for_date(measurement_date))
    averages.update(get_averages_as_dict(motion_result))
    records.update(get_records_as_dict(motion_result))
    motion_result.clear()
    return averages, records
