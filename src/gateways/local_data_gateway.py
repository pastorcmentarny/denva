import json

import requests

import config_service
from services import system_data_service

ONE_MINUTE_TIMEOUT = 60


def get_current_reading_for_denva() -> dict:
    return get_data_for('{}/now'.format(config_service.load_cfg()["urls"]['denva']))


def get_current_reading_for_enviro() -> dict:
    return get_data_for('{}/now'.format(config_service.load_cfg()["urls"]['enviro']))


def get_yesterday_report_for_denva() -> dict:
    return get_data_for('{}/report/yesterday'.format(config_service.load_cfg()["urls"]['denva']), ONE_MINUTE_TIMEOUT)


def get_yesterday_report_for_enviro() -> dict:
    return get_data_for('{}/report/yesterday'.format(config_service.load_cfg()["urls"]['enviro']), ONE_MINUTE_TIMEOUT)


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


def get_data_for(url: str, timeout: int = 3) -> dict:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return json.loads(response.text)
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
