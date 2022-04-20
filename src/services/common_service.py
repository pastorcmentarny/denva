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
from datetime import datetime

import config
from common import commands
from services import system_data_service, log_metrics_service


def run_gc() -> dict:
    return system_data_service.run_gc()


def get_healthcheck(app_name: str) -> dict:
    return {"status": "UP",
            "app": app_name}


def get_log_app(number: int):
    return commands.get_lines_from_path(config.get_log_path_for('log_app'), number)


def get_log_hc(number: int):
    return commands.get_lines_from_path(config.get_log_path_for('log_hc'), number)


def get_log_ui(number: int):
    return commands.get_lines_from_path(config.get_log_path_for('log_ui'), number)


def get_system_info():
    return commands.get_system_info()


def reboot_device():
    return commands.reboot('Requested by UI')


def stop_device(app_name: str):
    return commands.halt(app_name)


def get_log_count_for(log_type: str):
    return log_metrics_service.get_current_log_metrics_for(config.get_log_path_for(f'log_{log_type}'))


# TODO for knyszogar
def get_log_count_from_path(log_file_name: str):
    today = datetime.now()
    path_name = f'/home/pi/knyszogardata/logs/{log_file_name}-{today.year}-{today.month:02d}-{today.day:02d}.txt'
    return log_metrics_service.get_current_knyszogar_log_metrics_for(path_name)
