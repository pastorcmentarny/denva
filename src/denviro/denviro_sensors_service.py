from datetime import datetime

import commands
import config_service as config
import utils


def get_sensor_log_file():
    return config.PI_PATH + utils.get_date_as_filename('sensor-enviro-log', 'csv', datetime.now())


def get_last_measurement():
    entry = commands.get_last_line_from_log(get_sensor_log_file())
    data = entry.split(',')
    return get_data_row(data)


def get_data_row(row) -> dict:
    data_row = {
        'timestamp': row[0],
        'temperature': '{:0.1f}'.format(float(row[1])),  # unit = "C"
        "oxidised": '{:0.2f}'.format(float(row[6])),  # "oxidised"    unit = "kO"
        'reduced': '{:0.2f}'.format(float(row[7])),  # unit = "kO"
        "nh3": '{:0.2f}'.format(float(row[8])),  # unit = "kO"
        "pm1": row[9],  # unit = "ug/m3"
        "pm25": row[10],  # unit = "ug/m3"
        "pm10": row[11],  # unit = "ug/m3"
        'measurement_time': row[12],
        'cpu_temp': row[13],
        'light': '{:0.1f}'.format(float(row[4])),
    }
    return data_row


def add_enviro_row(data, row):
    data.append(
        {
            'timestamp': row[0],
            'temperature': '{:0.1f}'.format(float(row[1])),  # unit = "C"
            "oxidised": '{:0.2f}'.format(float(row[6])),  # "oxidised"    unit = "kO"
            'reduced': '{:0.2f}'.format(float(row[7])),  # unit = "kO"
            "nh3": '{:0.2f}'.format(float(row[8])),  # unit = "kO"
            "pm1": row[9],  # unit = "ug/m3"
            "pm25": row[10],  # unit = "ug/m3"
            "pm10": row[11],  # unit = "ug/m3"
            'cpu_temp': row[13],
            'light': '{:0.1f}'.format(float(row[4])),
            'measurement_time': row[12]
        }
    )