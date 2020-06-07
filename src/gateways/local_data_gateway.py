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
import json
import logging

import requests

import config_service
from services import system_data_service

logger = logging.getLogger('app')

REPORT_TIMEOUT = 150


def get_current_reading_for_denva() -> dict:
    return get_data_for('{}/now'.format(config_service.load_cfg()["urls"]['denva']))


def get_current_reading_for_enviro() -> dict:
    return get_data_for('{}/now'.format(config_service.load_cfg()["urls"]['enviro']))


def get_yesterday_report_for_denva() -> dict:
    return get_data_for('{}/report/yesterday'.format(config_service.load_cfg()["urls"]['denva']), REPORT_TIMEOUT)


def get_yesterday_report_for_enviro() -> dict:
    return get_data_for('{}/report/yesterday'.format(config_service.load_cfg()["urls"]['enviro']), REPORT_TIMEOUT)


def get_current_logs_for_all_services() -> dict:
    return {
        'app': {
            'denva': get_data_for('{}/log/app/recent'.format(config_service.load_cfg()["urls"]['denva'])),
            'enviro': get_data_for('{}/log/app/recent'.format(config_service.load_cfg()["urls"]['enviro'])),
            'delight': get_data_for('{}/log/app/recent'.format(config_service.load_cfg()["urls"]['delight']))
        },
        'hc': {
            'denva': get_data_for('{}/log/hc/recent'.format(config_service.load_cfg()["urls"]['denva'])),
            'enviro': get_data_for('{}/log/hc/recent'.format(config_service.load_cfg()["urls"]['enviro']))
        }
    }


def get_data_for(url: str, timeout: int = 3):  # ->list or dict
    try:
        with requests.get(url, timeout=timeout) as response:
            response.raise_for_status()
            data_response = response.text
            return json.loads(data_response)
    except Exception as whoops:
        return {'error': 'There was a problem: {}'.format(whoops)}


def get_current_warnings_for_all_services() -> dict:
    return {
        'denva': get_data_for(config_service.get_current_warnings_url_for('denva')),
        'enviro': get_data_for(config_service.get_current_warnings_url_for('enviro')),
        'delight': system_data_service.get_system_warnings(),
        'server': system_data_service.get_system_warnings()
    }


def get_all_healthcheck_from_all_services() -> dict:
    services = ['denva', 'enviro', 'server', 'delight']
    result = {}
    for service in services:
        result[service] = _get_hc_result(service)
    return result


def _get_hc_result(service: str):
    hc_result = get_data_for('{}/hc'.format(config_service.load_cfg()["urls"][service]))
    if 'error' in hc_result:
        return 'DOWN'
    return 'UP'


def get_current_reading_for_aircraft():
    return get_data_for('{}/flights/today'.format(config_service.load_cfg()["urls"]['delight']))


def get_yesterday_report_for_aircraft():
    return get_data_for('{}/flights/yesterday'.format(config_service.load_cfg()["urls"]['delight']))


def post_healthcheck_beat(device: str, app_type: str):
    url = config_service.get_system_hc_url()
    json_data = {'device': device, 'app_type': app_type}
    try:
        with requests.post(url, json=json_data, timeout=1) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem: {} using url {}, device {} and app_type {}'.format(whoops, url, device, app_type))


if __name__ == '__main__':
    post_healthcheck_beat('denva', 'app')
