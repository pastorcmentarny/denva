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
import web_data

information = {
    "crimes": "unknown",
    "floods": "unknown",
    "weather": ["unknown"],
    "o2": "unknown"
}


def get_data_about_rickmansworth() -> dict:
    information['crimes'] = web_data.get_crime()
    information['floods'] = web_data.get_flood()
    information['weather'] = web_data.get_weather()
    information['o2'] = web_data.get_o2_status()
    return information
