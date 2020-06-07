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

from services import backup_service
from zeroeighttrack import leaderboard_utils, leaderboard_file, leaderboard_score

results = leaderboard_file.load_leaderboard_from_file()


def get_result_by_id(result_id: int) -> dict:
    for result in results:
        if result['id'] == result_id:
            return result
    return {}


def save_results():
    leaderboard_file.save_leaderboard_to_file(results)


def load_results() -> list:
    return results


def add_result(lap_result: str) -> int:
    result_as_dict = leaderboard_utils.convert_lap_result_request_to_dict(lap_result, len(results) + 1)
    backup_service.backup_result(results)
    results.append(result_as_dict)
    leaderboard_file.save_leaderboard_to_file(results)
    return len(results)


def sort_leaderboard_by_time() -> list:
    return sorted(results, key=lambda index: index['time_in_ds'], reverse=False)


def get_top10() -> list:
    all_result = sort_leaderboard_by_time()
    return all_result[:10]


def size() -> int:
    return len(results)


def remove_result_by_id(result_id: int):
    results.pop(result_id - 1)
    save_results()


def get_position_for_id(result_id):
    top_leaderboard = sort_leaderboard_by_time()
    x = []
    for rank in top_leaderboard:
        if rank['id'] == result_id:
            return top_leaderboard.index(rank) + 1
    return []


# score is calculate dynamically so it will reflect change everytime when algorithm changed
def get_top10_by_score():
    score_list = []

    for result in results:
        if 'distance' not in result:
            result['distance'] = 260
        score = leaderboard_score.calculate_score(result['time_in_ds'], result['distance'])
        result['score'] = score
        score_list.append(result)

    return sorted(score_list, key=lambda index: index['score'], reverse=True)[:10]
