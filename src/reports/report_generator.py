#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import csv
import logging
from datetime import datetime
from datetime import timedelta
from timeit import default_timer as timer

import config
import dom_utils
from gateways import local_data_gateway
from reports import averages, records
from services import information_service, sensor_warnings_service

warnings_logger = logging.getLogger('warnings')
logger = logging.getLogger('app')

report = {
    'report_date': 'today',
    config.FIELD_MEASUREMENT_COUNTER: 0,
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
        "stats_counter": {
            'Bakerloo': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Central': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Circle': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'District': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Hammersmith-city': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Jubilee': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Metropolitan': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Northern': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Piccadilly': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Victoria': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,

            },
            'Waterloo-city': {
                'Good Service': 0,
                'Minor Delays': 0,
                'Severe Delays': 0,
                'Part suspended': 0,
                'Part closure': 0,
                'Planned closure': 0,
                'Reduced service': 0,
                'Suspended': 0,
                'Service Closed': 0,
            }
        }
    }
}


def generate_for_yesterday() -> dict:
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return generate_for(yesterday)


def generate_for(date: datetime) -> dict:
    try:
        year = date.year
        month = date.month
        day = date.day
        data = load_data(year, month, day)
        logger.info(f'data length: {len(data)}')
        report[config.FIELD_MEASUREMENT_COUNTER] = len(data)
        report['report_date'] = "{}.{}'{}".format(day, month, year)
        logger.info('Getting records..')
        report['records'] = records.get_records(data)
        logger.info('Getting averages..')
        report['avg'] = averages.get_averages(data)
        return report
    except Exception as exception:
        logger.error(f"Unable to generate  report due to {exception}. Data {report}", exc_info=True)
        return {}


def load_data(year, month, day) -> list:
    csv_data = read_data_as_list_from_csv_file(day, month, year, 'sensor-log')
    data = []
    for row in csv_data:
        data.append(
            {
                config.FIELD_TIMESTAMP: row[config.DENVA_DATA_COLUMN_TIMESTAMP],
                config.FIELD_MEASUREMENT_TIME: row[config.DENVA_DATA_COLUMN_MEASUREMENT_TIME],
                config.FIELD_TEMPERATURE: row[config.DENVA_DATA_COLUMN_TEMP],
                config.FIELD_PRESSURE: row[config.DENVA_DATA_COLUMN_PRESSURE],
                config.FIELD_HUMIDITY: row[config.DENVA_DATA_COLUMN_HUMIDITY],
                config.FIELD_GAS_RESISTANCE: row[config.DENVA_DATA_COLUMN_GAS_RESISTANCE],
                config.FIELD_COLOUR: row[config.DENVA_DATA_COLUMN_COLOUR],
                config.FIELD_RED: row[config.DENVA_DATA_COLUMN_R],
                config.FIELD_GREEN: row[config.DENVA_DATA_COLUMN_G],
                config.FIELD_BLUE: row[config.DENVA_DATA_COLUMN_B],
                config.FIELD_CO2: row[config.DENVA_DATA_COLUMN_CO2],
                config.FIELD_CO2_TEMPERATURE: row[config.DENVA_DATA_COLUMN_CO2_TEMPERATURE],
                config.FIELD_RELATIVE_HUMIDITY: row[config.DENVA_DATA_COLUMN_RELATIVE_HUMIDITY],
                config.FIELD_CPU_TEMP: row[config.DENVA_DATA_COLUMN_CPU_TEMP],
                config.FIELD_ECO2: row[config.DENVA_DATA_COLUMN_ECO2],
                config.FIELD_TVOC: row[config.DENVA_DATA_COLUMN_TVOC],
                config.FIELD_GPS_NUM_SATS: 0  # FIXME
                # config.FIELD_GPS_NUM_SATS: row[config.DENVA_DATA_COLUMN_GPS_NUM_SATS]
            }
        )
    return data


def load_enviro_data(year, month, day) -> list:
    csv_data = read_data_as_list_from_csv_file(day, month, year, 'sensor-enviro-log')
    data = []
    for row in csv_data:
        data.append({
            config.FIELD_TIMESTAMP: row[0],
            'temperature': '{:0.1f}'.format(float(row[1])),  # unit = "C"
            'light': '{:0.1f}'.format(float(row[4])),
            config.FIELD_OXIDISED: '{:0.2f}'.format(float(row[6])),  # config.FIELD_OXIDISED    unit = "kO"
            'reduced': '{:0.2f}'.format(float(row[7])),  # unit = "kO"
            config.FIELD_NH3: '{:0.2f}'.format(float(row[8])),  # unit = "kO"
            config.FIELD_PM1: row[9],  # unit = "ug/m3"
            config.FIELD_PM25: row[10],  # unit = "ug/m3"
            config.FIELD_PM10: row[11],  # unit = "ug/m3"
            "measurement_time": row[12],
        })
    return data


