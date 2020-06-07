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

from pathlib import Path

from zeroeighttrack import leaderboard_utils

path = Path(__file__).parent / '../data/eight_track_results.txt'


def load_leaderboard_from_file() -> list:
    result_file = open(path, 'r')
    content = result_file.readlines()
    results_list = []
    for line in content:
        if not line.isspace():
            results_list.append(leaderboard_utils.convert_line_to_result(line))

    return results_list


def save_leaderboard_to_file(results: list):
    eight_track_results = open(path, 'w', newline='')
    for result in results:
        eight_track_results.write(leaderboard_utils.convert_result_to_line(result))
        eight_track_results.write('\n')
    eight_track_results.close()
