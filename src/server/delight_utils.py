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
import random


def get_state_colour(current_state):
    if current_state.get_status_as_light_colour() == 'RED':
        color_red = 255
        color_green = 0
        color_blue = 0
    elif current_state.get_status_as_light_colour() == 'ORANGE':
        color_red = 255
        color_green = 110
        color_blue = 0
    elif current_state == 'REBOOT':
        color_red = 255
        color_green = 229
        color_blue = 124
    elif current_state == 'OFF':
        color_red = 0
        color_green = 0
        color_blue = 127
    else:
        color_red = 0
        color_green = 255
        color_blue = 0
    return color_red, color_green, color_blue


def get_state_colour_for_hc(current_state: str):
    if current_state == 'UNKNOWN':
        color_red = 64
        color_green = 64
        color_blue = 64
    elif current_state == 'DOWN':
        color_red = 255
        color_green = 0
        color_blue = 0
    elif current_state == 'WARN':
        color_red = 255
        color_green = 110
        color_blue = 0
    elif current_state == 'REBOOT':
        color_red = 255
        color_green = 229
        color_blue = 124
    elif current_state == 'OFF':
        color_red = 0
        color_green = 0
        color_blue = 127
    else:
        color_red = 0
        color_green = 255
        color_blue = 0
    return color_red, color_green, color_blue


def get_random_pixel_location_at_night(x: int):
    return x + random.randint(0, 2)
