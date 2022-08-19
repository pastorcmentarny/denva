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
import json
import logging

import requests

import config
from services import system_data_service

logger = logging.getLogger('app')

REPORT_TIMEOUT = 150
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}


def get_current_reading_for_denva() -> dict:
    return get_data_for('{}/now'.format(config.load_cfg()["urls"]['denva']))


def get_current_reading_for_enviro() -> dict:
    return get_data_for('{}/now'.format(config.load_cfg()["urls"]['enviro']))


def get_yesterday_report_for_denva() -> dict:
    return get_data_for('{}/report/yesterday'.format(config.load_cfg()["urls"]['denva']), REPORT_TIMEOUT)


def get_yesterday_report_for_enviro() -> dict:
    return get_data_for('{}/report/yesterday'.format(config.load_cfg()["urls"]['enviro']), REPORT_TIMEOUT)


def get_current_log_counts() -> dict:
    return {
        'app': {
            'denva': get_data_for('{}/log/count/app'.format(config.load_cfg()["urls"]['denva'])),
            'enviro': get_data_for('{}/log/count/app'.format(config.load_cfg()["urls"]['enviro'])),
            'delight': get_data_for('{}/log/count/app'.format(config.load_cfg()["urls"]['delight']))
        },
        'ui': {
            'denva': get_data_for('{}/log/count/ui'.format(config.load_cfg()["urls"]['denva'])),
            'enviro': get_data_for('{}/log/count/ui'.format(config.load_cfg()["urls"]['enviro'])),
            'delight': get_data_for('{}/log/count/ui'.format(config.load_cfg()["urls"]['delight']))
        }
    }


def get_current_logs_for_all_services() -> dict:
    return {
        'app': {
            'denva': get_data_for('{}/log/app/recent'.format(config.load_cfg()["urls"]['denva'])),
            'enviro': get_data_for('{}/log/app/recent'.format(config.load_cfg()["urls"]['enviro'])),
            'delight': get_data_for('{}/log/app/recent'.format(config.load_cfg()["urls"]['delight']))
        },
        'hc': {
            'denva': get_data_for('{}/log/hc/recent'.format(config.load_cfg()["urls"]['denva'])),
            'enviro': get_data_for('{}/log/hc/recent'.format(config.load_cfg()["urls"]['enviro']))
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
        'denva': get_data_for(config.get_current_warnings_url_for('denva')),
        'enviro': get_data_for(config.get_current_warnings_url_for('enviro')),
        'server': system_data_service.get_system_warnings(),
        'trases': get_data_for(config.get_current_warnings_url_for('trases'), 2),
    }


def get_all_healthcheck_from_all_services() -> dict:
    services = ['denva', 'enviro', 'server', 'delight']
    result = {}
    for service in services:
        result[service] = _get_hc_result(service)
    return result


def _get_hc_result(service: str):
    hc_result = get_data_for('{}/hc'.format(config.load_cfg()["urls"][service]))
    if 'error' in hc_result:
        return 'DOWN'
    return 'UP'


def get_current_reading_for_aircraft():
    return get_data_for('{}/flights/today'.format(config.load_cfg()["urls"]['denva']))


def get_yesterday_report_for_aircraft():
    return get_data_for('{}/flights/yesterday'.format(config.load_cfg()["urls"]['denva']))


def post_healthcheck_beat(device: str, app_type: str):
    url = config.get_system_hc_url()
    json_data = {'device': device, 'app_type': app_type}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem: {} using url {}, device {} and app_type {}'.format(whoops, url, device, app_type))


def post_healthcheck_reboot(device: str, app_type: str):
    url = config.get_system_hc_reboot_url()
    json_data = {'device': device, 'app_type': app_type}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem while sending reboot: {} using url {}, device {} and app_type {}'.format(whoops, url,
                                                                                                          device,
                                                                                                          app_type))


def post_metrics_update(metrics: str, result: str):
    url = config.get_metrics_service_url()
    json_data = {'metrics': metrics, 'result': result}
    try:
        with requests.post(url, json=json_data, timeout=1, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem while sending measurement: {} using url {}, metrics {} and result {}'.format(
                whoops, url, metrics, result))


def post_service_of(device: str, app_type: str, status: bool):
    print(f'{device}/{app_type} set status to {status} ')
    # TODO finish it!


def post_device_on_off(device: str, state: bool):
    url = config.get_service_on_off_url()
    json_data = {'device': device, 'state': state}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem: {} using url {}, device {} and state {}'.format(whoops, url, device, state))


def post_device_status(device: str, device_status: str):
    url = config.get_update_device_status_url()
    json_data = {'device': device, 'status': device_status}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            logger.info(json_data)
            logger.info(response.json())
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem: {} using url {}, device {} and state {}'.format(whoops, url, device, device_status))


def post_denva_measurement(json_data):
    url = config.get_post_denva_measurement_url()
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            logger.info(json_data)
            logger.info(response.json())
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem with sending measurement for denva with url {} due to {} '.format(url, whoops))


def post_denviro_measurement(json_data):
    url = config.get_post_denviro_measurement_url()
    json_data['cpu_temp'] = '40.0'
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            logger.info(json_data)
            logger.info(response.json())
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem with sending measurement for denviro with url {} due to {} '.format(url, whoops))


def add_entry_to_diary(new_entry: str):
    url = config.get_add_diary_entry_url()
    try:
        json_data = {'entry': new_entry}
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            logger.info(json_data)
            logger.info(response.json())
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem with sending measurement for denviro with url {} due to {} '.format(url, whoops))

def get_current_reading_for_trases():
    return None