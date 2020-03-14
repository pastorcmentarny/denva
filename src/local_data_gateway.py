import json

import requests

import config_serivce


def get_current_reading_for_denva() -> dict:
    return get_data_for('{}/now'.format(config_serivce.load_cfg()["urls"]['denva']))


def get_current_reading_for_enviro() -> dict:
    return get_data_for('{}/now'.format(config_serivce.load_cfg()["urls"]['enviro']))


def get_current_logs_for_all_services() -> dict:
    return {
        'app': {
            'denva': get_data_for('{}/log/app/recent'.format(config_serivce.load_cfg()["urls"]['denva'])),
            'enviro': get_data_for('{}/log/app/recent'.format(config_serivce.load_cfg()["urls"]['enviro']))
        },
        'hc': {
            'denva': get_data_for('{}/log/hc/recent'.format(config_serivce.load_cfg()["urls"]['denva'])),
            'enviro': get_data_for('{}/log/hc/recent'.format(config_serivce.load_cfg()["urls"]['enviro']))
        }
    }


def get_data_for(url: str) -> dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return json.loads(response.text)
    except Exception as whoops:
        return {'error': 'There was a problem: {}'.format(whoops)}


def get_current_warnings_for_all_services() -> dict:
    return {
        'denva': get_data_for(config_serivce.get_current_warnings_url_for('denva')),
        'enviro': get_data_for(config_serivce.get_current_warnings_url_for('enviro'))
    }


if __name__ == '__main__':
    print(get_current_reading_for_denva())
