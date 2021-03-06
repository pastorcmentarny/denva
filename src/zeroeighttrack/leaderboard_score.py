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

from common import gobshite_exception

NORMAL_DISTANCE = 260
MAX_SCORE = 26888


def calculate_score(time: int, distance: int, lap: int) -> int:
    score = MAX_SCORE - time
    if lap > 1:
        score = int(score + (score / 200) * (lap - 1))
    if distance == 0:
        return score - 450  # move to config?

    if 261 >= distance >= 259:
        return score

    if distance < 259:
        return score - ((NORMAL_DISTANCE - distance) * (NORMAL_DISTANCE - distance)) - int(
            (NORMAL_DISTANCE - distance) * (time / NORMAL_DISTANCE))

    if distance > 261:
        return score + (distance - NORMAL_DISTANCE)

    raise gobshite_exception.GobshiteException
