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

import config
from common import commands
from services import system_data_service, log_metrics_service


def run_gc() -> dict:
    return system_data_service.run_gc()


def get_healthcheck(app_name: str) -> dict:
    return {"status": "UP",
            "app": app_name}


def get_system_info() -> dict:
    return commands.get_system_info()


def reboot_device():
    return commands.reboot('Requested by UI')


def stop_device(app_name: str):
    return commands.halt(app_name)


def get_log_count_for(log_type: str):
    return log_metrics_service.get_current_log_metrics_for(config.get_log_path_for(f'log_{log_type}'))
