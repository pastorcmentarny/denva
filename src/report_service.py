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

import data_files
import email_sender_service
import report_generator
import utils

logger = logging.getLogger('app')


def generate_for_yesterday() -> dict:
    logger.info('Getting report for yesterday...')
    path = utils.get_date_as_filename('report', 'json', utils.get_yesterday_date())
    try:
        if data_files.check_if_report_was_generated(path):
            logger.info('Report was generated. Getting report from file.')
            return data_files.load_report(path)
        else:
            logger.info('Generating report')
            report = report_generator.generate_for_yesterday()
            email_sender_service.send(report, 'Report')
            data_files.save_report(report, utils.get_date_as_filename('report', 'json', utils.get_yesterday_date()))
            return report
    except Exception as e:
        logger.error('Unable to generate report due to {}.Returning empty report'.format(e), exc_info=True)
        return {'error': str(e)}