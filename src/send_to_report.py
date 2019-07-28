#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging

logger = logging.getLogger('app')


def send_current_data(data: dict) -> bool:
    url = '192.168.0.6:5000/update_data'
    try:
        response = requests.post(url, data=data)
        if response.ok:
            logger.info('request with data sent')
            return True
        else:
            logger.error('Unable to send data to server due to:' + response.raise_for_status())
    except Exception:
        logger.error('Unable to send report..', exc_info=True)

    return False
