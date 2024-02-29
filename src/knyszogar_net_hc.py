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
import sys
import time
import traceback
from timeit import default_timer as timer

import requests

import config
import dom_utils
from common import loggy, data_writer
from gateways import local_data_gateway

from services import networkcheck_service

CPU_TEMP = 'CPU Temp'

MEMORY_AVAILABLE = 'Memory Available'

FREE_SPACE = 'Free Space'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

PERFECT = 'PERFECT'
GOOD = 'GOOD'
POOR = 'POOR'
DOWN = 'OFF'

logger = logging.getLogger('hc')
dom_utils.setup_test_logging('healthcheck')
HOSTNAME = config.SERVER_IP
HEADERS = {
    "User-Agent": USER_AGENT}


def check_pages(headers, ok, pages, problems):
    for page in pages:
        logger.info(f'checking connection to :{page}')

        try:
            with requests.get(page, headers=headers, timeout=5) as response:
                if response.status_code == 200:
                    ok += 1
                else:
                    response.raise_for_status()

        except Exception as whoops:
            logger.warning(f'Response error: {whoops}')
            problems.append(str(whoops))

    return ok


def post_healthcheck_beat(device: str, app_type: str):
    local_data_gateway.post_healthcheck_beat(device,app_type)

def check_for(app_name: str, headers, page: str, app_type: str = ""):
    logger.info(f'checking connection to :{page}')
    try:
        with requests.get(page, headers=headers, timeout=5) as response:
            if response.status_code == 200:
                if app_type == "":
                    post_healthcheck_beat(app_name, 'ui')
                else:
                    post_healthcheck_beat(app_type, app_name)
            else:
                response.raise_for_status()
    except Exception as whoops:
        logger.warning(f'Response error: {whoops}')


def my_services_check():
    logger.debug('Checking my services...')

    headers = requests.utils.default_headers()
    headers['User-Agent'] = USER_AGENT

    start_time = time.perf_counter()
    check_for('denva', headers, f"{config.DENVA_IP}:5000/hc")
    check_for('denva2', headers, f"{config.DENVA_TWO_IP}:5000/hc")
    check_for('radar', headers, f"{config.DENVA_IP}:5000/hc/ar")
    check_for('server', headers, f"{config.SERVER_IP}:5000/hc")
    check_for('config', headers, f"{config.SERVER_IP}:18004/hc", 'knyszogar')
    check_for('email', headers, f"{config.SERVER_IP}:18010/hc", 'knyszogar')
    end_time = time.perf_counter()
    total_time = f'{(end_time - start_time):0.2f}'
    logger.info(f'It took {total_time} second to test.')


def network_check() -> dict:
    logger.debug('Checking network...')
    ok = 0
    problems = []

    pages = config.get_ping_pages().copy()

    headers = requests.utils.default_headers()
    headers['User-Agent'] = USER_AGENT

    start_time = timer()

    ok = check_pages(headers, ok, pages, problems)
    network_status = _get_network_status(ok)

    end_time = timer()
    total_time = end_time - start_time
    networkcheck_service.log_result(problems, network_status, total_time)
    result = f"{ok} of {len(pages)} pages were loaded successfully."

    logger.info(f'Status:{network_status}. {result}')
    problems_count = len(problems)
    if problems_count > 0:
        if problems_count == 1:
            logger.warning(f'There was {problems_count} found. {problems}')
        else:
            logger.warning(f'There were {problems_count} problems. Problems: {problems}')

    return {
        'status': network_status,
        'result': result,
        'problems': problems
    }


def _get_network_status(ok: int) -> str:
    if ok == 6:
        return PERFECT
    elif ok >= 4:
        return GOOD
    elif ok >= 2:
        return POOR
    elif ok == 1:
        return DOWN + '?'
    else:
        return DOWN + '!'


def app_loop():
    loop_counter = 10
    while True:
        try:
            logger.debug(f'loop no. {loop_counter}')
            if loop_counter % 2 == 0:
                logger.info("Performing healthcheck for my services")
                my_services_check()
                # TODO ADD DENVA ONE APP check
                # TODO ADD DENVA TWO APP check

            if loop_counter >= 10:
                logger.info("Performing network check")
                result = network_check()
                data_writer.save_dict_data_as_json("data/nhc.json", result)
                loop_counter = 0
            loop_counter += 1

            # send info to knyszogar that am up and running
            dom_utils.post_healthcheck_beat('knyszogar', 'hc')
        except BaseException as base_exception:
            logger.error(f'There is a problem with healthcheck: {base_exception}', exc_info=True)

        # wait until next check
        time.sleep(30)


if __name__ == '__main__':

    loggy.log_with_print('Starting application')

    try:
        app_loop()
    except KeyboardInterrupt as keyboard_exception:
        print(f'Received request application to shut down.. goodbye. {keyboard_exception}')
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        sys.exit(0)
    except Exception as exception:
        logger.error(f'Something went badly wrong\n{exception}', exc_info=True)
    except BaseException as disaster:
        logger.error(f'Something went badly wrong\n{disaster}', exc_info=True)
        msg = f'Shit hit the fan and application died badly because {disaster}'
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
