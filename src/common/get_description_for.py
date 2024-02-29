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
import config

KEY_INFORMATION = 'information'

KEY_ACTION = 'action'

KEY_VALUE = 'value'

KEY_SCORE = 'score'
logger = logging.getLogger('app')


def uv(uv_index):
    if uv_index < 0:
        logger.warning(f'weird uv value: {uv_index}')
        return config.UNKNOWN
    if uv_index == 0:
        return "NONE"
    elif uv_index < 3:
        return "LOW"
    elif 3 <= uv_index < 6:
        return "MEDIUM"
    elif 6 <= uv_index < 8:
        return "HIGH"
    elif 8 <= uv_index <= 11:
        return "VERY HIGH"
    else:
        return "EXTREME"


def brightness(red, green, blue) -> str:
    max_value = max(red, green, blue)
    mid = (red + green + blue) / 3
    result = (max_value + mid) / 2

    if result < 16:
        return 'pitch black'
    elif 16 <= result < 64:
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
        logger.warning(f'weird brightness value: {result} for {red} {green} {blue}')
        return '?'


def motion(motion_data: dict) -> str:
    return f'Acc: {motion_data["ax"]:5.1f} {motion_data["ay"]:5.1f} {motion_data["az"]:5.1f} Gyro: {motion_data["gx"]:5.1f} {motion_data["gy"]:5.1f} {motion_data["gz"]:5.1f} Mag: {motion_data["mx"]:5.1f} {motion_data["my"]:5.1f} {motion_data["mz"]:5.1f}'


# based on https://www.idt.com/eu/en/document/whp/overview-tvoc-and-indoor-air-quality
def iqa_from_tvoc(tvoc: str) -> dict:
    result = {
        KEY_SCORE: config.UNKNOWN,
        KEY_VALUE: 0,
        KEY_ACTION: config.UNKNOWN,
        KEY_INFORMATION: config.UNKNOWN
    }
    tvoc_value = int(tvoc)
    if tvoc_value < 150:
        result[KEY_SCORE] = 'Very Good'
        result[KEY_VALUE] = tvoc_value
        result[KEY_ACTION] = 'No action required'
        result[KEY_INFORMATION] = 'Clean air'
    elif tvoc_value < 500:
        result[KEY_SCORE] = 'Good'
        result[KEY_VALUE] = tvoc_value
        result[KEY_ACTION] = 'Ventilation recommended.'
        result[KEY_INFORMATION] = 'Good Air Quality'
    elif tvoc_value < 1500:
        result[KEY_SCORE] = 'Medium'
        result[KEY_VALUE] = tvoc_value
        result[KEY_ACTION] = 'Ventilation required.'
        result[KEY_INFORMATION] = 'Air Quality is not good. (Not recommended for exposure for than year)'
    elif tvoc_value < 5000:
        result[KEY_SCORE] = 'POOR'
        result[KEY_VALUE] = tvoc_value
        result[KEY_ACTION] = 'Ventilate now!'
        result[KEY_INFORMATION] = 'Air Quality is POOR. (Not recommended for exposure for than month)'
    else:
        result[KEY_SCORE] = 'BAD'
        result[KEY_VALUE] = tvoc_value
        result[KEY_ACTION] = 'Use only if unavoidable!'
        result[KEY_INFORMATION] = 'Unacceptable Air Quality! Use only if unavoidable and only for short periods.'

    return result
