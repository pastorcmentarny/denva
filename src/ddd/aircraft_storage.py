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

import csv
import json
import logging
from datetime import date
from datetime import datetime
from pathlib import Path

import config
import dom_utils

ENCODING = 'utf-8'
DEFAULT_PATH = "{}/{}{}"

logger = logging.getLogger('ddd')


def save_raw_reading(reading):
    data_path = config.get_directory_path_for_aircraft()
    date_as_folders = dom_utils.get_date_as_folders_linux()
    Path("{}/{}".format(data_path, date_as_folders)).mkdir(parents=True, exist_ok=True)
    airport_raw_data = DEFAULT_PATH.format(data_path, date_as_folders,
                                           dom_utils.get_date_as_filename("aircraft", "txt", datetime.now()))
    try:
        with open(airport_raw_data, 'a+', encoding=ENCODING) as aircraft_raw_file:
            json.dump(reading, aircraft_raw_file, ensure_ascii=False, indent=4)
    except Exception as exception:
        logger.error('Unable to save raw reading due to {}'.format(exception), exc_info=True)


def save_processed_data(result):
    data_path = config.get_directory_path_for_aircraft()
    date_as_folders = dom_utils.get_date_as_folders_linux()
    Path("{}/{}".format(data_path, date_as_folders)).mkdir(parents=True, exist_ok=True)
    airport_processed_data = DEFAULT_PATH.format(data_path, date_as_folders,
                                                 dom_utils.get_date_as_filename("aircraft-processed", "csv",
                                                                                datetime.now()))
    timestamp = datetime.now()
    try:
        with open(airport_processed_data, 'a+', encoding=ENCODING, newline='') as aircraft_processed_file:
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


def load_processed_data() -> list:
    return load_processed_data_for(date.today())


def load_processed_for_yesterday() -> list:
    return load_processed_data_for(dom_utils.get_yesterday_date_as_date())


# add validator for loaded
def load_processed_data_for(specified_data: date) -> list:
    data_path = config.get_directory_path_for_aircraft()
    date_as_folders = dom_utils.get_date_as_folders_for(specified_data)
    airport_processed_data = DEFAULT_PATH.format(data_path, date_as_folders,
                                                 dom_utils.get_date_as_filename("aircraft-processed", "csv",
                                                                                dom_utils.to_datetime(specified_data)))
    try:
        with open(airport_processed_data) as csv_file:
            aircraft_csv = csv.reader(csv_file)
            return list(aircraft_csv)
    except Exception as exception:
        logger.error('Unable to load processed reading due to {}'.format(exception), exc_info=True)
        return []
