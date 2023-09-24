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





def generate_for_yesterday() -> dict:
    logger.info('Getting report for yesterday...')
    try:
        path = dom_utils.get_date_as_filename('report', 'json', dom_utils.get_yesterday_date())
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
    except Exception as exception:
        logger.error('Unable to generate report due to {}.Returning empty report'.format(exception), exc_info=True)
        return {'error': str(exception)}


# TODO redo it as it mess
def create_and_store_it_if_needed(report_generation_cooldown: datetime, generate_now: bool = False) -> datetime:
    if data_files.is_report_file_exists(config.PI_DATA_PATH):
        logger.info('Report already sent.')
        return report_generation_cooldown
    if generate_now or app_timer.is_time_to_generate_report(report_generation_cooldown):
        logger.info('Generating report')
        email_data = report_generator.generate()
        email_sender_service.send(email_data, 'Report (via server)')
        data_files.save_report_at_server(email_data, config.PI_DATA_PATH)
        return datetime.now()
    return report_generation_cooldown
