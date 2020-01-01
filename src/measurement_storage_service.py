import requests
import logging

import config_serivce
logger = logging.getLogger('app')


def get_url_for(name:str):
    cfg = config_serivce.load_cfg()
    if name == 'enviro':
        return '{}/enviro'.format(cfg['urls']['enviro'])
    elif name == 'denva':
        return '{}/denva'.format(cfg['urls']['denva'])
    else:
        logging.error('unknown name: {}'.format(name))


def send(service_name:str,data:dict):
    url = get_url_for(service_name)
    response = requests.post(url, data=data)
    if response.status_code == '200':
        logger.info('data sent successfully for {}'.format(service_name))
    else:
        logger.warning('unable to sent data. code:{}'.format(response.status_code))