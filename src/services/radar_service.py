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
from gateways import local_data_gateway


def get_aircraft_detected_today_count():
    result = local_data_gateway.get_current_reading_for_aircraft()
    if 'error' in result:
        return 'Unknown'
    else:
        result["detected"] = get_count_difference_to_yesterday(int(result["detected"]))
        return result


def get_count_difference_to_yesterday(count: int) -> str:
    result = local_data_gateway.get_yesterday_report_for_aircraft()
    if 'error' in result:
        return ''
    else:
        diff = count - int(result["detected"])
        if diff > 0:
            return ' {}(+{}↑)'.format(count, diff)
        elif diff == 0:
            return ''
        else:
            return ' {}({}↓)'.format(count, diff)
