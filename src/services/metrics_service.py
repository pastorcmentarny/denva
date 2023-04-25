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
import copy
import logging
from datetime import date

import config
from common import data_files

DATE_OF_METRICS = "date"

METRIC_FLIGHT = 'flight'
METRIC_WEATHER = 'weather'
METRIC_LIGHT = 'light'
METRIC_POLLUTION = 'pollution'
METRIC_UV = 'uv'
METRIC_MOTION = 'motion'
METRIC_GAS = 'gas'
METRIC_AIR_QUALITY = 'air_quality'
METRICS_RGB = 'rgb'
METRICS_GPS = 'gps'
METRICS_CO2 = 'co2'
METRICS_SPECTROMETER = 'spectrometer'
COUNT = 'count'
ERRORS = 'errors'
OK = 'ok'

logger = logging.getLogger('server')
# remove OK part and left errors only as metrics purpose is to count errors
empty_stats = {
    DATE_OF_METRICS: str(date.today()),
    COUNT: 0,
    OK: {
        METRIC_AIR_QUALITY: 0,
        METRIC_GAS: 0,
        METRIC_MOTION: 0,
        METRIC_UV: 0,
        METRIC_POLLUTION: 0,
        METRIC_LIGHT: 0,
        METRIC_WEATHER: 0,
        METRIC_FLIGHT: 0,
        METRICS_RGB: 0,
        METRICS_GPS: 0,
        METRICS_CO2: 0,
        METRICS_SPECTROMETER : 0

    },
    ERRORS: {
        METRIC_AIR_QUALITY: 0,
        METRIC_GAS: 0,
        METRIC_MOTION: 0,
        METRIC_UV: 0,
        METRIC_POLLUTION: 0,
        METRIC_LIGHT: 0,
        METRIC_WEATHER: 0,
        METRIC_FLIGHT: 0,
        METRICS_RGB: 0,
        METRICS_GPS: 0,
        METRICS_CO2: 0,
        METRICS_SPECTROMETER : 0
    }

}


def setup():
    metrics_data = data_files.load_metrics_data(config.PI_DATA_PATH)
    if bool(metrics_data):
        return copy.deepcopy(metrics_data)
    else:
        return copy.deepcopy(empty_stats)


stats = copy.deepcopy(empty_stats)

metrics_names = [METRIC_AIR_QUALITY, METRIC_GAS, METRIC_MOTION, METRIC_UV, METRIC_POLLUTION,
                 METRIC_LIGHT, METRIC_WEATHER, METRIC_FLIGHT, METRICS_RGB, METRICS_GPS, METRICS_CO2]

metrics_results = [OK, ERRORS]


# TODO add load current_metrics on load
# TODO add metrics to report

def save_metrics():
    logger.info(f'saving metrics for {str(stats[DATE_OF_METRICS])}')
    result = data_files.save_metrics(stats, config.PI_DATA_PATH)
    logger.info(f'metrics {result}.')
    return result


def generate_daily_metrics():
    save_metrics()
    logger.info(f'Starting metrics for {str(stats[DATE_OF_METRICS])}')
    reset()
    stats[DATE_OF_METRICS] = str(date.today())
    logger.info('New metrics created.')


def add(metric: str, result: str):
    stats[COUNT] = stats[COUNT] + 1
    if metric not in metrics_names:
        logger.error(f'Unknown metrics ${metric}')
        stats[COUNT] = 1
        return
    elif result not in metrics_results:
        logger.error(f'Unknown metrics result ${result}')
        stats[COUNT] = stats[COUNT] - 1
        return

    if str(date.today()) != stats[DATE_OF_METRICS]:
        generate_daily_metrics()

    if stats[COUNT] % 10 == 0:
        save_metrics()

    if result == OK:
        stats[OK][metric] = stats[OK][metric] + 1
    else:
        stats[ERRORS][metric] = stats[ERRORS][metric] + 1


def get_currents_metrics() -> dict:
    return stats.copy()


def get_empty_metrics() -> dict:
    return empty_stats.copy()


def reset():
    global stats
    stats = copy.deepcopy(empty_stats)
