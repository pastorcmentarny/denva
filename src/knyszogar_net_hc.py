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
from common import status, data_files, loggy
from gateways import local_data_gateway
from services import networkcheck_service
from systemhc import system_health_check_service

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

PERFECT = 'PERFECT'
GOOD = 'GOOD'
POOR = 'POOR'
DOWN = 'DOWN'

logger = logging.getLogger('hc')
dom_utils.setup_test_logging('healthcheck')
HOSTNAME = config.SERVER_IP
HEADERS = {
    "User-Agent": USER_AGENT}


def check_pages(headers, ok, pages, problems):
    for page in pages:
        logger.info('checking connection to :{}'.format(page))

        try:
            with requests.get(page, headers=headers, timeout=5) as response:
                if response.status_code == 200:
                    ok += 1
                else:
                    response.raise_for_status()

        except Exception as whoops:
            logger.warning('Response error: {}'.format(whoops))
            problems.append(str(whoops))

    return ok


def post_healthcheck_beat(device: str, app_type: str):
    url = f'{HOSTNAME}:5000/shc/update'
    json_data = {'device': device, 'app_type': app_type}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem: {} using url {}, device {} and app_type {}'.format(whoops, url, device, app_type))


def check_for(app_name: str, headers, page: str, app_type: str = ""):
    logger.info('checking connection to :{}'.format(page))
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
        logger.warning('Response error: {}'.format(whoops))


def check_denva_app_status(cfg):
    state = status.Status()
    logger.info('Getting status for denva..')
    server_data = local_data_gateway.get_data_for('{}/system'.format(config.load_cfg()["urls"]['denva']))
    if 'error' in server_data:
        logger.warning('Unable to get Denva status due to {}'.format(server_data['error']))
        state.set_error()
    else:
        if float(dom_utils.get_float_number_from_text(server_data['CPU Temp'])) > cfg[config.FIELD_SYSTEM]['cpu_temp_error']:
            logger.warning('status: RED due to very high cpu temp on Denva )')
            state.set_danger()
        elif float(dom_utils.get_float_number_from_text(server_data['CPU Temp'])) > cfg[config.FIELD_SYSTEM]['cpu_temp_warn']:
            logger.warning('status: ORANGE due to high cpu temp on Denva )')
            state.set_warn()
        if dom_utils.get_int_number_from_text(server_data['Memory Available']) < 384:
            logger.warning('status: RED due to very low memory available on Denva')
            state.set_danger()
        elif dom_utils.get_int_number_from_text(server_data['Memory Available']) < 512:
            logger.warning('status: ORANGE due to low memory available on Denva')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Free Space']) < 256:
            logger.warning('status: RED due to very low free space on Denva')
            state.set_danger()
        elif dom_utils.get_int_number_from_text(server_data['Free Space']) < 1024:
            logger.warning('status: ORANGE due to low free space on Denva')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Data Free Space']) < 256:
            logger.warning('status: RED due to very low data free space on Denva')
            state.set_danger()
        elif dom_utils.get_int_number_from_text(server_data['Data Free Space']) < 1024:
            logger.warning('status: ORANGE due to low data free space on Denva')
            state.set_warn()

    local_data_gateway.post_device_status('denva', state.get_status_as_light_colour())
    logger.info('Denva: {}'.format(state.get_status_as_light_colour()))


def check_enviro_app_status(cfg):
    state = status.Status()
    logger.info('Getting status for enviro..')
    state.set_warn()
    local_data_gateway.post_device_status('denviro', state.get_status_as_light_colour())
    # 2. DENVIRO
    state = status.Status()
    server_data = local_data_gateway.get_data_for('{}/system'.format(config.load_cfg()["urls"]['enviro']))
    if 'error' in server_data:
        logger.warning('Unable to get Denviro status due to {}'.format(server_data['error']))
        state.set_error()
    else:
        system_health_check_service.update_hc_for('denviro', 'ui')
        if float(dom_utils.get_float_number_from_text(server_data['CPU Temp'])) > cfg[config.FIELD_SYSTEM]['cpu_temp_error']:
            logger.warning('status: RED due to very high cpu temp on Denviro')
            state.set_error()
        elif float(dom_utils.get_float_number_from_text(server_data['CPU Temp'])) > cfg[config.FIELD_SYSTEM]['cpu_temp_warn']:
            logger.warning('status: ORANGE due to high cpu temp on Denviro')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Memory Available']) < 384:
            logger.warning('status: RED due to very low memory available on Denviro')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Memory Available']) < 512:
            logger.warning('status: ORANGE due to low memory available on Denviro')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Free Space']) < 256:
            logger.warning('status: RED due to very low free space on Denviro')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Free Space']) < 1024:
            logger.warning('status: ORANGE due to low free space on Denviro')
            state.set_warn()

        if dom_utils.get_int_number_from_text(server_data['Data Free Space']) < 256:
            logger.warning('status: RED due to very low data free space on Denviro')
            state.set_error()
        elif dom_utils.get_int_number_from_text(server_data['Data Free Space']) < 1024:
            logger.warning('status: ORANGE due to low data free space on Denviro')
            state.set_warn()
    local_data_gateway.post_device_status('denviro', state.get_status_as_light_colour())
    logger.info('Denviro: {}'.format(state.get_status_as_light_colour()))


def my_services_check():
    logger.debug('Checking my services...')

    headers = requests.utils.default_headers()
    headers['User-Agent'] = USER_AGENT

    start_time = time.perf_counter()
    check_for('denva', headers, "http://192.168.0.201:5000/hc")
    check_for('radar', headers, "http://192.168.0.201:5000/hc/ar")
    check_for('denviro', headers, "http://192.168.0.202:5000/hc")
    check_for('trases', headers, "http://192.168.0.224:5000/hc")
    check_for('server', headers, "%s:5000/hc" % config.SERVER_IP)
    check_for('email', headers, "%s:18010/hc" % config.SERVER_IP, 'knyszogar')
    end_time = time.perf_counter()
    total_time = '{:0.2f}'.format((end_time - start_time))
    logger.info(f'It took {total_time} second to test.')


def network_check() -> dict:
    logger.debug('Checking network...')
    ok = 0
    problems = []

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

    ok = check_pages(headers, ok, pages, problems)
    network_status = _get_network_status(ok)

    end_time = timer()
    total_time = end_time - start_time
    networkcheck_service.log_result(problems, network_status, total_time)
    result = "{} of {} pages were loaded successfully.".format(ok, len(pages))

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
                check_denva_app_status(config.load_cfg())
                check_enviro_app_status(config.load_cfg())

            if loop_counter >= 10:
                logger.info("Performing network check")
                result = network_check()
                data_files.save_dict_data_as_json("data/nhc.json", result)
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
        local_data_gateway.post_device_on_off('hc', True)
        app_loop()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        sys.exit(0)
        # TODO post status to OFF
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        # TODO add send email: email_sender_service.send_error_log_email(APP_NAME,'{} crashes due to {}'.format(APP_NAME, exception))
        # TODO post status to ERROR
    except BaseException as disaster:
        logger.error('Something went badly wrong\n{}'.format(disaster), exc_info=True)
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
        # TODO add send email: email_sender_service.send_error_log_email(APP_NAME,'{} crashes due to {}'.format(APP_NAME, exception))
        # TODO post status to ERROR
    local_data_gateway.post_device_on_off('hc', False)
