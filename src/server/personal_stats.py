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

import config_service
from common import data_files
from common.gobshite_exception import GobshiteException

logger = logging.getLogger('app')


def convert_to_date_time(happen_at_time: str) -> datetime:
    date_as_array = happen_at_time.split('-')
    if len(date_as_array) == 3:
        return datetime(int(date_as_array[0]), int(date_as_array[1]), int(date_as_array[2]))
    elif len(date_as_array) == 5:
        return datetime(int(date_as_array[0]), int(date_as_array[1]), int(date_as_array[2]),
                        int(date_as_array[3]), int(date_as_array[4]))
    else:
        logger.warning('invalid data:{}'.format(happen_at_time))
        raise GobshiteException('passed crap data {}'.format(happen_at_time))


def get_time_in_days_as_text(event_time: datetime) -> str:
    result = int((datetime.now() - event_time).days) + 1
    text = 'day'
    if result > 1:
        text += 's'
    return '{} {}.'.format(result, text)


def __get_events():
    return data_files.load_json_data_as_dict_from(config_service.get_path_for_personal_events())


def get_personal_stats() -> dict:
    converted = {}
    events = __get_events()
    for event, happen_at_time in events.items():
        converted[event] = get_time_in_days_as_text(convert_to_date_time(happen_at_time))
    return converted
