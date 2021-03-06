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

from pathlib import Path

from _datetime import datetime

from common import dom_utils

path = Path(__file__).parent / '../data/routine_daily.txt'


def load_routine() -> list:
    timetable = []
    file = open(path, 'r', encoding="UTF-8", newline='')
    content = file.readlines()
    for line in content:
        timetable.append(line.rstrip())
    return timetable


def get_now_and_next_event(current_time: int) -> list:
    routine = load_routine()
    for event in routine:
        event_in_minutes = dom_utils.convert_time_to_minutes(event)
        if current_time <= event_in_minutes:
            idx = routine.index(event)
            return [routine[idx - 1], routine[idx], dom_utils.is_weekend_day(datetime.now())]

    return [routine[len(routine) - 1], routine[0], dom_utils.is_weekend_day(datetime.now())]
