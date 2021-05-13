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
import time
import traceback
from timeit import default_timer as timer

import config_service
from common import data_files
from ddd import aircraft_storage, aircraft_stats
from gateways import local_data_gateway

logger = logging.getLogger('ddd')

refresh_rate_in_seconds = 15


def display_stats():
    aircraft_data = aircraft_storage.load_processed_data()
    logger.info(aircraft_stats.count_aircraft_found(aircraft_data))
    logger.info(aircraft_stats.get_flights_found(aircraft_data))


def digest():
    # load and save them to file for stats
    counter = 0
    errors = 0  # add when error was happen last time
    warnings = 0
    while True:
        counter += 1
        start_time = timer()

        result = local_data_gateway.get_data_for(config_service.get_url_for_dump1090(), 5)

        if 'error' in result:
            logger.error(result['error'])
            local_data_gateway.post_metrics_update('flight', 'errors')
            errors += 1
            logger.error('Errors: {}'.format(errors))
        else:
            aircraft_storage.save_raw_reading(result)
            aircraft_storage.save_processed_data(result)
            if counter % 2 == 0:
                local_data_gateway.post_healthcheck_beat('other', 'radar')
            local_data_gateway.post_metrics_update('flight', 'OK')

        end_time = timer()

        measurement = int((end_time - start_time) * 1000)
        measurement_time = str(measurement)  # in ms

        if measurement > config_service.max_latency():
            warnings += 1
            logger.warning("Measurement {} was slow.It took {} ms".format(counter, measurement))

        if counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('other', 'digest')
        display_stats()
        msg = 'Measurement no. {} It took {} milliseconds to process. Errors: {}. Warnings: {}'.format(counter,
                                                                                                       measurement_time,
                                                                                                       errors,
                                                                                                       warnings)
        logger.info(msg)
        remaining_time = refresh_rate_in_seconds - (float(measurement_time) / 1000)

        if remaining_time > 0:
            time.sleep(remaining_time)


if __name__ == '__main__':
    config_service.set_mode_to('ddd')
    data_files.setup_logging('ddd')
    try:
        digest()
    except KeyboardInterrupt as keyboard_exception:
        logger.warning('Requesting shutdown: {}'.format(keyboard_exception), exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong: {}'.format(exception), exc_info=True)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
