import config
import dom_utils
from common import data_files


def get_warnings(measurement: dict) -> list:
    warnings = []
    if float(measurement[config.FIELD_GPS_NUM_SATS]) < 1:
        warnings.append(f"GPS not detecting any satellites.")

    return warnings

def get_last_measurement():
    return data_files.load_json_data_as_dict_from('/home/ds/data/gps-last-measurement.txt')


def get_averages_as_dict(gps_list):
    gps_data = 0

    for entry in gps_list:
        gps_data = gps_data + int(entry["num_sats"])

    size = len(gps_list)
    return {"num_sats" : (gps_data/size)}


def get_records_as_dict(gps_list):
    gps_records = {
        'max_num_sats' : -1,
        'gps_fastest_measurement_time': 16777216,
        'gps_slowest_measurement_time': 0
    }


    for entry in gps_list:
        for field_key in gps_records.keys():
            a_key = field_key.replace('gps','').replace("slowest_", "").replace("fastest_", "").replace("max_","")
            if field_key.startswith("gps_fastest_"):
                if gps_records[field_key] > entry[a_key]:
                    gps_records[field_key] = entry[a_key]
            elif field_key.startswith("num_sats"):
                if gps_records[field_key] < entry[a_key]:
                    gps_records[field_key] = entry[a_key]
            else:
                print(
                    f'Interesting. field {field_key} with data {gps_records[field_key]} :: key {a_key} with data {entry[a_key]}')
    return gps_records


def update_for_gps_sensor(averages, records):
        gps_result = data_files.load_list_of_dict_for(f"/home/ds/data/gps-data-{dom_utils.get_date_for_today()}.csv")
        averages.update(get_averages_as_dict(gps_result))
        records.update(get_records_as_dict(gps_result))
        gps_result.clear()