import csv
import datetime


def get_sensor_log_file() -> str:
    today = datetime.datetime.now()
    return '/home/pi/logs/sensor-log' + str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '.csv'


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
