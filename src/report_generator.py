import csv
from datetime import datetime
from datetime import timedelta

import averages
import records
import sensor_warnings
import sensor_log_reader
import utils

report = {
    'report_date': 'today',
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
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return generate_for(yesterday)


def generate_for(date: datetime) -> dict:
    year = date.year
    month = date.month
    day = date.day
    data = load_data(year, month, day)
    report['measurement_counter'] = len(data)
    report['report_date'] = "{}.{}'{}".format(day, month, year)
    warnings = sensor_warnings.get_warnings_for(year, month, day)
    report['warning_counter'] = len(warnings)
    report['warnings'] = sensor_warnings.count_warnings(warnings)
    report['records'] = records.get_records(data)
    report['avg'] = averages.get_averages(data)
    return report


def load_data(year, month, day) -> list:
    path = utils.get_filename_from_year_month_day('sensor-log', 'csv', year, month, day)
    sensor_log_file = utils.fix_nulls(open('/home/pi/logs/' + path, 'r',
                                           newline=''))
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
