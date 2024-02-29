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
import logging
from timeit import default_timer as timer

import requests

from gateways import web_data_gateway

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

# TODO MOVE TO config
PERFECT = 'Perfect'
GOOD = 'Good'
POOR = 'POOR'
ERROR = 'DOWN'

logger = logging.getLogger('hc')


def network_check(in_china: bool = False) -> dict:
    logger.debug('Checking network...')
    ok = 0
    problems = []

    if in_china:
        problems.append(f"In China mode: {in_china}")
        pages = [
            "https://dominiksymonowicz.com",
            'https://cn.bing.com/',
            'https://baidu.com',
            'https://amazon.cn',
            'https://www.cloudflare.com/zh-cn/',
            'https://www.sina.com.cn.'
        ]
    else:
        pages = [
            "https://dominiksymonowicz.com",
            'https://bing.com/',
            'https://baidu.com',
            'https://amazon.com',
            'https://wikipedia.org',
            'https://google.com/',
        ]
    headers = requests.utils.default_headers()
    headers['User-Agent'] = USER_AGENT

    start_time = timer()

    ok = web_data_gateway.check_pages(headers, ok, pages, problems)
    status = _get_network_status(ok)

    end_time = timer()
    total_time = int(end_time - start_time) * 1000
    log_result(problems, status, total_time)
    result = f"{ok} of {len(pages)} pages were loaded"

    logger.info(status)
    logger.info(result)
    if len(problems) > 0:
        logger.warning(problems)

    return {
        'status': status,
        'result': result,
        'problems': problems
    }


def log_result(problems, status, total_time):
    if status == POOR:
        logger.warning(
            f'It looks like there is some problem with network as some pages failed to load due to: {problems}')
    if status == ERROR:
        logger.error(f'Network is DOWN! All services failed due to: {problems}')
    if status == PERFECT or status == GOOD:
        logger.debug(f'Network seems to be fine. I took {total_time} ms to check.')


def _get_network_status(ok: int) -> str:
    if ok == 6:
        return PERFECT
    elif ok >= 4:
        return GOOD
    elif ok >= 2:
        return POOR
    elif ok == 1:
        return ERROR + '?'
    else:
        return ERROR + '!'


# use as standalone tool :)
if __name__ == '__main__':
    network_check()
