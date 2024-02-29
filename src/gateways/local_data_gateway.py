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


# TODO move to config
def get_current_reading_for_denva() -> dict:
    return get_data_for(f'{config.load_cfg()["urls"][config.KEY_DENVA_ONE]}/now')


def get_current_reading_for_denva_two() -> dict:
    return get_data_for(f'{config.load_cfg()["urls"]["denva2"]}/now')


def get_yesterday_report_for_denva() -> dict:
    return get_data_for(f'{config.load_cfg()["urls"][config.KEY_DENVA_ONE]}/report/yesterday', REPORT_TIMEOUT)


def get_yesterday_report_for_denva_two() -> dict:
    return get_data_for(f'{config.load_cfg()["urls"][config.KEY_DENVA_TWO]}/report/yesterday', REPORT_TIMEOUT)


def get_current_log_counts() -> dict:
    return {
        'app': {
            config.KEY_DENVA_ONE: get_data_for(
                f'{config.load_cfg()["urls"][config.KEY_DENVA_ONE]}/log/count/app'),
            config.KEY_DENVA_TWO: get_data_for(
                f'{config.load_cfg()["urls"][config.KEY_DENVA_TWO]}/log/count/app')
        },
        'ui': {
            config.KEY_DENVA_ONE: get_data_for(
                f'{config.load_cfg()["urls"][config.KEY_DENVA_ONE]}/log/count/ui'),
            config.KEY_DENVA_TWO: get_data_for(
                f'{config.load_cfg()["urls"][config.KEY_DENVA_TWO]}/log/count/ui')
        }
    }


def get_current_logs_for_all_services() -> dict:
    return {
        'app': {
            config.KEY_DENVA_ONE: get_data_for(
                f'{config.load_cfg()["urls"][config.KEY_DENVA_ONE]}/log/app/recent'),
            config.KEY_DENVA_TWO: get_data_for(
                f'{config.load_cfg()["urls"][config.KEY_DENVA_TWO]}/log/app/recent')
        },
        'hc': {
            config.KEY_DENVA_ONE: get_data_for(
                f'{config.load_cfg()["urls"][config.KEY_DENVA_ONE]}/log/hc/recent'),
            config.KEY_DENVA_TWO: get_data_for(
                f'{config.load_cfg()["urls"][config.KEY_DENVA_TWO]}/log/hc/recent')
        }
    }


def get_data_for(url: str, timeout: int = 3):  # ->list or dict
    try:
        with requests.get(url, timeout=timeout) as response:
            response.raise_for_status()
            data_response = response.text
            return json.loads(data_response)
    except Exception as whoops:
        return {'error': f'There was a problem: {whoops}'}


def get_current_warnings_for_all_services() -> dict:
    return {
        config.KEY_DENVA_ONE: get_data_for(config.get_current_warnings_url_for(config.KEY_DENVA_ONE)),
        config.KEY_DENVA_TWO: get_data_for(config.get_current_warnings_url_for(config.KEY_DENVA_TWO)),
        config.KEY_SERVER: system_data_service.get_system_warnings()
    }


def get_all_healthcheck_from_all_services() -> dict:
    services = [config.KEY_DENVA_ONE, config.KEY_DENVA_TWO, config.KEY_SERVER]
    result = {}
    for service in services:
        result[service] = _get_hc_result(service)
    return result


def _get_hc_result(service: str):
    hc_result = get_data_for(f'{config.load_cfg()["urls"][service]}/hc')
    if 'error' in hc_result:
        return 'OFF'
    return 'OK'


def get_current_reading_for_aircraft():
    return get_data_for(f'{config.load_cfg()["urls"][config.KEY_DENVA_ONE]}/flights/today')


def get_yesterday_report_for_aircraft():
    return get_data_for(f'{config.load_cfg()["urls"][config.KEY_DENVA_ONE]}/flights/yesterday')


def post_healthcheck_beat(device: str, app_type: str):
    logger.debug(f'Posting health check for {device}/{app_type}')
    url = config.get_system_hc_url()
    json_data = {'device': device, 'app_type': app_type}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            f'There was a problem: {whoops} using url {url}, device {device} and app_type {app_type}')


def post_metrics_update(metrics: str, result: str):
    url = config.get_metrics_service_url()
    json_data = {'metrics': metrics, 'result': result}
    try:
        with requests.post(url, json=json_data, timeout=1, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            f'There was a problem while sending measurement: {whoops} using url {url}, metrics {metrics} and result {result}')


def post_device_on_off(device: str, state: bool):
    url = config.get_service_on_off_url()
    json_data = {'device': device, 'state': state}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            f'There was a problem: {whoops} using url {url}, device {device} and state {state}')


def post_denva_measurement(json_data, which: str = 'one'):
    logger.debug(f'Posting measurements to denva {which.upper()}')
    url = config.get_post_denva_measurement_url(which)
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            f'There was a problem with sending measurement for denva with url {url} due to {whoops} ')


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
            f'There was a problem with adding entry with url {url} and entry {new_entry} due to {whoops} ')


def get_config():
    return get_data_for(f'{config.load_cfg()["urls"]["config"]}/config')


def send(service_name: str, data: dict):
    cfg = config.load_cfg()
    url = f'{cfg["urls"]["server"]}/denva'
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, data=json.dumps(data), timeout=2, headers=headers)
        if response.status_code == 200:
            logger.debug(f'data sent successfully for {service_name}')
        else:
            logger.warning(f'Unable to sent data. code:{response.status_code}')
    except Exception as exception:
        logger.error(f'Unable to sent data\n{exception}', exc_info=True)
