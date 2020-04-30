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
import os
from datetime import datetime

import config_service
from common import data_files, dom_utils
from gateways import web_data_gateway
from services import weather_service

UNKNOWN = "unknown"

logger = logging.getLogger('app')

information = {
    "crimes": UNKNOWN,
    "floods": UNKNOWN,
    "weather": [UNKNOWN],
    "o2": UNKNOWN
}


def is_rickmansworth_data_expired(date: str) -> bool:
    if not date:
        return True
    last_check = date.split('-')
    if len(last_check) != 3:
        return True
    today = datetime.now()
    # TODO refactor this shame
    if int(last_check[0]) == today.year and int(last_check[1]) == today.month and int(last_check[2]) == today.day:
        return False
    else:
        return True


def get_data_about_rickmansworth() -> dict:
    logger.debug('Getting crime,floods,weather and o2 issues data about Rickmansworth')
    ricky_file = config_service.get_data_path() + 'ricky.txt'
    if not os.path.exists(ricky_file):
        logger.info('File not exists. Getting ricky data from the web')
        get_data_from_web()
        logger.info('Got all data about Rickmansworth from web')
    else:
        logger.info('loading ricky data from the file')
        ricky_data = data_files.load_ricky(ricky_file)
        if is_rickmansworth_data_expired(ricky_data['date']):
            logger.info('Weather in the file is out of date, Getting weather from the web')
            get_data_from_web()
            logger.info('Got all data about Rickmansworth from web')
        else:
            logger.info('returning ricky from the file {}'.format(ricky_file))
            return ricky_data
    try:
        if not (information['crimes'] == UNKNOWN and information['crimes'] == UNKNOWN
                and information['weather'] == UNKNOWN and information['o2'] == UNKNOWN):
            today = datetime.now()
            information['date'] = '{}-{}-{}'.format(today.year, today.month, today.day)
            logger.info('Saving ricky data with timestamp {} to {}'.format(information['date'], ricky_file))
            data_files.save_dict_data_as_json(ricky_file, information)
    except Exception as e:
        logger.error('Unable to save data due to: {}'.format(e))

    return information


def get_data_from_web():
    information['crimes'] = web_data_gateway.get_crime()
    information['floods'] = web_data_gateway.get_flood()
    information['weather'] = weather_service.get_weather()
    information['o2'] = web_data_gateway.get_o2_status()


if __name__ == '__main__':
    dom_utils.setup_test_logging()
    print(get_data_about_rickmansworth())
