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
import gc
import logging.config
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer

import smbus
from PIL import ImageFont

import config
import dom_utils

from common import data_files
from denva import denva2_service

from emails import email_sender_service
from gateways import local_data_gateway
from services import barometric_service, spectrometer_service, motion_service, gps_service

bus = smbus.SMBus(1)

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_14 = ImageFont.truetype(rr_path, 14)

logger = logging.getLogger('app')
config.set_mode_to('denva')
dom_utils.setup_logging('app', True)
logger.info('Starting application ... \n Press Ctrl+C to shutdown')

app_startup_time = datetime.now()

counter = 1
led_status = 0
averages = {}
records = {}


def collect_last_measurements():
    all_measurements = barometric_service.get_last_measurement() | gps_service.get_last_measurement() | motion_service.get_last_measurement() | spectrometer_service.get_last_measurement()
    data_files.save_dict_data_as_json("/home/ds/data/all-measurement.json", all_measurements)
    return all_measurements


def generate_warnings(measurement):
    logger.debug('Updating warnings for all sensors')
    warnings = denva2_service.get_current_warnings(measurement)
    data_files.save_list_to_file(warnings, config.get_today_warnings())
    logger.debug('done')


def update_averages():
    logger.debug('Updating averages for all sensors')
    data_files.save_dict_data_as_json("/home/ds/data/all-averages.json", averages)
    averages.clear()
    gc.collect()


def update_records():
    logger.debug('Updating records for all sensors')
    data_files.save_dict_data_as_json("/home/ds/data/all-records.json", records)
    records.clear()
    gc.collect()


def generate_yesterday_report_if_need():
    logger.info('Generating report ')
    start_time = timer()
    data_path = '/home/ds/data/'
    yesterday = dom_utils.get_yesterday_date()
    report_averages = {}
    report_records = {}

    report = {
        'report_date': dom_utils.get_date_as_text(yesterday),
        'time_to_generate': 0,
        'averages': {},
        'records': {},
        'last_measurement': data_files.load_json_data_as_dict_from("/home/ds/data/all-measurement.json"),
        'problems': []
    }

    barometric_path = dom_utils.get_date_as_filename('barometric-data', 'txt', yesterday)
    path = Path("{}/{}".format(data_path, barometric_path))
    if not path.exists():
        report['problems'].append(f'Path to barometric data {barometric_path} does NOT exist.')
    else:
        report_averages, report_records = barometric_service.update_for_barometric_sensor(report_averages,
                                                                                          report_records,
                                                                                          dom_utils.get_date_for_today())
    print(report_averages)
    print(report_records)

    gps_path = dom_utils.get_date_as_filename('gps-data', 'txt', yesterday)
    path = Path("{}/{}".format(data_path, gps_path))
    if not path.exists():
        report['problems'].append(f'Path to gps data {gps_path} does NOT exist.')
    else:
        report_averages, report_records = gps_service.update_for_gps_sensor(report_averages,
                                                                            report_records,
                                                                            dom_utils.get_date_for_today())
    print(report_averages)
    print(report_records)

    spectrometer_path = dom_utils.get_date_as_filename('spectrometer-data', 'txt', yesterday)
    path = Path("{}/{}".format(data_path, spectrometer_path))
    if not path.exists():
        report['problems'].append(f'Path to spectrometer data {spectrometer_path} does NOT exist.')
    else:
        report_averages, report_records = spectrometer_service.update_for_spectrometer(report_averages,
                                                                                       report_records,
                                                                                       dom_utils.get_date_for_today())
    print(report_averages)
    print(report_records)

    motion_path = dom_utils.get_date_as_filename('motion-data', 'txt', yesterday)
    path = Path("{}/{}".format(data_path, motion_path))
    if not path.exists():
        report['problems'].append(f'Path to motion data {motion_path} does NOT exist.')
    else:
        report_averages, report_records = motion_service.update_for_motion_sensor(report_averages,
                                                                                  report_records,
                                                                                  dom_utils.get_date_for_today())
    print(report_averages)
    print(report_records)

    report['averages'] = report_averages
    report['records'] = report_records
    end_time = timer()
    measurement_time = int((end_time - start_time) * 1000)  # in ms
    report['time_to_generate'] = f"%.2f ms" % (measurement_time / 1000)
    data_files.save_dict_data_as_json(
        f"/home/ds/data/{dom_utils.get_date_as_filename('report', 'json', datetime.now())}", report)


def main():
    loop_counter = 0
    generate_yesterday_report_if_need()
    while True:
        global averages
        global records
        loop_counter += 1
        logger.debug('Loop no.{}'.format(loop_counter))

        try:
            start_time = timer()
            all_measurements_data = collect_last_measurements()
            generate_warnings(all_measurements_data)

            if loop_counter % 2 == 0:
                local_data_gateway.post_healthcheck_beat('denva2', 'app')

            if loop_counter % 20 == 0:
                logger.info('inner loop')
                averages, records = barometric_service.update_for_barometric_sensor(averages, records,
                                                                                    dom_utils.get_date_for_today())
                gc.collect()

                averages, records = gps_service.update_for_gps_sensor(averages, records, dom_utils.get_date_for_today())
                gc.collect()

                averages, records = motion_service.update_for_motion_sensor(averages, records,
                                                                            dom_utils.get_date_for_today())
                gc.collect()

                averages, records = spectrometer_service.update_for_spectrometer(averages, records,
                                                                                 dom_utils.get_date_for_today())
                gc.collect()

                update_averages()
                update_records()

            end_time = timer()
            measurement_time = int((end_time - start_time) * 1000)  # in ms
            logger.info('Measurement no. {} took {} milliseconds to measure it.'
                        .format(loop_counter, measurement_time))

            remaining_time_to_sleep = 15 - (float(measurement_time) / 1000)

            if measurement_time > config.max_latency(fast=False):
                logger.warning("Measurement {} was slow.It took {} ms".format(loop_counter, measurement_time))

            if remaining_time_to_sleep > 0:
                time.sleep(remaining_time_to_sleep)  # it should be 5 seconds between measurements
        except Exception as measurement_exception:
            logger.error(f'Measurement no. {loop_counter} failed. Error: {measurement_exception}', exc_info=True)
            time.sleep(5)


def cleanup_before_exit():
    sys.exit(0)


if __name__ == '__main__':
    global points
    email_sender_service.send_ip_email('denva')
    try:
        main()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        cleanup_before_exit()
    except Exception as exception:
        print(f'Whoops. {exception}')
        traceback.print_exc()
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email("application", "Application crashed due to {}.".format(exception))
        cleanup_before_exit()
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
        cleanup_before_exit()