def read_data_as_list_from_csv_file(day, month, year, log_file_name: str) -> list:
    path = dom_utils.get_filename_from_year_month_day(log_file_name, 'csv', year, month, day)
    sensor_log_file = dom_utils.fix_nulls(open(f'{config.PI_DATA_PATH}{path}', 'r',
                                               newline=''))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    sensor_log_file.close()
    return csv_data


def generate_enviro_report_for_yesterday() -> dict:
    yesterday = datetime.now() - timedelta(days=1)
    evniro_report = {}

    try:
        #TODO refactor
        # is below 2 lines looks stupid? yes, because it is
        warnings_logger.info("")
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
        evniro_report[config.FIELD_MEASUREMENT_COUNTER] = len(data)
        evniro_report['report_date'] = "{}.{}'{}".format(day, month, year)
        warnings = sensor_warnings_service.get_warnings_for(str(year), str(month), str(day))
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
        'enviro': local_data_gateway.get_current_reading_for_enviro(),
        'aircraft': local_data_gateway.get_current_reading_for_aircraft()
    },
        'report': {
            'denva': local_data_gateway.get_yesterday_report_for_denva(),
            'enviro': local_data_gateway.get_yesterday_report_for_enviro(),
            'aircraft': local_data_gateway.get_yesterday_report_for_aircraft(),
            'rickmansworth': information_service.get_data_about_rickmansworth(),
        },
        'status': local_data_gateway.get_data_for('http://192.168.0.203:5000/shc/get', 3)
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

        aircraft_count_difference = int(
            older_report['report']['aircraft']['detected']) - int(
            newer_report['report']['aircraft']['detected'])

        # TODO remove it in June2020
        if 'highest_nh3' in older_report['report']['enviro']['records'] and 'highest_nh3' in \
                newer_report['report']['enviro']['records']:
            enviro_records_nh3 = float(older_report['report']['enviro']['records']['highest_nh3']) - float(
                newer_report['report']['enviro']['records']['highest_nh3'])
        else:
            enviro_records_nh3 = 0.0
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

        differences = {
            "reports": {
                'first report': older_report['report']['denva']['report_date'],
                'second report': newer_report['report']['denva']['report_date'],
            },
            "denva": {
                "avg": {
                    "cpu_temperature": "{:.2f}".format(denva_avg_cpu_temperature),
                    config.FIELD_HUMIDITY: "{:.2f}".format(denva_avg_humidity),
                    "motion": "{:.2f}".format(denva_avg_motion),
                    config.FIELD_PRESSURE: "{:.2f}".format(denva_avg_pressure),
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
                    config.FIELD_HUMIDITY: {
                        "max": "{:.2f}".format(denva_records_cpu_humidity_max),
                        "min": "{:.2f}".format(denva_records_cpu_humidity_min)
                    },
                    "max_uv_index": {
                        "uva": "{:.2f}".format(denva_records_uva_max),
                        "uvb": "{:.2f}".format(denva_records_uvb_max)
                    },
                    config.FIELD_PRESSURE: {
                        "max": "{:.2f}".format(denva_records_pressure_max),
                        "min": "{:.2f}".format(denva_records_pressure_min)
                    },
                    "temperature": {
                        "max": "{:.2f}".format(denva_records_temperature_max),
                        "min": "{:.2f}".format(denva_records_temperature_min)
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
                    config.FIELD_LIGHT: "{:.1f}".format(enviro_avg_light),
                    config.FIELD_NH3: "{:.1f}".format(enviro_avg_nh3),
                    config.FIELD_OXIDISED: "{:.1f}".format(enviro_avg_oxidised),
                    config.FIELD_PM1: "{:.1f}".format(enviro_avg_pm1),
                    config.FIELD_PM25: "{:.1f}".format(enviro_avg_pm25),
                    config.FIELD_PM10: "{:.1f}".format(enviro_avg_pm10),
                    config.FIELD_REDUCED: "{:.1f}".format(enviro_avg_reduced),
                    "temperature": "{:.1f}".format(enviro_avg_temperature),
                },
                "records": {
                    "highest_light": "{:.1f}".format(enviro_records_light),
                    "highest_nh3": enviro_records_nh3,
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
            },
            "aircraft": {
                "count": aircraft_count_difference
            }
        }
        return differences
    except Exception as exception:
        msg = 'Unable to compare two reports due to:'
        logger.warning('{} {}'.format(msg, exception), exc_info=True)
        return {
            'error': '{} {}'.format(msg, exception)
        }
