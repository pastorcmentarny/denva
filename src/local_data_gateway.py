import json
import requests


def get_data_for(url: str) -> dict:
    response = requests.get(url)
    try:
        response.raise_for_status()
        return json.loads(response.text)
    except Exception as whoops:
        return {'error' : 'There was a problem: {}'.format(whoops) }


def get_current_warnings_for_all_services() -> dict:
    #TODO REMOVE IT MOCK
    return {
         'denva' : ['Temperature is low'],
        'enviro' : ['PM 2.5 is high','PM 10 is high']
    }
''' replace with:
return {
    'denva' : get_data_for(config_serivce.get_current_warnings_url__for('denva')),
    'enviro' : get_data_for(config_serivce.get_current_warnings_url__for('enviro'))
}
'''
