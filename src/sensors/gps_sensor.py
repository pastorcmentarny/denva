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

import config
from gateways import local_data_gateway

logger = logging.getLogger('app')


def setup():
    logger.debug("Setting up GPS Sensor")
    return PA1010D()


gps = setup()


def get_no_vales(get_data_exception):
    return {config.FIELD_TIMESTAMP: datetime.now(), config.FIELD_GPS_LATITUDE: 0.0, config.FIELD_GPS_LONGITUDE: -0.0,
            config.FIELD_GPS_ALTITUDE: 0, config.FIELD_GPS_LAT_DIR: 'N', config.FIELD_GPS_LON_DIR: 'W',
            config.FIELD_GPS_GEO_SEP: '0', config.FIELD_GPS_NUM_SATS: '0', config.FIELD_GPS_QUAL: 0,
            config.FIELD_SPEED_OVER_GROUND: 0.0, config.FIELD_GPS_MODE_FIX_TYPE: '0', config.FIELD_GPS_PDOP: '0',
            config.FIELD_GPS_HDOP: '0', config.FIELD_GPS_VDOP: '0', '_i2c_addr': 16, '_i2c': 'x', '_debug': False,
            "error": str(get_data_exception)}


last = get_no_vales("Not init yet")


def get_measurement():
    global last
    try:
        updated = gps.update()
        if updated:
            last = updated
            local_data_gateway.post_metrics_update('gps', 'ok')
            return gps.data
        else:
            return last
    except Exception as exception:
        local_data_gateway.post_metrics_update('gps', 'errors')
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        return get_no_vales(exception)
