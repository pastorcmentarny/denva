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

import config_serivce

logger = logging.getLogger('app')


def get_url_for(name: str):
    cfg = config_serivce.load_cfg()
    if name == 'enviro':
        return '{}/enviro'.format(cfg['urls']['server'])
    elif name == 'denva':
        return '{}/denva'.format(cfg['urls']['server'])
    else:
        logging.error('unknown name: {}'.format(name))


def send(service_name: str, data: dict):
    url = get_url_for(service_name)
    try:
        response = requests.post(url, data=json.dumps(data), timeout=2)
        if response.status_code == '200':
            logger.info('data sent successfully for {}'.format(service_name))
        else:
            logger.warning('Unable to sent data. code:{}'.format(response.status_code))
    except Exception as e:
        logger.error('Unable to sent data\n{}'.format(e), exc_info=True)
