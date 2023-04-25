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

import sys
from icp10125 import ICP10125

device = ICP10125()

DEFAULT_QNH = 1013.25
QNH = 1018

if len(sys.argv) > 1:
    QNH = float(sys.argv[1])


def calculate_altitude(pressure, qnh=DEFAULT_QNH):
    return 44330.0 * (1.0 - pow(pressure / qnh, (1.0 / 5.255)))


def get_measurement() -> dict:
    pressure, temperature = device.measure()
    altitude = calculate_altitude(pressure / 100, qnh=QNH)

    return {
        "pressure": pressure/100,
        "temperature": temperature,
        "altitude": altitude
    }
