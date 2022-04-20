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

logger = logging.getLogger('app')


def setup():
    logger.debug("Setting up GPS Sensor")
    return PA1010D()


gps = setup()


def get_measurement():
    try:
        updated = gps.update()
        if updated:
            logger.debug(f'GPS data: {gps.data}')
            return gps.data
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        raise exception
