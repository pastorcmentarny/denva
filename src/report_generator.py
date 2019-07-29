import csv
import datetime
from datetime import timedelta


import sensor_log_reader
import warning_reader
import warning_utils

report = {
    'measurement_counter': 0,
    'warning_counter': 0,
    'warnings': {
        'the': 0,
        'thw': 0,
        'tle': 0,
        'tlw': 0,
        'hhe': 0,
        'hhw': 0,
        'hle': 0,
        'hlw': 0,
        'uvaw': 0,
        'uvbw': 0,
    },
    "records": {
        'temperature': {
            'min': 0,
            'max': -0
        },
        'pressure': {
            'min': 0,
            'max': 0
        },
        'humidity': {
            'min': 0,
            'max': 0
        },
        'max_uv_index': {
            'uva': 0,
            'uvb': 0
        },
        'cpu_temperature': {
            'min': 0,
            'max': 0
        },
        'biggest_motion': 0
    }
}


def generate_for_yesterday() -> dict:
    today = datetime.datetime.now()
    yesterday = today - timedelta(days=1)
    return generate_for(yesterday.year, yesterday.month, yesterday.day)


def generate_for(year, month, day) -> dict:
    data = sensor_log_reader.get_sensor_log_file_for(year, month, day)
    report['measurement_counter'] = len(data)
    warnings = warning_reader.get_warnings_for(year, month, day)
    report['warning_counter'] = len(warnings)
    report['warnings'] = warning_utils.count_warnings(warnings)
    report['records'] = sensor_log_reader.get_records(year, month, day)
    report['avg'] = sensor_log_reader.get_averages(year, month, day)
    return report


def load_data(year, month, day) -> list:
    sensor_log_file = open('/home/pi/logs/sensor-log{}-{}-{}.csv'.format(str(year), str(month), str(day)), 'r',
                           newline='')
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []
    for row in csv_data:
        try:
            row[19] == '?'
        except IndexError:
            row.insert(19, '?')
            row.insert(20, '?')
        data.append(
            {
                'timestamp': row[0],
                'temp': row[1],
                'pressure': row[2],
                'humidity': row[3],
                'gas_resistance': row[4],
                'colour': row[5],
                'aqi': row[6],
                'uva_index': row[7],
                'uvb_index': row[8],
                'motion': row[9],
                'ax': row[10],
                'ay': row[11],
                'az': row[12],
                'gx': row[13],
                'gy': row[14],
                'gz': row[15],
                'mx': row[16],
                'my': row[17],
                'mz': row[18],
                'measurement_time': row[19],
                'cpu_temp': row[20]
            }
        )
    sensor_log_file.close()
    return data
