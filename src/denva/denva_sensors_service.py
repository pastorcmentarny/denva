from datetime import datetime

import commands
import config_service as config
import utils


def get_sensor_log_file():
    return config.PI_PATH + utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def get_last_measurement():
    entry = commands.get_last_line_from_log(get_sensor_log_file())
    data = entry.split(',')
    return get_data_row(data)


def get_data_row(row) -> dict:
    return {
        'timestamp': row[0],
        'temp': row[1],
        'pressure': row[2],
        'humidity': row[3],
        'gas_resistance': '{:0.2f}'.format(float(row[4])),
        'colour': row[5],
        'aqi': row[6],
        'uva_index': '{:0.2f}'.format(float(row[7])),
        'uvb_index': '{:0.2f}'.format(float(row[8])),
        'motion': row[9],
        'ax': '{:0.2f}'.format(float(row[10])),
        'ay': '{:0.2f}'.format(float(row[11])),
        'az': '{:0.2f}'.format(float(row[12])),
        'gx': '{:0.2f}'.format(float(row[13])),
        'gy': '{:0.2f}'.format(float(row[14])),
        'gz': '{:0.2f}'.format(float(row[15])),
        'mx': '{:0.2f}'.format(float(row[16])),
        'my': '{:0.2f}'.format(float(row[17])),
        'mz': '{:0.2f}'.format(float(row[18])),
        'cpu_temp': row[20],
        'eco2': row[21],
        'tvoc': row[22],
    }
