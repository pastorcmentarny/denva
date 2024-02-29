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
from common import loggy
import dom_utils
from gateways import local_data_gateway

config.DOWN = 'DOWN'

DEVICE_SERVER = 'server'
DEVICE_DENVA2 = 'denva'
DEVICE_DENVA = 'denva'

FIELD_FREE_SPACE = 'Free Space'
FIELD_MEMORY_AVAILABLE = 'Memory Available'
KEY_SYSTEM = 'system'

logger = logging.getLogger('app')


# TODO refactor this method as it looks dupicate
def get_errors_from_data(data: dict) -> list:
    errors = []
    if KEY_SYSTEM not in data:
        return ['No data.']

    hc_result = local_data_gateway.get_all_healthcheck_from_all_services()
    if hc_result[DEVICE_DENVA] == config.DOWN:
        errors.append('Healthcheck failed for Denva')
    if hc_result[DEVICE_DENVA2] == config.DOWN:
        errors.append('Healthcheck failed for Denva2')
    if hc_result[DEVICE_SERVER] == config.DOWN:
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

    denva2_data = data[KEY_SYSTEM][DEVICE_DENVA2]
    if DEVICE_DENVA2 in data[KEY_SYSTEM] and FIELD_MEMORY_AVAILABLE in denva2_data:
        if dom_utils.get_int_number_from_text(denva2_data[FIELD_MEMORY_AVAILABLE]) < 128:
            errors.append('Memory available ON DENVA2 is VERY LOW.')
        if dom_utils.get_int_number_from_text(denva2_data[FIELD_FREE_SPACE]) < 128:
            errors.append('Free space on disk ON DENVA2 is VERY LOW.')
    else:
        errors.append('Denva2 data is missing.')

    loggy.log_error_count(errors)
    return errors
