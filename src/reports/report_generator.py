#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import csv
import logging
from datetime import datetime
from datetime import timedelta
from timeit import default_timer as timer

from common import dom_utils
from denva import denva_sensors_service
from gateways import local_data_gateway
from reports import averages, records
from services import information_service, sensor_warnings_service, tubes_train_service

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
        warnings = sensor_warnings_service.get_warnings_for(year, month, day)
        report['warning_counter'] = len(warnings)
        report['warnings'] = denva_sensors_service.count_warnings(warnings)
        report['records'] = records.get_records(data)
        report['avg'] = averages.get_averages(data)
        report['tube']['delays'] = tubes_train_service.count_tube_problems_for(year, month,
                                                                               day)  # move to separate function
        return report
    except:
        logger.error("Unable to generate  report.", exc_info=True)
        return {}


def load_data(year, month, day) -> list:
    csv_data = read_data_as_list_from_csv_file(day, month, year, 'sensor-log')
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
    return data


def load_enviro_data(year, month, day) -> list:
    csv_data = read_data_as_list_from_csv_file(day, month, year, 'sensor-enviro-log')
    data = []
    for row in csv_data:
        data.append({
            'timestamp': row[0],
            'temperature': '{:0.1f}'.format(float(row[1])),  # unit = "C"
            'light': '{:0.1f}'.format(float(row[4])),
            "oxidised": '{:0.2f}'.format(float(row[6])),  # "oxidised"    unit = "kO"
            'reduced': '{:0.2f}'.format(float(row[7])),  # unit = "kO"
            "nh3": '{:0.2f}'.format(float(row[8])),  # unit = "kO"
            "pm1": row[9],  # unit = "ug/m3"
            "pm25": row[10],  # unit = "ug/m3"
            "pm10": row[11],  # unit = "ug/m3"
            "measurement_time": row[12],
        })
    return data


def read_data_as_list_from_csv_file(day, month, year, log_file_name: str) -> list:
    path = dom_utils.get_filename_from_year_month_day(log_file_name, 'csv', year, month, day)
    sensor_log_file = dom_utils.fix_nulls(open('/home/pi/logs/' + path, 'r',
                                               newline=''))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    sensor_log_file.close()
    return csv_data


def generate_enviro_report_for_yesterday() -> dict:
    yesterday = datetime.now() - timedelta(days=1)
    evniro_report = {}

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
        year = yesterday.year
        month = yesterday.month
        day = yesterday.day
        data = load_enviro_data(year, month, day)
        evniro_report['measurement_counter'] = len(data)
        evniro_report['report_date'] = "{}.{}'{}".format(day, month, year)
        warnings = sensor_warnings_service.get_warnings_for(year, month, day)
        evniro_report['warning_counter'] = len(warnings)
        evniro_report['avg'] = averages.get_enviro_averages(data)
        evniro_report['records'] = records.get_enviro_records(data)
        return evniro_report
    except Exception as exception:
        logger.error("Unable to generate  report.", exc_info=True)
        return {'error': exception}


def generate():
    logger.info('Preparing to send denva report email')
    start_time = timer()
    email_data = {'now': {
        'denva': local_data_gateway.get_current_reading_for_denva(),
        'enviro': local_data_gateway.get_current_reading_for_enviro()
    },
        'report': {
            'denva': local_data_gateway.get_yesterday_report_for_denva(),
            'enviro': local_data_gateway.get_yesterday_report_for_enviro(),
            'rickmansworth': information_service.get_data_about_rickmansworth(),
        }
    }
    end_time = timer()
    logger.info('It took {} ms to generate data'.format(int((end_time - start_time) * 1000)))
    return email_data


