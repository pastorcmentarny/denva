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
from utils import dom_utils


def print_measurement(data, left_width=20, right_width=6):
    print_title(left_width, right_width)
    print_items(data, left_width, right_width)
    print('-' * 36 + '\n')


def print_items(data: dict, left_width, right_width):
    for title, value in data.items():
        print(title.ljust(left_width, '.') + str(value).rjust(right_width, ' '))


def print_title(left_width, right_width):
    title = 'Measurement @ {}'.format(dom_utils.get_timestamp_title())
    print(title.center(left_width + right_width, "-"))
