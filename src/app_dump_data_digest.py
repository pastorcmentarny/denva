"""
[
{"hex":"471f6f", "squawk":"0000", "flight":"", "lat":0.000000, "lon":0.000000, "validposition":0, "altitude":4975,  "vert_rate":1920,"track":69, "validtrack":1,"speed":190, "messages":3, "seen":231},
{"hex":"3c65c8", "squawk":"2565", "flight":"", "lat":0.000000, "lon":0.000000, "validposition":0, "altitude":0,  "vert_rate":-576,"track":89, "validtrack":1,"speed":127, "messages":4, "seen":248}
]
"""
import csv
import logging
from datetime import datetime
from timeit import default_timer as timer

import time

from common import dom_utils
from ddd import aircraft_storage
from gateways import local_data_gateway

logger = logging.getLogger('ddd')

refresh_rate_in_seconds = 15


def counter():
    aircraft_data = aircraft_storage.load_processed_data()
    if aircraft_data:
        print("Data size: {}".format(len(aircraft_data)))
        flights = []
        for aircraft_row in aircraft_data:
            if len(aircraft_row) > 3:
                flights.append(aircraft_row[3])
        flights = set(flights)
        flights = list(flights)
        print("Found: {}".format(len(flights)))
        print(flights)


def digest():
    errors = 0
    while True:
        start_time = timer()

        result = local_data_gateway.get_data_for("http://192.168.0.201:16601/data.json", 5)

        if 'error' in result:
            logger.error(result['error'])
            errors += 1
            print('Errors: {}'.format(errors))
        else:
            aircraft_storage.save_raw_reading(result)

            aircraft_storage.save_processed_data(result)
            counter()
        end_time = timer()

        measurement_time = str(int((end_time - start_time) * 1000))  # in ms
        logger.debug('It took {} milliseconds to process.'.format(measurement_time))

        remaining_time = refresh_rate_in_seconds - (float(measurement_time) / 1000)

        if remaining_time > 0:
            time.sleep(remaining_time)


if __name__ == '__main__':
    dom_utils.setup_test_logging()
    try:
        digest()
    except KeyboardInterrupt as keyboard_exception:
        logger.warning('Request to shutdown{}'.format(keyboard_exception), exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
