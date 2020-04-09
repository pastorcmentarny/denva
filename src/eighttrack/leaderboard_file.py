import csv

from eighttrack import leaderboard_utils

path = '../data/eight_track_results.txt'


def load_leaderboard_from_file() -> list:
    result_file = open(path, 'r')
    content = result_file.readlines()
    results_list = []
    for line in content:
        results_list.append(leaderboard_utils.convert_line_to_result(line))

    return results_list

def save_leaderboard_to_file(results: list):
    eight_track_results = open(path, 'w', newline='')
    for result in results:
        eight_track_results.write(leaderboard_utils.convert_result_to_line(result))
        eight_track_results.write('\n')
    eight_track_results.close()
