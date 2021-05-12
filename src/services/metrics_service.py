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
import copy
import logging
from datetime import date

import config_service
from common import commands, data_files
from services import system_data_service
from systemhc import system_health_check_service

DATE_OF_METRICS = "date"

METRIC_FLIGHT = 'flight'
METRIC_GAS = 'gas'
METRIC_LIGHT = 'light'
METRIC_POLLUTION = 'pollution'
METRIC_UV = 'uv'
METRIC_MOTION = 'motion'
METRIC_COLOUR = 'colour'
METRIC_AIR_QUALITY = 'air_quality'
METRIC_ENVIRONMENT = 'environment'
COUNT = 'count'
ERRORS = 'errors'
OK = 'OK'

logger = logging.getLogger('metrics')

empty_stats = {
    DATE_OF_METRICS: str(date.today()),
    COUNT: 0,
    OK: {
        METRIC_ENVIRONMENT: 0,
        METRIC_AIR_QUALITY: 0,
        METRIC_COLOUR: 0,
        METRIC_MOTION: 0,
        METRIC_UV: 0,
        METRIC_POLLUTION: 0,
        METRIC_LIGHT: 0,
        METRIC_GAS: 0,
        METRIC_FLIGHT: 0

    },
    ERRORS: {
        METRIC_ENVIRONMENT: 0,
        METRIC_AIR_QUALITY: 0,
        METRIC_COLOUR: 0,
        METRIC_MOTION: 0,
        METRIC_UV: 0,
        METRIC_POLLUTION: 0,
        METRIC_LIGHT: 0,
        METRIC_GAS: 0,
        METRIC_FLIGHT: 0
    }

}

stats = copy.deepcopy(empty_stats)

metrics_names = [METRIC_ENVIRONMENT, METRIC_AIR_QUALITY, METRIC_COLOUR, METRIC_MOTION,
                 METRIC_UV, METRIC_POLLUTION, METRIC_LIGHT, METRIC_GAS, METRIC_FLIGHT]

metrics_results = [OK, ERRORS]


def generate_daily_metrics():
    logger.info(f'saving metrics for ${str(stats[DATE_OF_METRICS])}')
    result = data_files.save_metrics(stats)
    logger.info(f'metrics saved. Starting metrics for ${str(stats[DATE_OF_METRICS])}')
    reset()
    stats[DATE_OF_METRICS] = str(date.today())
    logger.info('New metrics created.')
    return result


def add(what: str, result: str):
    stats[COUNT] = stats[COUNT] + 1
    if what not in metrics_names:
        logger.error(f'Unknown metrics ${what}')
        stats[COUNT] = stats[COUNT] - 1
        return
    elif result not in metrics_results:
        logger.error(f'Unknown metrics result ${result}')
        stats[COUNT] = stats[COUNT] - 1
        return

    if str(date.today()) != stats[DATE_OF_METRICS]:
        generate_daily_metrics()

    if result == OK:
        stats[OK][what] = stats[OK][what] + 1
    else:
        stats[ERRORS][what] = stats[ERRORS][what] + 1


def run_gc() -> dict:
    return system_data_service.run_gc()


def get_system_hc():
    return system_health_check_service.get_system_healthcheck()


def get_log_hc(number: int):
    return commands.get_lines_from_path(config_service.get_log_path_for('log_hc'), number)


def get_log_ui(number: int):
    return commands.get_lines_from_path(config_service.get_log_path_for('log_ui'), number)


def get_system_info():
    return commands.get_system_info()


def get_currents_metrics() -> dict:
    return stats.copy()


def get_ping_test_results():
    return None


def reset():
    global stats

    stats = copy.deepcopy(empty_stats)
    print(f'stats ${stats}')
    print(f'empty stats ${empty_stats}')
