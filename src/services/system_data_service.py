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
import os
from datetime import datetime

import gc
import psutil

import config
import dom_utils
from services import common_service


def get_boot_time() -> str:
    return datetime.fromtimestamp(psutil.boot_time()).strftime("%d-%m'%Y @ %H:%M:%S")


# Used for server only, Pi use commands.get_system_info(
def get_system_information() -> dict:
    return {
        "CPU Speed": '{} MHz'.format(psutil.cpu_freq().current),
        "Memory Available": get_memory_available_in_mb(),
        "Disk Free": "{} MB".format(common_service.get_system_info()),
        "Uptime": get_boot_time()
    }


def get_memory_available_in_mb() -> str:
    return '{}MB'.format(dom_utils.convert_bytes_to_megabytes(psutil.virtual_memory().available))


# TODO use this for all services not only server
def get_system_warnings() -> list:
    problems = []
    memory_data = psutil.virtual_memory()
    memory_threshold = config.get_memory_available_threshold()
    if memory_data.available <= memory_threshold:
        problems.append('Memory available is low. Memory left: {} bytes.'.format(memory_data.available))
    free_space_left = common_service.get_system_info()
    if free_space_left <= config.get_disk_space_available_threshold():
        problems.append('Disk free space is low. Free space left: {} MB.'.format(free_space_left))
    return problems


def run_gc():
    result = {
        'memory_before': get_memory_available_in_mb(),
        'memory_after': '',
        'memory_saved': '',
        'memory_info_before': str(psutil.Process(os.getpid()).memory_full_info()),
        'gc_stats_before': gc.get_stats()
    }
    gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_SAVEALL)
    gc.collect()

    result['memory_after'] = get_memory_available_in_mb()
    result['memory_saved'] = dom_utils.get_int_number_from_text(
        result['memory_before']) - dom_utils.get_int_number_from_text(
        result['memory_after'])
    result['memory_info_after'] = str(psutil.Process(os.getpid()).memory_full_info())
    result['gc_stats_after'] = gc.get_stats()
    return result
