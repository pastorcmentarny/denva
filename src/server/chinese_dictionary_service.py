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

import random

import requests

import config
from common import data_loader

words = []


def load_dictionary_file() -> list:
    content = data_loader.load_as_list_from_file(config.get_path_to_chinese_dictionary())
    for line in content:
        definition = line.split(config.FILE_SPLITTER)
        definition = definition[2:len(definition) - 2]
        word = {'character': definition[0],
                'pinyin': definition[1],
                'english': definition[3],
                'polish': definition[4]
                }
        words.append(word)
    return words


def get_random_chinese_word() -> dict:
    load_dictionary_file()
    return words[random.randint(0, len(words) - 1)]


'''
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1_2)
'''


# it works only for bigger files by design
def get_chinese_dictionary_from_github() -> list:
    path = "https://raw.githubusercontent.com/pastorcmentarny/DomLearnsChinese/master/res/raw/dictionary.txt"
    #    path = 'https://github.com/pastorcmentarny/DomLearnsChinese/raw/master/res/raw/dictionary.txt'

    #    s = requests.Session()
    #    s.mount('https://', MyAdapter())
    #    print(s.get(path))

    headers = requests.utils.default_headers()
    headers[
        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    response = requests.get(path, headers=headers)

    try:
        response.raise_for_status()
        return response.text.splitlines()
    except Exception as whoops:
        return [f'Error: {whoops}']
