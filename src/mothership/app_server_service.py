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

import datetime
import os

import gc
import psutil
import time

import config_service
import data_files
from services import error_detector_service
from zeroeighttrack import leaderboard
import local_data_gateway
import mothership.celebrations as celebrations
import mothership.chinese_dictionary_service as cn
from mothership import daily
import mothership.good_english_sentence as eng
import mothership.good_method_name as method
import mothership.information_service as information
import mothership.personal_stats as personal_events
import mothership.random_irregular_verb as verb
import utils
from services import weather_service, system_data_service
import web_data
import pprint


def get_last_updated_page() -> str:
    now = datetime.datetime.now()
    return "{}.{}'{} - {}:{}".format(now.day, now.month, now.year, now.hour, now.minute)


def get_gateway_data() -> dict:
    return {'chinese': cn.get_random_chinese_word(),
            'english': eng.get_random_english_sentence(),
            'verb': verb.get_random_irregular_verb(),
            'method': method.get_random_method_name(),
            'calendar': celebrations.get_next_3_events(),
            'today': get_last_updated_page(),
            'events': personal_events.get_personal_stats(),
            'weather': weather_service.get_weather(),
            'information': information.get_information(),
            'daily': daily.get_now_and_next_event(datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
            }


def get_fasting_warning() -> str:
    hour = datetime.datetime.now().hour
    if hour >= 19 or hour <= 11:
        return "NO FOOD (INTERMITTENT FASTING PERIOD)"
    elif hour == 10:
        return "NO FOOD (OPTIONAL)"
    return ''


def get_all_warnings_page() -> list:
    start = time.time_ns()
    data = []

    tube = web_data.get_tube(False)
    if tube == ["Tube data N/A"]:
        data.append("Tube data N/A")
    elif tube != 'Good Service' or tube != 'Service Closed':
        data.append(tube)

    train = web_data.get_train()
    if train == 'Train data N/A':
        data.append('Train data N/A')
    elif train != "Good service":
        data.append(train)

    data.append(get_fasting_warning())

    data = utils.clean_list_from_nones(data)

    end = time.time_ns()
    print('Execution time: {} ns.'.format((end - start)))

    return data


def get_random_frame() -> str:
    return data_files.get_random_frame_picture_path()


# prototype if works i need systemutils
def clean():
    print(psutil.Process(os.getpid()).memory_info())
    gc.collect()
    print(psutil.Process(os.getpid()).memory_info())


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
    return error_detector_service.get_errors(data)


def add_result(data: str) -> dict:
    result_id = leaderboard.add_result(data)
    return {
        'position': leaderboard.get_position_for_id(result_id),
        'result': leaderboard.get_result_by_id(result_id),
        'top10': leaderboard.get_top10()
    }


if __name__ == '__main__':
    pprint.PrettyPrinter(indent=4).pprint(get_links_for_gateway())


def get_top_10():
    return leaderboard.get_top10()


def get_all_results():
    return leaderboard.sort_leaderboard_by_time()


def get_top_10_score():
    return leaderboard.get_top10_by_score()