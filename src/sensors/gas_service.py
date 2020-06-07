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

from enviroplus import gas


def get_oxidising():
    data = gas.read_all()
    return data.oxidising / 1000


def get_reducing():
    data = gas.read_all()
    return data.reducing / 1000


def get_nh3():
    data = gas.read_all()
    return data.nh3 / 1000
