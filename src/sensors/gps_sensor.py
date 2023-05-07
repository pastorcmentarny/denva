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
from common import loggy
from gateways import local_data_gateway

logger = logging.getLogger('app')


def setup():
    logger.debug("Setting up GPS Sensor")
    return PA1010D()


gps = setup()
logger.info('Enabling Enable or disable fix NMEA output time behind PPS function. (Default off)')
gps.send_command("PMTK255,1")
logger.info('Command sent.')


def get_no_vales(get_data_exception):
    return {config.FIELD_TIMESTAMP: datetime.now().strftime("%Y%m%d-%H%M%S"), config.FIELD_GPS_LATITUDE: 0.0, config.FIELD_GPS_LONGITUDE: -0.0,
            config.FIELD_GPS_ALTITUDE: 0, config.FIELD_GPS_LAT_DIR: 'N', config.FIELD_GPS_LON_DIR: 'W',
            config.FIELD_GPS_GEO_SEP: '0', config.FIELD_GPS_NUM_SATS: '0', config.FIELD_GPS_QUAL: 0,
            config.FIELD_GPS_SPEED_OVER_GROUND: 0.0, config.FIELD_GPS_MODE_FIX_TYPE: '0', config.FIELD_GPS_PDOP: '0',
            config.FIELD_GPS_HDOP: '0', config.FIELD_GPS_VDOP: '0', '_i2c_addr': 16, '_i2c': 'x', '_debug': False,
            "error": str(get_data_exception)}


def get_measurement():
    try:
        updated = gps.update()
        print(gps.data)
        if updated:
            gps_data = gps.data
            return {config.FIELD_TIMESTAMP: datetime.now().strftime("%Y%m%d-%H%M%S"),
                    config.FIELD_GPS_LATITUDE: gps_data[config.FIELD_GPS_LATITUDE],
                    config.FIELD_GPS_LONGITUDE: gps_data[config.FIELD_GPS_LONGITUDE],
                    config.FIELD_GPS_ALTITUDE: gps_data[config.FIELD_GPS_ALTITUDE],
                    config.FIELD_GPS_LAT_DIR: gps_data[config.FIELD_GPS_LON_DIR],
                    config.FIELD_GPS_LON_DIR: gps_data[config.FIELD_GPS_LON_DIR],
                    config.FIELD_GPS_GEO_SEP: gps_data[config.FIELD_GPS_GEO_SEP],
                    config.FIELD_GPS_NUM_SATS: gps_data[config.FIELD_GPS_NUM_SATS],
                    config.FIELD_GPS_QUAL: gps_data[config.FIELD_GPS_QUAL],
                    config.FIELD_GPS_SPEED_OVER_GROUND: gps_data[config.FIELD_GPS_SPEED_OVER_GROUND],
                    config.FIELD_GPS_MODE_FIX_TYPE: gps_data[config.FIELD_GPS_MODE_FIX_TYPE],
                    config.FIELD_GPS_PDOP: gps_data[config.FIELD_GPS_PDOP],
                    config.FIELD_GPS_HDOP: gps_data[config.FIELD_GPS_HDOP],
                    config.FIELD_GPS_VDOP: gps_data[config.FIELD_GPS_VDOP]
                    }
        else:
            loggy.log_with_print("Gps data wasn't updated")
            return get_no_vales("Gps data wasn't updated")
    except Exception as gps_exception:
        logger.error(
            f'Unable to read data from PA1010D (gps sensor) sensor due to {type(gps_exception).__name__} throws : {gps_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('gps', 'errors')
        return get_no_vales(gps_exception)
