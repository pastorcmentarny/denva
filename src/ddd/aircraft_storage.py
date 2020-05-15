import csv
import json
import logging
from datetime import datetime

from common import dom_utils

logger = logging.getLogger('ddd')


def save_raw_reading(reading):
    airport_raw_data = "D:\\denva\\data\\{}".format(dom_utils.get_date_as_filename("aircraft", "txt", datetime.now()))
    try:
        with open(airport_raw_data, 'a+', encoding='utf-8') as aircraft_raw_file:
            json.dump(reading, aircraft_raw_file, ensure_ascii=False, indent=4)
    except Exception as exception:
        logger.error('Unable to save raw reading due to {}'.format(exception), exc_info=True)


def save_processed_data(result):
    airport_processed_data = "D:\\denva\\data\\{}".format(
        dom_utils.get_date_as_filename("aircraft-processed", "csv", datetime.now()))
    timestamp = datetime.now()
    try:
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
    except Exception as exception:
        logger.error('Unable to save processed reading due to {}'.format(exception), exc_info=True)
