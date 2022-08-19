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

from common import loggy
import dom_utils
from gateways import local_data_gateway

DEVICE_SERVER = 'server'
DEVICE_ENVIRO = 'enviro'
DEVICE_DENVA = 'denva'

FIELD_FREE_SPACE = 'Free Space'
FIELD_MEMORY_AVAILABLE = 'Memory Available'
KEY_SYSTEM = 'system'

logger = logging.getLogger('app')


def get_errors_from_data(data: dict) -> list:
    errors = []
    if KEY_SYSTEM not in data:
        return ['No data.']

    hc_result = local_data_gateway.get_all_healthcheck_from_all_services()
    if hc_result[DEVICE_DENVA] == 'DOWN':
        errors.append('Healthcheck failed for Denva')
    if hc_result[DEVICE_ENVIRO] == 'DOWN':
        errors.append('Healthcheck failed for Denviro')
    if hc_result[DEVICE_SERVER] == 'DOWN':
        errors.append('Healthcheck failed for Server')

    server_data = data[KEY_SYSTEM][DEVICE_SERVER]
    if DEVICE_SERVER in data[KEY_SYSTEM] and FIELD_MEMORY_AVAILABLE in server_data:
        if dom_utils.get_int_number_from_text(server_data[FIELD_MEMORY_AVAILABLE]) < 500:
            errors.append('Memory available on SERVER is VERY LOW.')

    if DEVICE_SERVER in data[KEY_SYSTEM] and FIELD_FREE_SPACE in server_data:
        if dom_utils.get_int_number_from_text(server_data[FIELD_FREE_SPACE]) < 128:
            errors.append('Free space on disk ON SERVER is VERY LOW.')
    else:
        errors.append('Server data is missing.')

    denva_data = data[KEY_SYSTEM][DEVICE_DENVA]
    if DEVICE_DENVA in data[KEY_SYSTEM] and FIELD_MEMORY_AVAILABLE in denva_data:
        if dom_utils.get_int_number_from_text(denva_data[FIELD_MEMORY_AVAILABLE]) < 128:
            errors.append('Memory available ON DENVA is VERY LOW.')
    if DEVICE_SERVER in data[KEY_SYSTEM] and FIELD_FREE_SPACE in server_data:
        if dom_utils.get_int_number_from_text(denva_data[FIELD_FREE_SPACE]) < 128:
            errors.append('Free space on disk ON DENVA is VERY LOW.')
    else:
        errors.append('Denva data is missing.')

    enviro_data = data[KEY_SYSTEM][DEVICE_ENVIRO]
    if DEVICE_ENVIRO in data[KEY_SYSTEM] and FIELD_MEMORY_AVAILABLE in enviro_data:
        if dom_utils.get_int_number_from_text(enviro_data[FIELD_MEMORY_AVAILABLE]) < 128:
            errors.append('Memory available ON ENVIRO is VERY LOW.')
        if dom_utils.get_int_number_from_text(enviro_data[FIELD_FREE_SPACE]) < 128:
            errors.append('Free space on disk ON ENVIRO is VERY LOW.')
    else:
        errors.append('Enviro data is missing.')

    loggy.log_error_count(errors)
    return errors
