from datetime import datetime
import re
import config_service as config
from common import data_files, commands, dom_utils


def load_data_for_today() -> list:
    today = datetime.now()
    return data_files.load_data(today.year, today.month, today.day)


def get_sensor_log_file():
    return config.PI_PATH + dom_utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def get_sensor_log_file_at_server() -> str:
    return config.NETWORK_PATH + 'denva/' + dom_utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


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


def add_row(data, row):
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
            'cpu_temp': row[20],
            'eco2': row[21],
            'tvoc': row[22]
        }
    )

def get_warnings(data) -> dict:
    warnings = {}
    if type(data['temp']) is not float:
        data['temp'] = float(data['temp'])
    if data['temp'] < 16:
        warnings['temp'] = 'Temperature is too low [tle]. Current temperature is: {}'.format(str(data['temp']))
    elif data['temp'] < 18:
        warnings['temp'] = 'Temperature is low [tlw]. Current temperature is: {}'.format(str(data['temp']))
    elif data['temp'] > 25:
        warnings['temp'] = 'Temperature is high [thw]. Current temperature is: {}'.format(str(data['temp']))
    elif data['temp'] > 30:
        warnings['temp'] = 'Temperature is too high  [the]. Current temperature is: {}'.format(str(data['temp']))

    data['humidity'] = float(data['humidity'])

    if data['humidity'] < 30:
        warnings['humidity'] = 'Humidity is too low [hle]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] < 40:
        warnings['humidity'] = 'Humidity is low [hlw]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] > 60:
        warnings['humidity'] = 'Humidity is high [hhw]. Current humidity is: {}'.format(str(data['humidity']))
    elif data['humidity'] > 70:
        warnings['humidity'] = 'Humidity is too high [hhe]. Current humidity is: {}'.format(str(data['humidity']))

    data['uva_index'] = float(data['uva_index'])

    if data['uva_index'] > 6:
        warnings['uva_index'] = 'UV A is too high [uvae]. Current UV A is: {}'.format(str(data['uva_index']))

    data['uvb_index'] = float(data['uvb_index'])

    if data['uvb_index'] > 6:
        warnings['uvb_index'] = 'UV B is too high [uvbe]. Current UV B is: {}'.format(str(data['uvb_index']))

    data['cpu_temp'] = float(re.sub('[^0-9.]', '', data['cpu_temp']))

    if data['cpu_temp'] > config['sensor']['cpu_temp_fatal']:
        warnings['cpu_temp'] = 'CPU temperature is too high [cthf]. Current temperature is: {}'.format(
            str(data['cpu_temp']))
    elif data['cpu_temp'] > config['sensor']['cpu_temp_error']:
        warnings['cpu_temp'] = 'CPU temperature is very high [cthe]. Current temperature is: {}'.format(
            str(data['cpu_temp']))
    elif data['cpu_temp'] > config['sensor']['cpu_temp_warn']:
        warnings['cpu_temp'] = 'CPU temperature is high [cthw]. Current temperature is: {}'.format(
            str(data['cpu_temp']))

    data['motion'] = float(data['motion'])

    if data['motion'] > 1000:
        warnings['motion'] = 'Dom is shaking his legs [slw]. Value: {}'.format(str(data['motion']))

    if int(commands.get_space_available()) < 500:
        warnings['free_space'] = 'Low Free Space: {}'.format(commands.get_space_available() + 'MB')

    if int(data['eco2']) > 1000:
        warnings['eco2'] = 'High CO2 level: {}'.format(data['eco2'])

    if int(data['tvoc']) > 5000:
        warnings['tvoc'] = 'Air Quality BAD: {}'.format(data['tvoc'])
    elif int(data['tvoc']) > 1500:
        warnings['tvoc'] = 'Air Quality POOR: {}'.format(data['tvoc'])
    dom_utils.log_error_count(warnings)
    return warnings


def count_warnings(warnings) -> dict:
    warning_counter = {
        'the': 0,
        'thw': 0,
        'tle': 0,
        'tlw': 0,
        'hhe': 0,
        'hhw': 0,
        'hle': 0,
        'hlw': 0,
        'cthf': 0,
        'cthe': 0,
        'cthw': 0,
        'uvaw': 0,
        'uvbw': 0,
        'fsl': 0,
        'dfsl': 0,
        'dsl': 0,
        'cow': 0,
        'iqe': 0,
        'iqw': 0
    }

    for warning in warnings:
        if '[cthf]' in warning:
            warning_counter['cthf'] += 1
        elif '[cthe]' in warning:
            warning_counter['cthe'] += 1
        elif '[cthw]' in warning:
            warning_counter['cthw'] += 1
        elif '[the]' in warning:
            warning_counter['the'] += 1
        elif '[thw]' in warning:
            warning_counter['thw'] += 1
        elif '[tlw]' in warning:
            warning_counter['tlw'] += 1
        elif '[tle]' in warning:
            warning_counter['tle'] += 1
        elif '[hhe]' in warning:
            warning_counter['hhe'] += 1
        elif '[hhw]' in warning:
            warning_counter['hhw'] += 1
        elif '[hlw]' in warning:
            warning_counter['hlw'] += 1
        elif '[hle]' in warning:
            warning_counter['hle'] += 1
        elif '[uvaw]' in warning:
            warning_counter['uvaw'] += 1
        elif '[uvbw]' in warning:
            warning_counter['uvbw'] += 1
        elif '[fsl]' in warning:
            warning_counter['fsl'] += 1
        elif '[dfsl]' in warning:
            warning_counter['dfsl'] += 1
        elif '[dsl]' in warning:
            warning_counter['dsl'] += 1
        elif '[cow]' in warning:
            warning_counter['cow'] += 1
        elif '[iqw]' in warning:
            warning_counter['iqw'] += 1
        elif '[iqe]' in warning:
            warning_counter['iqe'] += 1

    return warning_counter