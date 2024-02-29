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

# List of sentences that are cool to use or it is an examples of good English sentence patterns.
sentences = [
]

def load_routine() -> list:
    timetable = []
    file = open(config.get_path_to_good_english_sentences(), 'r', encoding="UTF-8", newline='')
    content = file.readlines()
    for line in content:
        timetable.append(line.rstrip())
    return timetable

def get_random_english_sentence() -> str:
    return sentences[random.randint(0, len(sentences) - 1)]
