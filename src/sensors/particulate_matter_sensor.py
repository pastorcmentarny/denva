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
import time

from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError

from gateways import local_data_gateway

logger = logging.getLogger('app')

pms5003 = PMS5003()


def get_measurement():
    global pms5003
    p_1 = 0
    p_2 = 0
    p_10 = 0

    try:
        pms_data = pms5003.read()
        p_1 = float(pms_data.pm_ug_per_m3(1.0))
        p_2 = float(pms_data.pm_ug_per_m3(2.5))
        p_10 = float(pms_data.pm_ug_per_m3(10))
    except BaseException as pms_exception:
        logger.error(
            f'Unable to restart ICM20948 due to {type(pms_exception).__name__} throws : {pms_exception}',
            exc_info=True)
        logger.info('Restarting sensor.. (it will takes ... 5 seconds')
        pms5003 = PMS5003()
        time.sleep(5)

    return p_1, p_2, p_10
