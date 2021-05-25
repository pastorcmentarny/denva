#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
* source: http://open-notify.org/Open-Notify-API/ISS-Location-Now/ http://open-notify.org/Open-Notify-API/
"""

import time
from datetime import datetime

from gateways import web_data_gateway

poland_square_border = {
    "west": {
        "latitude": 53.912817,
        "longitude": 14.185539
    },
    "north": {
        "latitude": 54.833614,
        "longitude": 18.171741
    },
    "east": {
        "latitude": 50.869520,
        "longitude": 24.144916
    },
    "south": {
        "latitude": 49.002326,
        "longitude": 22.859570
    }
}

# it is not accurate
uk_rectangle_border = {
    "west": {
        "latitude": 50.069559,
        "longitude": -5.718743
    },
    "north": {
        "latitude": 58.671823,
        "longitude": -3.376886
    },
    "east": {
        "latitude": 52.481091,
        "longitude": 1.763014
    },
    "south": {
        "latitude": 49.956746,
        "longitude": -5.207077
    }
}


def is_in_polish_border_zone(position: dict) -> bool:
    iss_latitude = float(position['latitude'])
    iss_longitude = float(position['longitude'])
    if iss_latitude > poland_square_border['north']['latitude'] or iss_latitude < poland_square_border['south'][
        'latitude']:
        return False
    if iss_longitude > poland_square_border['east']['longitude'] or iss_longitude < poland_square_border['west'][
        'longitude']:
        return False
    if poland_square_border['south']['latitude'] < iss_latitude < poland_square_border['north']['latitude'] and \
            poland_square_border['west']['longitude'] < iss_longitude < poland_square_border['east']['longitude']:
        print(f'ISS is at latitude:{iss_latitude} and longitude: {iss_longitude}')
        return True
    return False


def is_in_uk_border_zone(position: dict) -> bool:
    iss_latitude = float(position['latitude'])
    iss_longitude = float(position['longitude'])
    if iss_latitude > uk_rectangle_border['north']['latitude'] or iss_latitude < uk_rectangle_border['south'][
        'latitude']:
        return False
    if iss_longitude > uk_rectangle_border['east']['longitude'] or iss_longitude < uk_rectangle_border['west'][
        'longitude']:
        return False
    if uk_rectangle_border['south']['latitude'] < iss_latitude < uk_rectangle_border['north']['latitude'] and \
            uk_rectangle_border['west']['longitude'] < iss_longitude < uk_rectangle_border['east']['longitude']:
        print(f'ISS is at latitude:{iss_latitude} and longitude: {iss_longitude}')
        return True
    return False


# need to move utils for float comparison
# https://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


if __name__ == '__main__':
    counter = 0
    while True:
        counter += 1
        print(f'no.{counter} at {datetime.now()}')
        print('In Poland: ' + str(is_in_polish_border_zone(web_data_gateway.get_iss_location()['iss_position'])))
        print('In UK: ' + str(is_in_uk_border_zone(web_data_gateway.get_iss_location()['iss_position'])))
        time.sleep(5)
