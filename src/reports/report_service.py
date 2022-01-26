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
import logging
from datetime import datetime

import config
from common import data_files, app_timer
import dom_utils
from gateways import local_data_gateway
from server import app_server_service
from reports import report_generator
from emails import email_sender_service
from services import information_service as information

logger = logging.getLogger('app')


def generate_enviro_report_for_yesterday() -> dict:
    yesterday = dom_utils.get_yesterday_date()
    logger.info('Getting  report for enviro for {}'.format(yesterday))
    path = dom_utils.get_date_as_filename('report-enviro', 'json', yesterday)
    if data_files.check_if_report_was_generated(path):
        logger.info('Report was generated. Getting report from file using path: {}'.format(path))
        return data_files.load_report(path)
    else:
        logger.info('Generating report')
        report = report_generator.generate_enviro_report_for_yesterday()
        email_sender_service.send(report, 'Report')
        data_files.save_report(report, dom_utils.get_date_as_filename('report-enviro', 'json', yesterday))
        return report


def generate_for_yesterday() -> dict:
    logger.info('Getting report for yesterday...')
    path = dom_utils.get_date_as_filename('report', 'json', dom_utils.get_yesterday_date())
    try:
        if data_files.check_if_report_was_generated(path):
            logger.info('Report was generated. Getting report from file.')
            return data_files.load_report(path)
        else:
            logger.info('Generating report')
            report = report_generator.generate_for_yesterday()
            email_sender_service.send(report, 'Report')
            data_files.save_report(report,
                                   dom_utils.get_date_as_filename('report', 'json', dom_utils.get_yesterday_date()))
            return report
    except Exception as e:
        logger.error('Unable to generate report due to {}.Returning empty report'.format(e), exc_info=True)
        return {'error': str(e)}


def create_and_store_it_if_needed(report_generation_cooldown: datetime) -> datetime:
    if data_files.is_report_file_exists(config.PI_DATA_PATH):
        logger.debug('Report already sent.')
        return report_generation_cooldown
    if app_timer.is_time_to_send_report_email(report_generation_cooldown):
        logger.info('Generating report')
        email_data = report_generator.generate()
        email_sender_service.send(email_data, 'Report (via server)')
        data_files.save_report_at_server(email_data,config.SERVER_IP)
        return datetime.now()
    return report_generation_cooldown


def create_for_current_measurements():
    return {'information': information.get_data_about_rickmansworth(),
            'denva': local_data_gateway.get_current_reading_for_denva(),
            'enviro': local_data_gateway.get_current_reading_for_enviro(),
            'aircraft': local_data_gateway.get_current_reading_for_aircraft(),
            'warnings': local_data_gateway.get_current_warnings_for_all_services(),
            'logs': local_data_gateway.get_current_logs_for_all_services(),
            'system': app_server_service.get_current_system_information_for_all_services(),
            'status': local_data_gateway.get_data_for('http://192.168.0.203:5000/shc/get', 3)
            }


def get_last_two_days_report_difference() -> dict:
    two_days_exists = data_files.is_report_file_exists_for(dom_utils.get_two_days_ago_date())
    yesterday_ago = data_files.is_report_file_exists_for(dom_utils.get_yesterday_date())

    if not two_days_exists or not yesterday_ago:
        return {
            'error': 'Unable to generate difference between because at least one of the report do not exists.'
                     'Reports:2 days ago: {}. Yesterday: {}'.format(two_days_exists, yesterday_ago)
        }

    two_days_ago = data_files.load_report_on_server_on(dom_utils.get_two_days_ago_date())
    one_day_ago = data_files.load_report_on_server_on(dom_utils.get_yesterday_date())
    return report_generator.compare_two_reports(two_days_ago, one_day_ago)


def get_yesterday_report_from_server():
    yesterday = dom_utils.get_yesterday_date()
    logger.info('Getting report for: {}'.format(yesterday))
    if not data_files.is_report_file_exists():
        logger.info('Report is not generated. Creating now.')
        create_and_store_it_if_needed(yesterday)
    return data_files.load_report_on_server_on(yesterday)
