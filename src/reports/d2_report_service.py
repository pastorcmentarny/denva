import logging
from pathlib import Path
from datetime import datetime
import config
import dom_utils
from common import data_files, app_timer, data_writer, data_loader
from timeit import default_timer as timer

from services import barometric_service, gps_service, spectrometer_service, motion_service

logger = logging.getLogger('app')


def get_report_for(report_path: str, report_date):
    report_file = Path(report_path)
    if report_file.exists():
        return data_loader.load_json_data_as_dict_from(report_path)
    else:
        logger.info('Report is not generated yet. Generating new one.')
        return generate_report(report_date)


def generate_yesterday_report_if_need(report_generation_cooldown, first_loop: bool = False):
    logger.debug('Checking if generating new report is needed.')
    if data_files.is_report_file_exists(config.PI_DATA_PATH):
        logger.debug('Report was already generated.')
        return report_generation_cooldown
    if first_loop or app_timer.is_time_to_generate_report(report_generation_cooldown):
        logger.info(f'Generating new report.'
                    f' Reasons: 1st?{first_loop},'
                    f'time to refresh? {app_timer.is_time_to_generate_report(report_generation_cooldown)}')
        generate_report(dom_utils.get_yesterday_datetime())
        return datetime.now()
    else:
        logger.debug('Report already sent.')
    return report_generation_cooldown


def generate_report(report_date):
    report_start_time = timer()
    data_path = '/home/ds/data/'

    report_averages = {}
    report_records = {}
    report = {
        'report_date': dom_utils.get_date_as_text(report_date),
        'time_to_generate': 0,
        'averages': {},
        'records': {},
        'last_measurement': data_loader.load_json_data_as_dict_from(config.get_all_mesaurements_as_one_path()),
        'problems': []
    }
    barometric_path = dom_utils.get_date_as_filename('barometric-data', 'txt', report_date)
    path = Path(f"{data_path}/{barometric_path}")
    if not path.exists():
        report['problems'].append(f'Path to barometric data {barometric_path} does NOT exist.')
    else:
        report_averages, report_records = barometric_service.update_for_barometric_sensor(report_averages,
                                                                                          report_records,
                                                                                          dom_utils.get_date_for_today())
    gps_path = dom_utils.get_date_as_filename('gps-data', 'txt', report_date)
    path = Path(f"{data_path}/{gps_path}")
    if not path.exists():
        report['problems'].append(f'Path to gps data {gps_path} does NOT exist.')
    else:
        report_averages, report_records = gps_service.update_for_gps_sensor(report_averages,
                                                                            report_records,
                                                                            dom_utils.get_date_for_today())
    spectrometer_path = dom_utils.get_date_as_filename('spectrometer-data', 'txt', report_date)
    path = Path(f"{data_path}/{spectrometer_path}")
    if not path.exists():
        report['problems'].append(f'Path to spectrometer data {spectrometer_path} does NOT exist.')
    else:
        report_averages, report_records = spectrometer_service.update_for_spectrometer(report_averages,
                                                                                       report_records,
                                                                                       dom_utils.get_date_for_today())
    motion_path = dom_utils.get_date_as_filename('motion-data', 'txt', report_date)
    path = Path(f"{data_path}/{motion_path}")
    if not path.exists():
        report['problems'].append(f'Path to motion data {motion_path} does NOT exist.')
    else:
        report_averages, report_records = motion_service.update_for_motion_sensor(report_averages,
                                                                                  report_records,
                                                                                  dom_utils.get_date_for_today())
    report['averages'] = report_averages
    report['records'] = report_records
    report_end_time = timer()
    measurement_time = int((report_end_time - report_start_time) * 1000)  # in ms
    report['time_to_generate'] = f"%.2f ms" % (measurement_time / 1000)
    data_writer.save_dict_data_as_json(
        f"/home/ds/data/{dom_utils.get_date_as_filename('report', 'json', datetime.now())}", report)
