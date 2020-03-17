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
import gc
import os
import psutil
import time

import mothership.celebrations as celebrations
import mothership.information_service as information
import mothership.chinese_dictionary_service as cn
import mothership.good_english_sentence as eng
import mothership.good_method_name as method
import mothership.random_irregular_verb as verb
import mothership.personal_stats as personal_events
import data_files
import utils
import web_data


def get_last_updated_page() -> str:
    now = datetime.datetime.now()
    return "{}.{}'{} - {}:{}".format(now.day,now.month,now.year,now.hour,now.minute)


def get_gateway_data() -> dict:
    return {'chinese' : cn.get_random_chinese_word(),
            'english' : eng.get_random_english_sentence(),
            'verb' : verb.get_random_irregular_verb(),
            'method' : method.get_random_method_name(),
            'calendar' : celebrations.get_next_3_events(),
            'today' : get_last_updated_page(),
            'events' : personal_events.get_personal_stats(),
            'weather' : web_data.get_weather(),
            'information': information.get_information()
            }


def get_fasting_warning() -> str:
    hour = datetime.datetime.now().hour
    if hour >= 19 or hour <= 11:
        return "NO FOOD (INTERMITTENT FASTING PERIOD)"
    elif hour == 10:
        return "NO FOOD (OPTIONAL)"
    return None


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

#prototype if works i need systemutils
def clean():
    print(psutil.Process(os.getpid()).memory_info())
    gc.collect()
    print(psutil.Process(os.getpid()).memory_info())


#USED for test only
if __name__ == '__main__':
    print(get_all_warnings_page())
    clean()
