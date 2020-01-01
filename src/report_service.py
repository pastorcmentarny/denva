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
    path = utils.get_date_as_filename('report', 'json', utils.get_yesterday_date())
    if data_files.check_if_report_was_generated(path):
        return data_files.load_report(path)
    else:
        report = report_generator.generate_for_yesterday()
        email_sender_service.send(report, 'Report')
        data_files.save_report(report, utils.get_date_as_filename('report', 'json', utils.get_yesterday_date()))
        return report
