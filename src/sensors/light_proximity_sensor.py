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

from gateways import local_data_gateway

logger = logging.getLogger('app')


def setup():
    try:
        logger.info('Starting ltr559 sensor')
        # Transitional fix for breaking change in LTR559
        from ltr559 import LTR559
        ltr559 = LTR559()
    except ImportError:
        import ltr559
        logger.info('ltr559 sensor started')
    return ltr559


ltr559 = setup()


def get_illuminance():
    try:
        return ltr559.get_lux()
    except Exception as light_proximity_exception:
        logger.error(
            f'Unable to read data from ltr559 (light) sensor due to {type(light_proximity_exception).__name__} throws : {light_proximity_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('light', 'errors')
        setup()
        return -1


# don't need proximity metrics
def get_proximity():
    try:
        return ltr559.get_proximity()
    except Exception as light_proximity_exception:
        logger.error(
            f'Unable to read data from ltr559 (light) sensor due to {type(light_proximity_exception).__name__} throws : {light_proximity_exception}',
            exc_info=True)
        local_data_gateway.post_metrics_update('light', 'errors')
        setup()
        return -1
