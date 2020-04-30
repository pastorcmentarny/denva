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
import logging
from datetime import datetime

from common import data_files, dom_utils, app_timer
from gateways import local_data_gateway
from mothership import app_server_service
from reports import report_generator
from services import email_sender_service
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


def create_and_store_it_if_needed(report_generation_cooldown):
    if data_files.is_report_file_exists():
        logger.info('Report already sent.')
        return report_generation_cooldown
    if app_timer.is_time_to_run_every_6_hours(report_generation_cooldown):
        email_data = report_generator.generate()
        email_sender_service.send(email_data, 'Report (via server)')
        data_files.save_report_at_server(email_data)
        return datetime.now()


def create_for_current_measurements():
    return {'information': information.get_information(),
            'denva': local_data_gateway.get_current_reading_for_denva(),
            'enviro': local_data_gateway.get_current_reading_for_enviro(),
            'warnings': local_data_gateway.get_current_warnings_for_all_services(),
            'logs': local_data_gateway.get_current_logs_for_all_services(),
            'system': app_server_service.get_current_system_information_for_all_services()}
