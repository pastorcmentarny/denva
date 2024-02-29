import config
from common import data_loader


def get_warnings(measurement: dict) -> list:
    warnings = []
    if float(measurement[config.FIELD_GPS_NUM_SATS]) < 1:
        warnings.append(f"GPS not detecting any satellites.")

    return warnings


def get_last_measurement():
    return data_loader.load_json_data_as_dict_from(config.get_gps_last_measurement())


def get_averages_as_dict(gps_list):
    gps_data = 0

    for entry in gps_list:
        gps_data = gps_data + int(entry["num_sats"])

    size = len(gps_list)
    return {"num_sats": (gps_data / size)}


def get_records_as_dict(gps_list):
    gps_records = {
        'max_num_sats': -1,
        'gps_fastest_measurement_time': 16777216,
        'gps_slowest_measurement_time': 0
    }

    for entry in gps_list:
        for field_key in gps_records.keys():
            a_key = field_key.replace('gps_', '').replace("slowest_", "").replace("fastest_", "").replace("max_", "")
            if field_key.startswith("gps_fastest_"):
                if gps_records[field_key] > entry[a_key]:
                    gps_records[field_key] = entry[a_key]
            elif field_key.startswith("gps_slowest_"):
                if gps_records[field_key] < entry[a_key]:
                    gps_records[field_key] = entry[a_key]
            elif field_key.startswith("max_num_sats"):
                if gps_records[field_key] < int(entry[a_key]):
                    gps_records[field_key] = int(entry[a_key])
            else:
                print(
                    f'Interesting. field {field_key} with data {gps_records[field_key]} :: key {a_key} with data {entry[a_key]}')
    return gps_records


def update_for_gps_sensor(averages: dict, records: dict, measurement_date: str):
    gps_result = data_loader.load_list_of_dict_for(config.get_gps_data_for_date(measurement_date))
    averages.update(get_averages_as_dict(gps_result))
    records.update(get_records_as_dict(gps_result))
    gps_result.clear()
    return averages, records
