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
from gateways import web_data_gateway
from services import weather_service
import logging
logger = logging.getLogger('app')

information = {
    "crimes": "unknown",
    "floods": "unknown",
    "weather": ["unknown"],
    "o2": "unknown"
}


def get_data_about_rickmansworth() -> dict:
    logger.debug('Getting crime,floods,weather and o2 issues data about Rickmansworth')
    information['crimes'] = web_data_gateway.get_crime()
    information['floods'] = web_data_gateway.get_flood()
    information['weather'] = weather_service.get_weather()
    information['o2'] = web_data_gateway.get_o2_status()
    logger.info('Got all data about Rickmansworth.')
    return information
