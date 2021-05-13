#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import logging

from enviroplus import gas

from gateways import local_data_gateway

logger = logging.getLogger('app')


def get_measurement():
    try:
        data = gas.read_all()
        oxidising = data.oxidising / 1000
        reducing = data.reducing / 1000
        nh3 = data.nh3 / 1000
        local_data_gateway.post_metrics_update('gas', 'OK')
        return oxidising, reducing, nh3
    except Exception as exception:
        logger.error(f'Unable to read from gas sensor due to {exception}')
        local_data_gateway.post_metrics_update('gas', 'errors')
        return 0, 0, 0
