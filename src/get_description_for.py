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

logger = logging.getLogger('app')


def uv(uv_index):
    if uv_index == 0:
        return "NONE"
    elif uv_index < 3:
        return "LOW"
    elif 3 <= uv_index < 6:
        return "MEDIUM"
    elif 6 <= uv_index < 8:
        return "HIGH"
    elif 8 <= uv_index < 11:
        return "VERY HIGH"
    elif uv_index > 11:
        return "EXTREME"
    else:
        logger.warning('weird uv value: {}'.format(uv_index))
        return "UNKNOWN"


def brightness(r, g, b) -> str:
    max_value = max(r, g, b)
    mid = (r + g + b) / 3
    result = (max_value + mid) / 2

    if result < 16:
        return 'pitch black'
    elif 32 <= result < 64:
        return 'very dark'
    elif 64 <= result < 96:
        return 'dark'
    elif 96 <= result < 128:
        return 'bit dark'
    elif 128 <= result < 160:
        return 'grey'
    elif 160 <= result < 192:
        return 'bit bright'
    elif 192 <= result < 224:
        return 'bright'
    elif 224 <= result < 240:
        return 'very bright'
    elif 240 <= result < 256:
        return 'white'
    else:
        logger.warning('weird brightness value: {} for {} {} {}'.format(result, r, g, b))
        return '?'


def motion(motion_data: dict) -> str:
    return 'Acc: {:5.1f} {:5.1f} {:5.0f} Gyro: {:5.1f} {:5.1f} {:5.1f} Mag: {:5.1f} {:5.1f} {:5.1f}'.format(
        motion_data['ax'],
        motion_data['ay'],
        motion_data['az'],
        motion_data['gx'],
        motion_data['gy'],
        motion_data['gz'],
        motion_data['mx'],
        motion_data['my'],
        motion_data['mz'])
