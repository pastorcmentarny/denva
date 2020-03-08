import json
import requests
import config_serivce

def get_current_reading_for_denva() -> dict:
    return get_data_for('http://192.168.0.2:5000/now')


def get_current_reading_for_enviro() -> dict:
    return get_data_for('http://192.168.0.4:5000/now')


def get_data_for(url: str) -> dict:
    response = requests.get(url)
    try:
        response.raise_for_status()
        return json.loads(response.text)
    except Exception as whoops:
        return {'error' : 'There was a problem: {}'.format(whoops) }


def get_current_warnings_for_all_services() -> dict:
    return {
        'denva' : get_data_for(config_serivce.get_current_warnings_url_for('denva')),
        'enviro' : get_data_for(config_serivce.get_current_warnings_url_for('enviro'))
    }

if __name__ == '__main__':
    print(get_current_reading_for_denva())