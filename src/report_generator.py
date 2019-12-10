import csv
import logging
from datetime import datetime
from datetime import timedelta

import averages
import records
import sensor_warnings
import tubes_train_service
import utils
import web_data

warnings_logger = logging.getLogger('warnings')
stats_log = logging.getLogger('stats')
logger = logging.getLogger('app')

report = {
    'report_date': 'today',
    'measurement_counter': 0,
    'warning_counter': 0,
    'warnings': {},  # TODO i believe i don't need specify anything as this dict will be overwritten
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
        'biggest_motion': 0,
        'highest_eco2': 0,
        'highest_tvoc': 0
    },
     "rickmansworth": {
        "crimes": "unknown",
        "floods": "unknown",
        "weather": ["unknown"],
        "o2": "unknown",
    },
    "tube": {
        "delays": {
            'BakerlooMD': 0,
            'BakerlooSD': 0,
            'BakerlooPS': 0,
            'BakerlooFS': 0,
            'BakerlooTotalTime': 0,
            'CentralMD': 0,
            'CentralSD': 0,
            'CentralPS': 0,
            'CentralFS': 0,
            'CentralTotalTime': 0,
            'CircleMD': 0,
            'CircleSD': 0,
            'CirclePS': 0,
            'CircleFS': 0,
            'CircleTotalTime': 0,
            'DistrictMD': 0,
            'DistrictSD': 0,
            'DistrictPS': 0,
            'DistrictFS': 0,
            'DistrictTotalTime': 0,
            'HammersmithMD': 0,
            'HammersmithSD': 0,
            'HammersmithPS': 0,
            'HammersmithFS': 0,
            'HammersmithTotalTime': 0,
            'JubileeMD': 0,
            'JubileeSD': 0,
            'JubileePS': 0,
            'JubileeFS': 0,
            'JubileeTotalTime': 0,
            'MetropolitanMD': 0,
            'MetropolitanSD': 0,
            'MetropolitanPS': 0,
            'MetropolitanFS': 0,
            'MetropolitanTotalTime': 0,
            'NorthernMD': 0,
            'NorthernSD': 0,
            'NorthernPS': 0,
            'NorthernFS': 0,
            'NorthernTotalTime': 0,
            'PiccadillyMD': 0,
            'PiccadillySD': 0,
            'PiccadillyPS': 0,
            'PiccadillyFS': 0,
            'PiccadillyTotalTime': 0,
            'VictoriaMD': 0,
            'VictoriaSD': 0,
            'VictoriaPS': 0,
            'VictoriaFS': 0,
            'VictoriaTotalTime': 0,
            'WaterlooMD': 0,
            'WaterlooSD': 0,
            'WaterlooPS': 0,
            'WaterlooFS': 0,
            'WaterlooTotalTime': 0
        }
    }
}


def generate_for_yesterday() -> dict:
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return generate_for(yesterday)


def generate_for(date: datetime) -> dict:
    try:
        # is below 2 lines looks stupid? yes, because it is
        warnings_logger.info("")
        stats_log.info("")
        '''
        why? as report is generated on next day, you need add log entry 
        logger can trigger TimedRotatingFileHandler event  and create file
        that is used by report service. 
        Why I used logger to store data? because I am lazy and i used most efficient way
        to store data I do analyse over later.
        '''
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
        report['tube']['delays'] = tubes_train_service.count_tube_problems_for(year, month, day)
        report['rickmansworth']['crimes'] = web_data.get_crime()
        report['rickmansworth']['floods'] = web_data.get_flood()
        report['rickmansworth']['weather'] = web_data.get_weather()
        report['rickmansworth']['o2'] = web_data.get_o2_status()
        return report
    except:
        logger.error("Unable to generate  report.", exc_info=True)
        return {}


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
            logger.warning("no data for ")
            row.insert(19, '?')
            row.insert(20, '?')
        try:
            row[21] == '?'
        except IndexError:
            logger.warning("no eco2 or tvoc data")
            row.insert(21, 0)
            row.insert(22, 0)
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
                'tvoc': row[22],
            }
        )
    sensor_log_file.close()
    return data
