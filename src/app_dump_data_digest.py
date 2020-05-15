"""
[
{"hex":"471f6f", "squawk":"0000", "flight":"", "lat":0.000000, "lon":0.000000, "validposition":0, "altitude":4975,  "vert_rate":1920,"track":69, "validtrack":1,"speed":190, "messages":3, "seen":231},
{"hex":"3c65c8", "squawk":"2565", "flight":"", "lat":0.000000, "lon":0.000000, "validposition":0, "altitude":0,  "vert_rate":-576,"track":89, "validtrack":1,"speed":127, "messages":4, "seen":248}
]
"""
import csv
import json
import logging
from datetime import datetime
from timeit import default_timer as timer

import time

from common import dom_utils
from gateways import local_data_gateway

logger = logging.getLogger('app')

refresh_rate_in_seconds = 15
airport_raw_data = "D:\\denva\\data\\{}".format(dom_utils.get_date_as_filename("aircraft", "txt", datetime.now()))
airport_processed_data = "D:\\denva\\data\\{}".format(
    dom_utils.get_date_as_filename("aircraft-processed", "csv", datetime.now()))


def counter():
    with open(airport_processed_data) as csv_file:
        aircraft_csv = csv.reader(csv_file)
        aircraft_data = list(aircraft_csv)
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
            with open(airport_raw_data, 'a+', encoding='utf-8') as aircraft_raw_file:
                json.dump(result, aircraft_raw_file, ensure_ascii=False, indent=4)

            timestamp = datetime.now()
            with open(airport_processed_data, 'a+', encoding='utf-8', newline='') as aircraft_processed_file:
                csv_writer = csv.writer(aircraft_processed_file)

                for entry in result:
                    if entry['flight'] != '':
                        csv_writer.writerow([timestamp,
                                             entry['hex'], entry['squawk'], entry['flight'].strip(), entry['lat'],
                                             entry['lon'], entry['validposition'], entry['altitude'],
                                             entry['vert_rate'], entry['track'], entry['validtrack'],
                                             entry['speed'], entry['messages'], entry['seen']
                                             ])
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
    except Exception as keyboard_exception:
        logger.error('Something went badly wrong\n{}'.format(keyboard_exception), exc_info=True)


