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
import time
from datetime import datetime

import dom_utils

import config
import server.celebrations as celebrations
import server.chinese_dictionary_service as cn
import server.good_english_sentence as eng
import server.good_method_name as method
import server.information_service as information
import server.personal_stats as personal_events
import server.random_irregular_verb as verb
import server.rules_service as rules
from common import data_files, commands
from gateways import web_data_gateway, local_data_gateway, tube_client
from reports import report_generator
from server import daily
from services import error_detector_service, radar_service, metrics_service
from services import weather_service, system_data_service
from systemhc import system_health_check_service

logger = logging.getLogger('app')
server_logger = logging.getLogger('server')


def get_now_and_next_event():
    events = daily.get_now_and_next_event(datetime.now().hour * 60 + datetime.now().minute)
    celebration = celebrations.get_next_3_events()
    return {
        'now': events[0],
        'next': events[1],
        'celebration': celebration[0],
        'celebration2': celebration[1]
    }


def get_last_updated_page() -> str:
    now = datetime.now()
    return "{}.{}'{} - {}:{}".format(now.day, now.month, now.year, now.hour, now.minute)


def get_gateway_data() -> dict:
    weather_response = weather_service.get_weather()
    weather_response = weather_response[:len(weather_response)]
    return {'chinese': cn.get_random_chinese_word(),
            'english': eng.get_random_english_sentence(),
            'verb': verb.get_random_irregular_verb(),
            'method': method.get_random_method_name(),
            'calendar': celebrations.get_next_3_events(),
            'today': get_last_updated_page(),
            'events': personal_events.get_personal_stats(),
            'weather': weather_response,
            'information': information.get_information(),
            'daily': daily.get_now_and_next_event(datetime.now().hour * 60 + datetime.now().minute),
            'rule': rules.get_random_rule()
            }


def get_fasting_warning() -> str:
    hour = datetime.now().hour
    if hour >= 19 or hour < 12:
        return "NO FOOD (INTERMITTENT FASTING PERIOD)"
    elif hour == 12:
        return "NO FOOD (OPTIONAL)"
    return ''


def get_all_warnings_page() -> list:
    start = time.perf_counter()
    data = []

    tube = web_data_gateway.get_tube(False)
    if tube == ["Tube data N/A"]:
        data.append("Tube data N/A")
    elif tube != 'Good Service' or tube != 'Service Closed':
        data.append(tube)

    train = web_data_gateway.get_train()
    if train == 'Train data N/A':
        data.append('Train data N/A')
    elif train != "Good service":
        data.append(train)

    data.append(get_fasting_warning())

    data = dom_utils.clean_list_from_nones(data)

    end = time.perf_counter()
    logger.info('Execution time: {} ns.'.format((end - start)))  # TODO move to stats

    return data


def get_current_system_information_for_all_services(config: dict):
    return {
        'server': local_data_gateway.get_data_for('{}/system'.format(config["urls"]['delight'])),
        'denva': local_data_gateway.get_data_for('{}/system'.format(config["urls"]['denva'])),
        'denva2': local_data_gateway.get_data_for('{}/system'.format(config["urls"]['denva2'])),
    }


def get_links_for_gateway(config_data: dict, sensor_only: bool = False) -> dict:
    return {
        'logApp': get_links_for(config_data, 'log/app', sensor_only),
        'logHc': get_links_for(config_data, 'log/hc', sensor_only),
        'logUi': get_links_for(config_data, 'log/ui', sensor_only),
        'averages': get_links_for(config_data, 'avg', True),
        'records': get_links_for(config_data, 'records', True),
        'stats': get_links_for(config_data, 'stats', True),
        'warningsAll': get_links_for(config_data, 'warns', True),
        'warningsCounter': get_links_for(config_data, 'warns/count', True),
    }


def get_links_for(config: dict, suffix: str, sensor_only: bool = False) -> dict:
    urls = config['urls']
    result = {
        'denva': '{}/{}'.format(urls['denva'], suffix)
    }
    if not sensor_only:
        result['server'] = '{}/{}'.format(urls['server'], suffix)

    return result


def get_last_logs_for(log_file_name: str, lines):
    today = datetime.now()
    name = f'{log_file_name}-{today.year}-{today.month:02d}-{today.day:02d}.txt'
    return data_files.tail('/home/ds/knyszogardata/logs/' + name, lines)


def run_gc() -> dict:
    return system_data_service.run_gc()


def get_errors_from_data(data):
    return error_detector_service.get_errors_from_data(data)


def get_data_for_page(config_data, page_ricky: str, page_tt_delays_counter: str,page_tube_trains: str):
    logger.info('Getting data for main page')
    try:
        data = {
            'page_tube_trains': page_tube_trains,
            'page_tt_delays_counter': page_tt_delays_counter,
            'page_ricky': page_ricky,
            'warnings': local_data_gateway.get_current_warnings_for_all_services(),
            'denva': data_files.load_json_data_as_dict_from('/home/pi/data/denva_data.json'),
            'denva2': data_files.load_json_data_as_dict_from('/home/pi/data/denva_two_data.json'),
            'aircraft': radar_service.get_aircraft_detected_today_count(),
            config.FIELD_SYSTEM: get_current_system_information_for_all_services(config_data),
            'links': get_links_for_gateway(config_data),
            'welcome_text': data_files.load_text_to_display(config_data["paths"]["text"]),
            'transport': web_data_gateway.get_status()
        }
        data['errors'] = get_errors_from_data(data)
    except Exception as exception:
        logger.error(f'Unable to get data due to {exception}', exc_info=True)
        data = {
            'page_tube_trains': page_tube_trains,
            'page_tt_delays_counter': page_tt_delays_counter,
            'page_ricky': page_ricky,
            'warnings': {},
            'denva': {},
            'denva2': {},
            'aircraft': {},
            config.FIELD_SYSTEM: {},
            'links': get_links_for_gateway(config_data),
            'welcome_text': f"Unable to load message due to ${exception}"
        }
    return data



def get_device_status(config_data: dict):
    logger.info('Getting data for main page')
    try:
        data = {
            'warnings': local_data_gateway.get_current_warnings_for_all_services(),
            'denva': local_data_gateway.get_current_reading_for_denva(),
            'denva2': local_data_gateway.get_current_reading_for_denva_two(),
            'aircraft': radar_service.get_aircraft_detected_today_count(),
            config.FIELD_SYSTEM: get_current_system_information_for_all_services(config_data),
            'links': get_links_for_gateway(config_data),
            'welcome_text': data_files.load_text_to_display(config_data),
            'transport': web_data_gateway.get_status(),
            'metrics': metrics_service.get_currents_metrics(),
            'log_count': local_data_gateway.get_current_log_counts(),

        }
        data['errors'] = get_errors_from_data(data)
    except Exception as exception:
        logger.error('Unable to get data due to {}'.format(exception))
        data = {
            'warnings': {},
            'denva': {},
            'denva2': {},
            'aircraft': {},
            config.FIELD_SYSTEM: {},
            'links': get_links_for_gateway(config_data),
            'welcome_text': f"Unable to load message due to ${exception}",
            'transport': [],
            'metrics': {},
            'log_count': {}
        }
    return data


def count_tube_problems_today():
    return tube_client.count_tube_problems(tube_client.load())


def get_report_for_yesterday():
    return report_generator.generate()


def get_system_hc():
    return system_health_check_service.get_system_healthcheck()

def get_ping_test_results():
    return commands.get_ping_results()
