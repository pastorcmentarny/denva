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

import config

words = []


def load_dictionary_file() -> list:
    file_path = config_service.get_irregular_verbs_path()
    file = open(file_path, 'r', encoding="UTF-8", newline='')
    content = file.readlines()
    for line in content:
        definition = line.split(";;")
        word = {'Base': definition[0],
                'PastSimple': definition[1],
                'PastParticiple': definition[2],
                # TODO add polish translation when i do it
                # TODO add sentence example
                }
        words.append(word)
    return words


def get_random_irregular_verb() -> dict:
    load_dictionary_file()
    return words[random.randint(0, len(words) - 1)]
