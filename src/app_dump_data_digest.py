import logging
from timeit import default_timer as timer

import time

import config_service
from common import data_files
from ddd import aircraft_storage, aircraft_stats
from gateways import local_data_gateway

logger = logging.getLogger('ddd')

refresh_rate_in_seconds = 15
max_latency = 200


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

        result = local_data_gateway.get_data_for("http://192.168.0.201:16601/data.json", 5)

        if 'error' in result:
            logger.error(result['error'])
            errors += 1
            print('Errors: {}'.format(errors))
        else:
            aircraft_storage.save_raw_reading(result)
            aircraft_storage.save_processed_data(result)

        end_time = timer()

        measurement = int((end_time - start_time) * 1000)
        measurement_time = str(measurement)  # in ms

        if measurement > max_latency:
            warnings += 1
            logger.warning("Measurement {} was slow.It took {} ms".format(counter, measurement))

        display_stats()
        msg = 'Measurement no. {} It took {} milliseconds to process. Errors: {}. Warnings: {}'.format(counter,
                                                                                                       measurement_time,
                                                                                                       errors,
                                                                                                       warnings)
        print(msg)
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
        logger.warning('Request to shutdown{}'.format(keyboard_exception), exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
