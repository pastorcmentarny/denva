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
import os
from datetime import datetime
from timeit import default_timer as timer

import config
from common import loggy, commands
import dom_utils

logger = logging.getLogger('app')


def get_airplane_for_today():
    logger.info('Getting all flights with flights name today')
    return get_all_airplanes_for(datetime.now())


def get_airplane_for_yesterday():
    logger.info('Getting all flights with flights name yesterday')
    return get_all_airplanes_for(dom_utils.get_yesterday_datetime())


# TODO improve it
def get_all_airplanes_for(date: datetime) -> dict:
    start_time = timer()
    path = f"/home/ds/data/{date.year}/{date.month:02d}/{date.day:02d}/aircraft.txt"
    if not os.path.exists(path):
        return {'error': 'no file with airplane detected found.'}
    file = open(path, config.READ_MODE, newline=config.EMPTY)
    detected_entries = file.readlines()
    all_aircraft = []
    for row in detected_entries:
        row = row.split(',')
        if row[10] != config.EMPTY:
            all_aircraft.append(row[10].strip())
    result_as_set = set(all_aircraft)
    all_aircraft = (list(result_as_set))
    loggy.log_time('Getting airplane measurement', start_time, timer())
    return {'flights': all_aircraft}


def check_hc():
    return {
        'dump': commands.is_dump_active()
    }
