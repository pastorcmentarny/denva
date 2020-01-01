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
import requests
import logging

import config_serivce
logger = logging.getLogger('app')


def get_url_for(name:str):
    cfg = config_serivce.load_cfg()
    if name == 'enviro':
        return '{}/enviro'.format(cfg['urls']['server'])
    elif name == 'denva':
        return '{}/denva'.format(cfg['urls']['server'])
    else:
        logging.error('unknown name: {}'.format(name))


def send(service_name:str,data:dict):
    url = get_url_for(service_name)
    response = requests.post(url, data=data)
    if response.status_code == '200':
        logger.info('data sent successfully for {}'.format(service_name))
    else:
        logger.warning('unable to sent data. code:{}'.format(response.status_code))