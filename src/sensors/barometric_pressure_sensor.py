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
import sys
from icp10125 import ICP10125

from gateways import local_data_gateway
logger = logging.getLogger('app')

device = ICP10125()

DEFAULT_QNH = 1013.25
QNH = 1018

if len(sys.argv) > 1:
    QNH = float(sys.argv[1])


def calculate_altitude(pressure, qnh=DEFAULT_QNH):
    return 44330.0 * (1.0 - pow(pressure / qnh, (1.0 / 5.255)))


# TODO add try/catch for handle errors and         local_data_gateway.post_metrics_update('co2', 'errors')
def get_measurement() -> dict:
    try:
        pressure, temperature = device.measure()
        altitude = calculate_altitude(pressure / 100, qnh=QNH)
        return {
            "pressure": pressure / 100,
            "temperature": temperature,
            "altitude": altitude
        }
    except Exception as icp10125_exception:
        logger.error(
            f'Unable to read data from scd4x (co2 sensor) sensor due to {type(icp10125_exception).__name__} throws : {icp10125_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('air_quality', 'errors')
        return {
            "pressure": -1,
            "temperature": -1,
            "altitude": -1,
            "error": str(icp10125_exception)
        }
