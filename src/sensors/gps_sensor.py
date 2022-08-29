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

from pa1010d import PA1010D
from datetime import datetime

logger = logging.getLogger('app')


def setup():
    logger.debug("Setting up GPS Sensor")
    return PA1010D()


gps = setup()


def get_measurement():
    try:
        updated = gps.update()
        if updated:
            return gps.data
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        raise exception


def get_no_vales(get_data_exception):
    return {'timestamp': datetime.now(), 'latitude': 0.0, 'longitude': -0.0,
            'altitude': 0, 'lat_dir': 'N', 'lon_dir': 'W', 'geo_sep': '0', 'num_sats': '0', 'gps_qual': 0,
            'speed_over_ground': 0.0, 'mode_fix_type': '0', 'pdop': '0', 'hdop': '0', 'vdop': '0',
            '_i2c_addr': 16, '_i2c': 'x', '_debug': False, "error": str(get_data_exception)}
