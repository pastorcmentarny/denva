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
from common import data_files
import dom_utils
import logging

logger = logging.getLogger('app')

lines = ['Bakerloo', 'Central', 'Circle', 'District', 'Hammersmith-city', 'Jubilee', 'Metropolitan', 'Northern',
         'Piccadilly', 'Victoria', 'Waterloo-city']


def get_stats_file_for(year: str, month: str, day: str) -> list:
    date = dom_utils.get_filename_for_stats(year, month, day)
    return data_files.load_stats('/home/pi/logs/' + date)


def get_stats_file_for_today() -> list:
    return data_files.load_stats('/home/pi/logs/stats.log')


# TODO add for specific day
# TODO add for this month


def count_today_tube_problems(problem_list) -> dict:
    stats_counter = {
        'Bakerloo': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Central': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Circle': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'District': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Hammersmith-city': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Jubilee': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Metropolitan': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Northern': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Piccadilly': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Victoria': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Waterloo-city': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0,
            'Reduced service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        }
    }

    for problem in problem_list:
        columns = problem.split('::')
        timestamp = columns[0]
        tube_line = columns[1].strip()
        tube_status = columns[2].strip()

        for a_line in lines:
            if tube_line == a_line:
                if tube_status in stats_counter[a_line]:
                    stats_counter[a_line][tube_status] += 1
                else:
                    logger.error(f'Add {tube_status} to tube status!')

    return stats_counter