def compare_two_reports(older_report: dict, newer_report: dict) -> dict:
    try:
        denva_avg_cpu_temperature = float(older_report['report']['denva']['avg']['cpu_temperature']) - float(
            newer_report['report']['denva']['avg']['cpu_temperature'])
        denva_avg_humidity = float(older_report['report']['denva']['avg']['humidity']) - float(
            newer_report['report']['denva']['avg']['humidity'])
        denva_avg_motion = float(older_report['report']['denva']['avg']['motion']) - float(
            newer_report['report']['denva']['avg']['motion'])
        denva_avg_pressure = float(older_report['report']['denva']['avg']['pressure']) - float(
            newer_report['report']['denva']['avg']['pressure'])
        denva_avg_temperature = float(older_report['report']['denva']['avg']['temperature']) - float(
            newer_report['report']['denva']['avg']['temperature'])
        denva_avg_uva = float(older_report['report']['denva']['avg']['uva']) - float(
            newer_report['report']['denva']['avg']['uva'])
        denva_avg_uvb = float(older_report['report']['denva']['avg']['uvb']) - float(
            newer_report['report']['denva']['avg']['uvb'])

        denva_records_biggest_motion = float(older_report['report']['denva']['records']['biggest_motion']) - float(
            newer_report['report']['denva']['records']['biggest_motion'])

        denva_records_cpu_temperature_max = float(
            older_report['report']['denva']['records']['cpu_temperature']['max']) - float(
            newer_report['report']['denva']['records']['cpu_temperature']['max'])
        denva_records_cpu_temperature_min = float(
            older_report['report']['denva']['records']['cpu_temperature']['min']) - float(
            newer_report['report']['denva']['records']['cpu_temperature']['min'])

        denva_records_highest_eco2 = int(older_report['report']['denva']['records']['highest_eco2']) - int(
            newer_report['report']['denva']['records']['highest_eco2'])
        denva_records_highest_tvoc = int(older_report['report']['denva']['records']['highest_tvoc']) - int(
            newer_report['report']['denva']['records']['highest_tvoc'])

        denva_records_cpu_humidity_max = float(older_report['report']['denva']['records']['humidity']['max']) - float(
            newer_report['report']['denva']['records']['humidity']['max'])
        denva_records_cpu_humidity_min = float(older_report['report']['denva']['records']['humidity']['min']) - float(
            newer_report['report']['denva']['records']['humidity']['min'])

        denva_records_uva_max = float(older_report['report']['denva']['records']['max_uv_index']['uva']) - float(
            newer_report['report']['denva']['records']['max_uv_index']['uva'])
        denva_records_uvb_max = float(older_report['report']['denva']['records']['max_uv_index']['uvb']) - float(
            newer_report['report']['denva']['records']['max_uv_index']['uvb'])

        denva_records_pressure_max = float(older_report['report']['denva']['records']['pressure']['max']) - float(
            newer_report['report']['denva']['records']['pressure']['max'])
        denva_records_pressure_min = float(older_report['report']['denva']['records']['pressure']['min']) - float(
            newer_report['report']['denva']['records']['pressure']['min'])

        denva_records_temperature_max = float(older_report['report']['denva']['records']['temperature']['max']) - float(
            newer_report['report']['denva']['records']['temperature']['max'])
        denva_records_temperature_min = float(older_report['report']['denva']['records']['temperature']['min']) - float(
            newer_report['report']['denva']['records']['temperature']['min'])

        warnings_cow = int(older_report['report']['denva']['warnings']['cow']) - int(
            newer_report['report']['denva']['warnings']['cow'])
        warnings_cthe = int(older_report['report']['denva']['warnings']['cthe']) - int(
            newer_report['report']['denva']['warnings']['cthe'])
        warnings_cthf = int(older_report['report']['denva']['warnings']['cthf']) - int(
            newer_report['report']['denva']['warnings']['cthf'])
        warnings_cthw = int(older_report['report']['denva']['warnings']['cthw']) - int(
            newer_report['report']['denva']['warnings']['cthw'])
        warnings_dfsl = int(older_report['report']['denva']['warnings']['dfsl']) - int(
            newer_report['report']['denva']['warnings']['dfsl'])
        warnings_dsl = int(older_report['report']['denva']['warnings']['dsl']) - int(
            newer_report['report']['denva']['warnings']['dsl'])
        warnings_fsl = int(older_report['report']['denva']['warnings']['fsl']) - int(
            newer_report['report']['denva']['warnings']['fsl'])
        warnings_hhe = int(older_report['report']['denva']['warnings']['hhe']) - int(
            newer_report['report']['denva']['warnings']['hhe'])
        warnings_hhw = int(older_report['report']['denva']['warnings']['hhw']) - int(
            newer_report['report']['denva']['warnings']['hhw'])
        warnings_hle = int(older_report['report']['denva']['warnings']['hle']) - int(
            newer_report['report']['denva']['warnings']['hle'])
        warnings_hlw = int(older_report['report']['denva']['warnings']['hlw']) - int(
            newer_report['report']['denva']['warnings']['hlw'])
        warnings_iqe = int(older_report['report']['denva']['warnings']['iqe']) - int(
            newer_report['report']['denva']['warnings']['iqe'])
        warnings_iqw = int(older_report['report']['denva']['warnings']['iqw']) - int(
            newer_report['report']['denva']['warnings']['iqw'])
        warnings_the = int(older_report['report']['denva']['warnings']['the']) - int(
            newer_report['report']['denva']['warnings']['the'])
        warnings_thw = int(older_report['report']['denva']['warnings']['thw']) - int(
            newer_report['report']['denva']['warnings']['thw'])
        warnings_tle = int(older_report['report']['denva']['warnings']['tle']) - int(
            newer_report['report']['denva']['warnings']['tle'])
        warnings_tlw = int(older_report['report']['denva']['warnings']['tlw']) - int(
            newer_report['report']['denva']['warnings']['tlw'])
        warnings_uvaw = int(older_report['report']['denva']['warnings']['uvaw']) - int(
            newer_report['report']['denva']['warnings']['uvaw'])
        warnings_uvbw = int(older_report['report']['denva']['warnings']['uvbw']) - int(
            newer_report['report']['denva']['warnings']['uvbw'])

        enviro_avg_light = float(older_report['report']['enviro']['avg']['light']) - float(
            newer_report['report']['enviro']['avg']['light'])
        enviro_avg_nh3 = float(older_report['report']['enviro']['avg']['nh3']) - float(
            newer_report['report']['enviro']['avg']['nh3'])
        enviro_avg_oxidised = float(older_report['report']['enviro']['avg']['oxidised']) - float(
            newer_report['report']['enviro']['avg']['oxidised'])
        enviro_avg_pm1 = float(older_report['report']['enviro']['avg']['pm1']) - float(
            newer_report['report']['enviro']['avg']['pm1'])
        enviro_avg_pm25 = float(older_report['report']['enviro']['avg']['pm25']) - float(
            newer_report['report']['enviro']['avg']['pm25'])
        enviro_avg_pm10 = float(older_report['report']['enviro']['avg']['pm10']) - float(
            newer_report['report']['enviro']['avg']['pm10'])
        enviro_avg_reduced = float(older_report['report']['enviro']['avg']['reduced']) - float(
            newer_report['report']['enviro']['avg']['reduced'])
        enviro_avg_temperature = float(older_report['report']['enviro']['avg']['temperature']) - float(
            newer_report['report']['enviro']['avg']['temperature'])

        enviro_records_light = float(older_report['report']['enviro']['records']['highest_light']) - float(
            newer_report['report']['enviro']['records']['highest_light'])
        # TODO add nh3 enviro_records_nh3 = float(older_report['report']['enviro']['records']['highest_nh3']) - float(newer_report['report']['enviro']['records']['highest_nh3'])
        enviro_records_oxidised = float(older_report['report']['enviro']['records']['highest_oxidised']) - float(
            newer_report['report']['enviro']['records']['highest_oxidised'])
        enviro_records_pm1 = float(older_report['report']['enviro']['records']['highest_pm1']) - float(
            newer_report['report']['enviro']['records']['highest_pm1'])
        enviro_records_pm25 = float(older_report['report']['enviro']['records']['highest_pm25']) - float(
            newer_report['report']['enviro']['records']['highest_pm25'])
        enviro_records_pm10 = float(older_report['report']['enviro']['records']['highest_pm10']) - float(
            newer_report['report']['enviro']['records']['highest_pm10'])
        enviro_records_reduced = float(older_report['report']['enviro']['records']['highest_reduced']) - float(
            newer_report['report']['enviro']['records']['highest_reduced'])
        enviro_records_temperature_max = float(
            older_report['report']['enviro']['records']['temperature']['max']) - float(
            newer_report['report']['enviro']['records']['temperature']['max'])
        enviro_records_temperature_min = float(
            older_report['report']['enviro']['records']['temperature']['min']) - float(
            newer_report['report']['enviro']['records']['temperature']['min'])

        diffferences = {
            "reports": {
                'first report': older_report['report']['denva']['report_date'],
                'second report': newer_report['report']['denva']['report_date'],
            },
            "denva": {
                "avg": {
                    "cpu_temperature": "{:.2f}".format(denva_avg_cpu_temperature),
                    "humidity": "{:.2f}".format(denva_avg_humidity),
                    "motion": "{:.2f}".format(denva_avg_motion),
                    "pressure": "{:.2f}".format(denva_avg_pressure),
                    "temperature": "{:.2f}".format(denva_avg_temperature),
                    "uva": "{:.2f}".format(denva_avg_uva),
                    "uvb": "{:.2f}".format(denva_avg_uvb),
                },
                "records": {
                    "biggest_motion": denva_records_biggest_motion,
                    "cpu_temperature": {
                        "max": "{:.2f}".format(denva_records_cpu_temperature_max),
                        "min": "{:.2f}".format(denva_records_cpu_temperature_min)
                    },
                    "highest_eco2": denva_records_highest_eco2,
                    "highest_tvoc": denva_records_highest_tvoc,
                    "humidity": {
                        "max": "{:.2f}".format(denva_records_cpu_humidity_max),
                        "min": "{:.2f}".format(denva_records_cpu_humidity_min)
                    },
                    "max_uv_index": {
                        "uva": "{:.2f}".format(denva_records_uva_max),
                        "uvb": "{:.2f}".format(denva_records_uvb_max)
                    },
                    "pressure": {
                        "max": "{:.2f}".format(denva_records_pressure_max),
                        "min": "{:.2f}".format(denva_records_pressure_min)
                    },
                    "temperature": {
                        "max": "{:.2f}".format(denva_records_temperature_max),
                        "min": "{:.2f}".format(denva_records_temperature_min)
                    }
                },
                "tube": {
                    "delays": {
                        "BakerlooTotalTime": "0 seconds.",
                        "CentralTotalTime": "0 seconds.",
                        "CircleTotalTime": "0 seconds.",
                        "DistrictTotalTime": "0 seconds.",
                        "HammersmithTotalTime": "0 seconds.",
                        "JubileeTotalTime": "0 seconds.",
                        "MetropolitanTotalTime": "0 seconds.",
                        "NorthernTotalTime": "0 seconds.",
                        "PiccadillyTotalTime": "0 seconds.",
                        "VictoriaTotalTime": "0 seconds.",
                        "WaterlooTotalTime": "0 seconds."
                    }
                },
                "warnings": {
                    "cow": warnings_cow,
                    "cthe": warnings_cthe,
                    "cthf": warnings_cthf,
                    "cthw": warnings_cthw,
                    "dfsl": warnings_dfsl,
                    "dsl": warnings_dsl,
                    "fsl": warnings_fsl,
                    "hhe": warnings_hhe,
                    "hhw": warnings_hhw,
                    "hle": warnings_hle,
                    "hlw": warnings_hlw,
                    "iqe": warnings_iqe,
                    "iqw": warnings_iqw,
                    "the": warnings_the,
                    "thw": warnings_thw,
                    "tle": warnings_tle,
                    "tlw": warnings_tlw,
                    "uvaw": warnings_uvaw,
                    "uvbw": warnings_uvbw
                }
            },
            "enviro": {
                "avg": {
                    "light": "{:.1f}".format(enviro_avg_light),
                    "nh3": "{:.1f}".format(enviro_avg_nh3),
                    "oxidised": "{:.1f}".format(enviro_avg_oxidised),
                    "pm1": "{:.1f}".format(enviro_avg_pm1),
                    "pm25": "{:.1f}".format(enviro_avg_pm25),
                    "pm10": "{:.1f}".format(enviro_avg_pm10),
                    "reduced": "{:.1f}".format(enviro_avg_reduced),
                    "temperature": "{:.1f}".format(enviro_avg_temperature),
                },
                "records": {
                    "highest_light": "{:.1f}".format(enviro_records_light),
                    "highest_nh3": "TO ADD",  # TODO add nh3
                    "highest_oxidised": "{:.1f}".format(enviro_records_oxidised),
                    "highest_pm1": "{:.1f}".format(enviro_records_pm1),
                    "highest_pm10": "{:.1f}".format(enviro_records_pm10),
                    "highest_pm25": "{:.1f}".format(enviro_records_pm25),
                    "highest_reduced": "{:.1f}".format(enviro_records_reduced),
                    "temperature": {
                        "max": "{:.1f}".format(enviro_records_temperature_max),
                        "min": "{:.1f}".format(enviro_records_temperature_min)
                    }
                }
            }
        }
        return diffferences
    except Exception as e:
        msg = 'Unable to compare two reports due to:'
        logger.warning('{} {}'.format(msg, e), exc_info=True)
        return {
            'error': '{} {}'.format(msg, e)
        }
