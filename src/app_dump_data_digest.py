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
import time
import traceback
from timeit import default_timer as timer

import config
from common import data_files
from ddd import aircraft_storage, aircraft_stats
from gateways import local_data_gateway

logger = logging.getLogger('ddd')
config.set_mode_to('ddd')
data_files.setup_logging(config.get_environment_log_path_for('ddd'))

refresh_rate_in_seconds = 15


def display_stats():
    aircraft_data = aircraft_storage.load_processed_data()
    logger.debug(aircraft_stats.count_aircraft_found(aircraft_data))
    logger.debug(aircraft_stats.get_flights_found(aircraft_data))


def digest():
    # load and save them to file for stats
    counter = 0
    errors = 0  # add when error was happened last time
    warnings = 0
    while True:
        counter += 1
        start_time = timer()

        result = local_data_gateway.get_data_for(config.get_url_for_dump1090(), 5)

        if 'error' in result:
            logger.error(result['error'])
            local_data_gateway.post_metrics_update('flight', 'errors')
            errors += 1
            logger.error('Errors: {}'.format(errors))
        else:
            aircraft_storage.save_raw_reading(result)
            aircraft_storage.save_processed_data(result)
            if counter % 2 == 0:
                local_data_gateway.post_healthcheck_beat('knyszogar', 'radar')
            local_data_gateway.post_metrics_update('flight', 'ok')

        end_time = timer()

        measurement = int((end_time - start_time) * 1000)
        measurement_time = str(measurement)  # in ms
        if measurement > config.slow_latency():
            warnings += 1
            logger.warning(f"Measurement {counter} was SLOW.It took {measurement} ms")
        else:
            logger.debug(f'Measurement took {measurement} ms.')

        if counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('knyszogar', 'digest')
        display_stats()
        measurement_message = 'Measurement no. {} It took {} milliseconds to process. Errors: {}. Warnings: {}'.format(
            counter,
            measurement_time,
            errors,
            warnings)
        logger.debug(measurement_message)
        remaining_time = refresh_rate_in_seconds - (float(measurement_time) / 1000)

        if remaining_time > 0:
            time.sleep(remaining_time)


if __name__ == '__main__':
    try:
        digest()
    except KeyboardInterrupt as keyboard_exception:
        logger.warning('Requesting shutdown: {}'.format(keyboard_exception), exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong: {}'.format(exception), exc_info=True)
    except BaseException as disaster:
        disaster_error_message = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(disaster_error_message)
        traceback.print_exc()
        logger.fatal(disaster_error_message, exc_info=True)
