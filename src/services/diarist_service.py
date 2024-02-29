# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

from datetime import datetime

import logging

import config
from common import data_files

"""
Service to write down all events that happen
"""

logger = logging.getLogger('app')


def add(new_entry):
    path = config.get_path_diary_for_today()
    data_files.save_entry(to_line(new_entry), path)


def to_line(new_entry):
    now = datetime.now()
    timestamp = f'{now.year}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}{now.second:02d}'
    text = ''
    for element in new_entry:
        key, value = element, new_entry[element]
        text += f'{timestamp}::{value}'
    return text
