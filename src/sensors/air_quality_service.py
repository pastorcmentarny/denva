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

from sgp30 import SGP30


logger = logging.getLogger('app')

sgp30 = SGP30()

air_quality_led_status = 0
counter = 0


def get_eco2_measurement_as_string():
    return str(sgp30.get_air_quality().equivalent_co2)


def get_tvoc_measurement_as_string():
    return str(sgp30.get_air_quality().total_voc)


def crude_progress_bar():
    global air_quality_led_status
    global counter
    counter = counter + 1
    logger.warning('Waiting.. {}s.\n'.format(counter))


def start_measurement():
    sgp30.start_measurement(crude_progress_bar)
