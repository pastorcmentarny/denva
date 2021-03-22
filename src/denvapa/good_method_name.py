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

import random

names = [
    'getLogsAsSourceRecords()',
    'findElement()',
    'clickElement()',
    'waitUntilVisible()',
    'establishConnectionToLeader(List<InetAddressAndPort> servers)',
    'if (isLookingForLeader(response)) '
]


def get_random_method_name() -> str:
    return names[random.randint(0, len(names) - 1)]
