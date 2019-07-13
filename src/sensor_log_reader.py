import csv
import datetime
import time


def get_sensor_log_file() -> str:
    today = datetime.datetime.now()
    return '/home/pi/logs/sensor-log' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '.csv'


def get_records() -> list:
    start = time.time_ns()
    result = {
        'temperature': {
            'min': 100,
            'max': -100
        },
        'pressure': {
            'min': 10000,
            'max': 0
        },
        'humidity': {
            'min': 100,
            'max': -100
        },
        'max_uv_index': {
            'uva': -100,
            'uvb': -100
        },
        'biggest_motion': 0
    }

    data_records = load_data()
    for data_record in data_records:
        if float(data_record['temp']) > float(result['temperature']['max']):
            result['temperature']['max'] = data_record['temp']
        if float(data_record['temp']) < float(result['temperature']['min']):
            result['temperature']['min'] = data_record['temp']

        if float(data_record['pressure']) > float(result['pressure']['max']):
            result['pressure']['max'] = data_record['pressure']
        if float(data_record['pressure']) < float(result['pressure']['min']):
            result['pressure']['min'] = data_record['pressure']

        if float(data_record['humidity']) > float(result['humidity']['max']):
            result['humidity']['max'] = data_record['humidity']
        if float(data_record['humidity']) < float(result['humidity']['min']):
            result['humidity']['min'] = data_record['humidity']

        if float(data_record['uva_index']) > float(result['max_uv_index']['uva']):
            result['max_uv_index']['uva'] = data_record['uva_index']

        if float(data_record['uvb_index']) > float(result['max_uv_index']['uvb']):
            result['max_uv_index']['uvb'] = data_record['uvb_index']

        if float(data_record['motion']) > float(result['biggest_motion']):
            result['biggest_motion'] = data_record['motion']

        result['max_uv_index']['uva'] = round(float(result['max_uv_index']['uva']), 2)
        result['max_uv_index']['uvb'] = round(float(result['max_uv_index']['uvb']), 2)
        result['biggest_motion'] = str(int((float(result['biggest_motion']))))

    end = time.time_ns()
    return result


def load_data() -> list:
    sensor_log_file = open(get_sensor_log_file(), 'r', newline='')
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []

    for row in csv_data:
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
                'mz': row[18]
            }
        )

    sensor_log_file.close()
    return data
