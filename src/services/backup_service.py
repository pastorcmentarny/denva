# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path

import config_service
from common import dom_utils
from zeroeighttrack import leaderboard_utils


def backup_result(results: list):
    dt = datetime.now()
    dir_path = '{}backup\\{}\\{:02d}\\{:02d}\\'.format(config_service.get_path_for_information_backup(), dt.year,
                                                       dt.month, dt.day)
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    path = dir_path + dom_utils.get_date_with_time_as_filename('zeroeight-results', 'txt', datetime.now())

    eight_track_results = open(path, 'w+', newline='', encoding='utf-8')
    for result in results:
        eight_track_results.write(leaderboard_utils.convert_result_to_line(result))
        eight_track_results.write('\n')
    eight_track_results.close()
    return path
