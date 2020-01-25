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
from datetime import datetime


def get_app_uptime(app_startup_time) -> str:
    time_now = datetime.now()
    duration = time_now - app_startup_time
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    uptime = "App:"
    if days[0] > 0:
        uptime += "%d d," % (days[0])
    if hours[0] > 0:
        uptime += "%d h," % (hours[0])
    if minutes[0] > 0:
        uptime += "%d m," % (minutes[0])
    if seconds[0] > 0:
        uptime += "%d s," % (seconds[0])
    return uptime[:-1]


def is_time_to_send_report_email(previous_update_time) -> bool:
    return is_it_time(previous_update_time, 6 * 60 * 60)


def is_time_to_send_email(previous_update_time) -> bool:
    is_time_to_run_every_5_minutes(previous_update_time)


def is_time_to_run_every_5_minutes(previous_update_time) -> bool:
    return is_it_time(previous_update_time, 5 * 60)


def is_time_to_run_every_hour(previous_update_time) -> bool:
    return is_it_time(previous_update_time, 60 * 60)


def is_time_to_run_every_6_hours(previous_update_time) -> bool:
    return is_it_time(previous_update_time, 6 * 60 * 60)


def is_it_time(previous_update_time, time_difference) -> bool:
    time_now = datetime.now()
    duration = time_now - previous_update_time
    duration_in_s = duration.total_seconds()
    return duration_in_s > time_difference
