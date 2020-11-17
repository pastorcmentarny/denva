# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

import logging
import time
from datetime import datetime

import config_service
import denvapa.celebrations as celebrations
import denvapa.chinese_dictionary_service as cn
import denvapa.good_english_sentence as eng
import denvapa.good_method_name as method
import denvapa.information_service as information
import denvapa.personal_stats as personal_events
import denvapa.random_irregular_verb as verb
import denvapa.rules_service as rules
from common import data_files, dom_utils
from denvapa import daily
from gateways import web_data_gateway, local_data_gateway
from services import error_detector_service, radar_service
from services import weather_service, system_data_service
from zeroeighttrack import leaderboard

logger = logging.getLogger('app')


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
    if hour >= 19 or hour <= 12:
        return "NO FOOD (INTERMITTENT FASTING PERIOD)"
    elif hour == 10:
        return "NO FOOD (OPTIONAL)"
    return ''


def get_all_warnings_page() -> list:
    start = time.time_ns()
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

    end = time.time_ns()
    logger.info('Execution time: {} ns.'.format((end - start)))  # TODO move to stats

    return data


def get_random_frame() -> str:
    return data_files.get_random_frame_picture_path()


def get_current_system_information_for_all_services():
    return {
        'server': system_data_service.get_system_information(),
        'denva': local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['denva'])),
        'enviro': local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['enviro'])),
        'delight': local_data_gateway.get_data_for('{}/system'.format(config_service.load_cfg()["urls"]['delight']))
    }


def get_links_for_gateway(sensor_only: bool = False) -> dict:
    return {
        'logApp': get_links_for('log/app', sensor_only),
        'logHc': get_links_for('log/hc', sensor_only),
        'logUi': get_links_for('log/ui', sensor_only),
        'averages': get_links_for('avg', True),
        'records': get_links_for('records', True),
        'stats': get_links_for('stats', True),
        'warningsAll': get_links_for('warns', True),
        'warningsCounter': get_links_for('warns/count', True),
    }


def get_links_for(suffix: str, sensor_only: bool = False) -> dict:
    urls = config_service.load_cfg()['urls']
    result = {
        'denva': '{}/{}'.format(urls['denva'], suffix),
        'enviro': '{}/{}'.format(urls['enviro'], suffix)
    }
    if not sensor_only:
        result['server'] = '{}/{}'.format(urls['server'], suffix)

    return result


# TODO improve it
def get_last_logs_for(log_file_name: str, lines):
    env = config_service.get_mode()
    if env == 'dev':
        env_dir = 'd:/denva/logs/'
    else:
        env_dir = 'e:/denva/logs/'
    return data_files.tail(env_dir + log_file_name, lines)


def run_gc() -> dict:
    return system_data_service.run_gc()


def get_errors_from_data(data):
    return error_detector_service.get_errors_from_data(data)


def add_result(data: str) -> dict:
    result_id = leaderboard.add_result(data)
    return {
        'position': leaderboard.get_position_for_id(result_id),
        'result': leaderboard.get_result_by_id(result_id),
        'top10': leaderboard.get_top10()
    }


def get_top_10():
    return leaderboard.get_top10()


def get_all_results():
    return leaderboard.sort_leaderboard_by_time()


def get_top_10_score():
    return leaderboard.get_top10_by_score()


def get_data_for_page(page_frame, page_gateway, page_recent_log_app, page_ricky, page_tt_delays_counter,
                      page_tube_trains, page_webcam):
    logger.info('Getting data for main page')
    try:
        data = {
            'page_tube_trains': page_tube_trains,
            'page_tt_delays_counter': page_tt_delays_counter,
            'page_recent_log_app': page_recent_log_app,
            'page_frame': page_frame,
            'page_webcam': page_webcam,
            'page_ricky': page_ricky,
            'page_gateway': page_gateway,
            'warnings': local_data_gateway.get_current_warnings_for_all_services(),
            'denva': local_data_gateway.get_current_reading_for_denva(),
            'enviro': local_data_gateway.get_current_reading_for_enviro(),
            'aircraft': radar_service.get_aircraft_detected_today_count(),
            'system': get_current_system_information_for_all_services(),
            'links': get_links_for_gateway(),
        }
        data['errors'] = get_errors_from_data(data)
    except Exception as e:
        logger.error('Unable to get data due to {}'.format(e))
        data = {
            'page_tube_trains': page_tube_trains,
            'page_tt_delays_counter': page_tt_delays_counter,
            'page_recent_log_app': page_recent_log_app,
            'page_frame': page_frame,
            'page_webcam': page_webcam,
            'page_ricky': page_ricky,
            'page_gateway': page_gateway,
            'warnings': {},
            'denva': {},
            'enviro': {},
            'aircraft': {},
            'system': {},
            'links': get_links_for_gateway()
        }
    return data


def stop_all_devices():
    local_data_gateway.get_data_for('{}/halt'.format(config_service.load_cfg()["urls"]['denva']))
    local_data_gateway.get_data_for('{}/halt'.format(config_service.load_cfg()["urls"]['enviro']))
    local_data_gateway.get_data_for('{}/halt'.format(config_service.load_cfg()["urls"]['delight']))
    return {'result': 'All devices stopped'}


def reboot_all_devices():
    local_data_gateway.get_data_for('{}/reboot'.format(config_service.load_cfg()["urls"]['denva']))
    local_data_gateway.get_data_for('{}/reboot'.format(config_service.load_cfg()["urls"]['enviro']))
    local_data_gateway.get_data_for('{}/reboot'.format(config_service.load_cfg()["urls"]['delight']))
    return {'result': 'All devices starting to reboot'}
